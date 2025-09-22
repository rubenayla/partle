# backend/app/api/v1/products.py
from collections.abc import Generator
from sqlalchemy import or_, func, and_, not_
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File
from sqlalchemy.orm import Session, joinedload

from app.db.models import Product, User, Tag, Store
from app.schemas import product as schema
from app.auth.security import get_current_user
from app.api.deps import get_db
from app.search.indexing import index_product, delete_product_from_index
from app.search.client import search_client
from app.logging_config import get_logger
from app.utils.test_data import get_excluded_test_tags

router = APIRouter()
logger = get_logger("api.products")


# ───────────────────────────────────────────
# CRUD endpoints
# ───────────────────────────────────────────
@router.get("/", response_model=list[schema.ProductOut])
def list_products(
    store_id: int | None = None,
    store_ids: str | None = None,  # Comma-separated list of store IDs
    store_name: str | None = None,
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    tags: str | None = None,
    sort_by: str | None = None,
    user_lat: float | None = None,  # User's latitude for distance sorting
    user_lon: float | None = None,  # User's longitude for distance sorting
    include_test_data: bool = False,  # Include mock/test data in results
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    # Start with eager loading to prevent N+1 queries
    query = db.query(Product).options(
        joinedload(Product.store),
        joinedload(Product.creator),
        joinedload(Product.tags)
    )

    # Exclude test/mock data by default unless explicitly requested
    if not include_test_data:
        excluded_tags = get_excluded_test_tags()
        if excluded_tags:
            # Subquery to find products with excluded tags
            excluded_products = (
                db.query(Product.id)
                .join(Product.tags)
                .filter(Tag.name.in_(excluded_tags))
                .subquery()
            )
            # Exclude products that have any of the excluded tags
            query = query.filter(~Product.id.in_(excluded_products))

    # Handle multiple store IDs if provided
    if store_ids is not None:
        try:
            store_id_list = [int(sid.strip()) for sid in store_ids.split(',') if sid.strip()]
            if store_id_list:
                query = query.filter(Product.store_id.in_(store_id_list))
        except ValueError:
            # Invalid store_ids format, ignore the filter
            pass
    elif store_id is not None:
        # Single store_id for backward compatibility
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

    # Handle distance-based sorting
    if sort_by == "distance" and user_lat is not None and user_lon is not None:
        from app.db.models import Store
        # Join with Store table
        query = query.join(Store)

        # Calculate distance using Haversine formula
        # This uses PostgreSQL's math functions for distance calculation
        # Distance in kilometers
        distance = func.acos(
            func.cos(func.radians(user_lat)) *
            func.cos(func.radians(Store.lat)) *
            func.cos(func.radians(Store.lon) - func.radians(user_lon)) +
            func.sin(func.radians(user_lat)) *
            func.sin(func.radians(Store.lat))
        ) * 6371  # Earth's radius in km

        # Filter out stores without coordinates and sort by distance
        query = query.filter(Store.lat.isnot(None), Store.lon.isnot(None))
        query = query.order_by(distance)
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "name_asc":
        query = query.order_by(Product.name.asc())
    elif sort_by == "random":
        query = query.order_by(func.random())
    elif sort_by == "created_at":
        query = query.order_by(Product.created_at.desc())
    elif sort_by == "created_at_asc":
        query = query.order_by(Product.created_at.asc())
    else:
        # Default sort by creation date if no valid sort_by specified
        query = query.order_by(Product.created_at.desc())

    return query.offset(offset).limit(limit).all()


@router.get("/my", response_model=list[schema.ProductOut])
def list_my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List products created by the current user - with eager loading to prevent N+1 queries."""
    return (
        db.query(Product)
        .options(
            joinedload(Product.store),
            joinedload(Product.creator),
            joinedload(Product.tags)
        )
        .filter(Product.creator_id == current_user.id)
        .order_by(Product.created_at.desc())
        .all()
    )


@router.get("/store/{store_id}", response_model=list[schema.ProductOut])
def list_products_by_store(
    store_id: int,
    include_test_data: bool = False,
    db: Session = Depends(get_db)
):
    """List products for a specific store - with eager loading to prevent N+1 queries."""
    query = (
        db.query(Product)
        .options(
            joinedload(Product.store),
            joinedload(Product.creator),
            joinedload(Product.tags)
        )
        .filter(Product.store_id == store_id)
    )

    # Exclude test/mock data by default unless explicitly requested
    if not include_test_data:
        excluded_tags = get_excluded_test_tags()
        if excluded_tags:
            excluded_products = (
                db.query(Product.id)
                .join(Product.tags)
                .filter(Tag.name.in_(excluded_tags))
                .subquery()
            )
            query = query.filter(~Product.id.in_(excluded_products))

    return query.order_by(func.random()).all()


@router.get("/user/{user_id}", response_model=list[schema.ProductOut])
def list_products_by_user(user_id: int, db: Session = Depends(get_db)):
    """List products uploaded by a specific user - with eager loading to prevent N+1 queries."""
    return (
        db.query(Product)
        .options(
            joinedload(Product.store),
            joinedload(Product.creator),
            joinedload(Product.tags)
        )
        .filter(Product.creator_id == user_id)
        .order_by(Product.created_at.desc())
        .all()
    )


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
        # Check if store exists and user owns it
        store = db.query(Store).filter_by(id=payload.store_id).first()
        if not store:
            raise HTTPException(404, "Store not found")

        # Only the store owner can add products to their store
        if store.owner_id != current_user.id:
            raise HTTPException(403, "You can only add products to your own stores")

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
    # Use query with joinedload to include creator information
    from sqlalchemy.orm import joinedload
    product = db.query(Product).options(
        joinedload(Product.creator),
        joinedload(Product.store)
    ).filter(Product.id == product_id).first()
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


@router.post("/{product_id}/image", response_model=schema.ProductOut)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload an image for a product."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    
    # Check ownership - only creator can edit their product
    if product.creator_id != current_user.id:
        raise HTTPException(403, "You can only edit products you created")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"Invalid file type. Allowed types: {', '.join(allowed_types)}")
    
    # Read file data (limit to 10MB)
    file_data = await file.read()
    if len(file_data) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(400, "File too large. Maximum size is 10MB")
    
    # Update product with image data
    product.image_data = file_data
    product.image_filename = file.filename
    product.image_content_type = file.content_type
    product.updated_by_id = current_user.id
    
    db.commit()
    db.refresh(product)
    
    logger.info("Product image uploaded", 
               product_id=product.id, 
               filename=file.filename,
               size_bytes=len(file_data))
    
    # Update in Elasticsearch if available
    if search_client.is_available():
        try:
            index_product(product)
        except Exception as e:
            logger.warning(f"Failed to update product {product.id} in Elasticsearch: {e}")
    
    return product


@router.delete("/{product_id}/image", status_code=204)
def delete_product_image(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete the image from a product."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    
    # Check ownership - only creator can edit their product
    if product.creator_id != current_user.id:
        raise HTTPException(403, "You can only edit products you created")
    
    # Clear image data
    product.image_data = None
    product.image_filename = None
    product.image_content_type = None
    product.updated_by_id = current_user.id
    
    db.commit()
    
    logger.info("Product image deleted", product_id=product.id)
    
    # Update in Elasticsearch if available
    if search_client.is_available():
        try:
            index_product(product)
        except Exception as e:
            logger.warning(f"Failed to update product {product.id} in Elasticsearch: {e}")
