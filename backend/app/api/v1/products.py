# backend/app/api/v1/products.py
from collections.abc import Generator
from sqlalchemy import or_, func
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.models import Product, User, Tag
from app.schemas import product as schema
from app.auth.security import get_current_user
from app.api.deps import get_db
from app.search.indexing import index_product, delete_product_from_index
from app.search.client import search_client
from app.logging_config import get_logger

router = APIRouter()
logger = get_logger("api.products")


# ───────────────────────────────────────────
# CRUD endpoints
# ───────────────────────────────────────────
@router.get("/", response_model=list[schema.ProductOut])
def list_products(
    store_id: int | None = None,
    store_name: str | None = None,
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    tags: str | None = None,
    sort_by: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if store_id is not None:
        query = query.filter(Product.store_id == store_id)

    if store_name is not None:
        # Join with Store table to filter by store name (case-insensitive partial match)
        from app.db.models import Store
        query = query.join(Store).filter(Store.name.ilike(f"%{store_name}%"))

    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    if min_price is not None:
        query = query.filter(or_(Product.price >= min_price, Product.price.is_(None)))

    if max_price is not None:
        query = query.filter(or_(Product.price <= max_price, Product.price.is_(None)))

    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        # Only apply tag filter if tag_list contains actual tag names
        if tag_list and any(tag_name for tag_name in tag_list):
            query = query.join(Product.tags).filter(Tag.name.in_(tag_list))

    if sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "name_asc":
        query = query.order_by(Product.name.asc())
    elif sort_by == "random":
        query = query.order_by(func.random())

    return query.offset(offset).limit(limit).all()


@router.get("/store/{store_id}", response_model=list[schema.ProductOut])
def list_products_by_store(store_id: int, db: Session = Depends(get_db)):
    """List products for a specific store."""
    return db.query(Product).filter(Product.store_id == store_id).order_by(func.random()).all()


# TODO HOW TO UPDATE PRODUCT
@router.post("/", response_model=schema.ProductOut, status_code=201)
def create_product(
    payload: schema.ProductIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info("Creating product", 
                product_name=payload.name, 
                user_id=current_user.id, 
                store_id=payload.store_id)
    
    if payload.store_id is not None:
        # If product is linked to a store, check for uniqueness by name and store_id
        existing = (
            db.query(Product)
            .filter_by(name=payload.name, store_id=payload.store_id)
            .first()
        )
        if existing:
            logger.warning("Product creation failed - duplicate in store", 
                          product_name=payload.name, 
                          store_id=payload.store_id)
            raise HTTPException(409, "Product with this name already exists in this store")
    else:
        # If product is an orphan, check for uniqueness by name and creator_id
        existing = (
            db.query(Product)
            .filter_by(name=payload.name, creator_id=current_user.id)
            .first()
        )
        if existing:
            logger.warning("Product creation failed - duplicate orphan", 
                          product_name=payload.name, 
                          creator_id=current_user.id)
            raise HTTPException(409, "You already have an orphan product with this name")

    product = Product(
        **payload.model_dump(),
        creator_id=current_user.id,
        updated_by_id=current_user.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    logger.info("Product created successfully", 
               product_id=product.id, 
               product_name=product.name,
               price=product.price)
    
    # Index in Elasticsearch if available
    if search_client.is_available():
        try:
            index_product(product)
            logger.debug("Product indexed in Elasticsearch", product_id=product.id)
        except Exception as e:
            logger.error("Failed to index product in Elasticsearch", 
                        product_id=product.id, 
                        error=str(e))
    
    return product


@router.get("/{product_id}", response_model=schema.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.patch("/{product_id}", response_model=schema.ProductOut)
def update_product(
    product_id: int,
    payload: schema.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    
    # Check ownership - only creator can edit their product
    if product.creator_id != current_user.id:
        raise HTTPException(403, "You can only edit products you created")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    product.updated_by_id = current_user.id

    db.commit()
    db.refresh(product)
    
    # Update in Elasticsearch if available
    if search_client.is_available():
        try:
            index_product(product)
        except Exception as e:
            logger.warning(f"Failed to update product {product.id} in Elasticsearch: {e}")
    
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    
    # Delete from Elasticsearch if available
    if search_client.is_available():
        try:
            delete_product_from_index(product_id)
        except Exception as e:
            logger.warning(f"Failed to delete product {product_id} from Elasticsearch: {e}")
    
    db.delete(product)
    db.commit()


@router.post("/{product_id}/tags/{tag_id}", response_model=schema.ProductOut, status_code=201)
def add_tag_to_product(
    product_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    product.tags.append(tag)
    db.commit()
    db.refresh(product)
    
    # Update in Elasticsearch if available (tags changed)
    if search_client.is_available():
        try:
            index_product(product)
        except Exception as e:
            logger.warning(f"Failed to update product {product.id} tags in Elasticsearch: {e}")
    
    return product


@router.get("/{product_id}/image")
def get_product_image(product_id: int, db: Session = Depends(get_db)):
    """Get the image data for a product."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    
    if not product.image_data:
        raise HTTPException(404, "No image data available for this product")
    
    # Return the image data with proper content type
    return Response(
        content=product.image_data,
        media_type=product.image_content_type or "image/jpeg",
        headers={
            "Content-Disposition": f"inline; filename={product.image_filename or 'image.jpg'}"
        }
    )
