"""
Bulk product import endpoints for CSV/Excel files with image support.
Allows store owners to upload products in bulk with associated images.
"""
import io
import os
import zipfile
import tempfile
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
from PIL import Image
import logging

from app.api.deps import get_db
from app.db.models import Product, Store, Tag, User
from app.auth.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


def process_image(image_path: str) -> tuple[bytes, str]:
    """
    Process and validate an image file.
    Returns image data and content type.
    """
    try:
        with Image.open(image_path) as img:
            # Validate it's a valid image
            img.verify()

        # Read the actual image data
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Determine content type
        ext = os.path.splitext(image_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        content_type = content_types.get(ext, 'image/jpeg')

        return image_data, content_type
    except Exception as e:
        logger.warning(f"Failed to process image {image_path}: {e}")
        return None, None


def validate_dataframe(df: pd.DataFrame) -> List[str]:
    """
    Validate the imported dataframe has required columns.
    Returns list of errors if any.
    """
    errors = []
    required_columns = ['name', 'price']
    optional_columns = ['sku', 'description', 'url', 'image', 'tags']

    # Check for required columns
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")

    # Check data types
    if 'price' in df.columns:
        try:
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            if df['price'].isna().any():
                invalid_rows = df[df['price'].isna()].index.tolist()
                errors.append(f"Invalid price values in rows: {invalid_rows}")
        except Exception as e:
            errors.append(f"Error processing price column: {e}")

    # Check for empty names
    if 'name' in df.columns:
        empty_names = df[df['name'].isna() | (df['name'] == '')].index.tolist()
        if empty_names:
            errors.append(f"Empty product names in rows: {empty_names}")

    return errors


@router.post("/v1/stores/{store_id}/bulk-import")
async def bulk_import_products(
    store_id: int,
    products_file: UploadFile = File(..., description="CSV or Excel file with products"),
    images_zip: Optional[UploadFile] = File(None, description="ZIP file containing product images"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Bulk import products from CSV/Excel file with optional images ZIP.

    Expected columns:
    - name (required): Product name
    - price (required): Product price
    - sku (optional): Stock Keeping Unit - unique per store
    - description (optional): Product description
    - url (optional): Product URL
    - image (optional): Image filename (should match file in ZIP)
    - tags (optional): Comma-separated tags

    Returns summary of import results.
    """
    # Verify store exists and user owns it
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    if store.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this store")

    # Read the products file
    try:
        file_content = await products_file.read()
        file_extension = os.path.splitext(products_file.filename)[1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload CSV or Excel file."
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Validate dataframe
    validation_errors = validate_dataframe(df)
    if validation_errors:
        raise HTTPException(status_code=400, detail={"errors": validation_errors})

    # Extract images if ZIP provided
    images_dict = {}
    if images_zip:
        try:
            zip_content = await images_zip.read()
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
                    # Extract all files
                    zf.extractall(temp_dir)

                    # Process each image
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                                file_path = os.path.join(root, file)
                                image_data, content_type = process_image(file_path)
                                if image_data:
                                    # Store by filename (without path)
                                    images_dict[file.lower()] = {
                                        'data': image_data,
                                        'content_type': content_type,
                                        'filename': file
                                    }
        except Exception as e:
            logger.error(f"Error processing images ZIP: {e}")
            # Continue without images rather than failing entire import

    # Process products
    products_created = []
    products_failed = []

    for index, row in df.iterrows():
        try:
            # Create product
            product_data = {
                'name': str(row['name']),
                'price': float(row['price']),
                'store_id': store_id,
                'sku': str(row.get('sku', '')) if pd.notna(row.get('sku')) else None,
                'description': str(row.get('description', '')) if pd.notna(row.get('description')) else None,
                'url': str(row.get('url', '')) if pd.notna(row.get('url')) else None,
            }

            # Check for duplicate SKU within this store
            if product_data['sku']:
                existing = db.query(Product).filter(
                    Product.store_id == store_id,
                    Product.sku == product_data['sku']
                ).first()
                if existing:
                    raise ValueError(f"SKU '{product_data['sku']}' already exists in this store")

            # Handle image if specified
            if 'image' in row and pd.notna(row['image']):
                image_filename = str(row['image']).lower()
                if image_filename in images_dict:
                    image_info = images_dict[image_filename]
                    product_data['image_data'] = image_info['data']
                    product_data['image_filename'] = image_info['filename']
                    product_data['image_content_type'] = image_info['content_type']

            product = Product(**product_data)

            # Handle tags if specified
            if 'tags' in row and pd.notna(row['tags']):
                tag_names = [t.strip() for t in str(row['tags']).split(',')]
                for tag_name in tag_names:
                    if tag_name:
                        # Get or create tag
                        tag = db.query(Tag).filter(Tag.name == tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.add(tag)
                        product.tags.append(tag)

            db.add(product)
            products_created.append({
                'row': index,
                'name': product.name,
                'price': product.price
            })

        except Exception as e:
            products_failed.append({
                'row': index,
                'name': row.get('name', 'Unknown'),
                'error': str(e)
            })
            logger.error(f"Failed to import row {index}: {e}")

    # Commit all products
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Return summary
    return {
        'success': True,
        'store_id': store_id,
        'total_rows': len(df),
        'products_created': len(products_created),
        'products_failed': len(products_failed),
        'created_details': products_created[:10],  # First 10 for preview
        'failed_details': products_failed,
        'images_processed': len(images_dict)
    }


@router.get("/v1/import-template")
async def download_import_template(format: str = "csv"):
    """
    Download a template file for bulk product import.

    Parameters:
    - format: "csv" or "xlsx"
    """
    # Create sample data
    sample_data = {
        'sku': [
            'LAPTOP-001',
            'MOUSE-WL-02',
            'KB-MECH-RGB',
            'HUB-USBC-01',
            'STAND-MON-ADJ'
        ],
        'name': [
            'Gaming Laptop Pro',
            'Wireless Mouse',
            'Mechanical Keyboard',
            'USB-C Hub',
            'Monitor Stand'
        ],
        'price': [1299.99, 29.99, 89.99, 49.99, 39.99],
        'description': [
            'High-performance gaming laptop with RTX graphics',
            'Ergonomic wireless mouse with long battery life',
            'RGB mechanical keyboard with blue switches',
            'Multi-port USB-C hub with HDMI and ethernet',
            'Adjustable monitor stand with cable management'
        ],
        'url': [
            'https://example.com/laptop',
            'https://example.com/mouse',
            'https://example.com/keyboard',
            'https://example.com/hub',
            'https://example.com/stand'
        ],
        'image': [
            'laptop.jpg',
            'mouse.jpg',
            'keyboard.jpg',
            'hub.jpg',
            'stand.jpg'
        ],
        'tags': [
            'electronics,gaming,computers',
            'electronics,accessories',
            'electronics,gaming,accessories',
            'electronics,accessories',
            'office,accessories'
        ]
    }

    df = pd.DataFrame(sample_data)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as tmp:
        if format == 'csv':
            df.to_csv(tmp.name, index=False)
            media_type = 'text/csv'
            filename = 'product_import_template.csv'
        elif format == 'xlsx':
            df.to_excel(tmp.name, index=False)
            media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            filename = 'product_import_template.xlsx'
        else:
            raise HTTPException(status_code=400, detail="Format must be 'csv' or 'xlsx'")

        return FileResponse(
            path=tmp.name,
            media_type=media_type,
            filename=filename
        )


@router.get("/v1/import-instructions")
async def get_import_instructions():
    """
    Get detailed instructions for bulk product import.
    """
    return {
        "instructions": {
            "file_formats": ["CSV (.csv)", "Excel (.xlsx, .xls)"],
            "required_columns": {
                "name": "Product name (text)",
                "price": "Product price (number)"
            },
            "optional_columns": {
                "sku": "Stock Keeping Unit - unique per store (text)",
                "description": "Product description (text)",
                "url": "Product URL/link (text)",
                "image": "Image filename matching file in ZIP (text)",
                "tags": "Comma-separated tags (text)"
            },
            "image_upload": {
                "format": "ZIP file containing images",
                "supported_formats": ["jpg", "jpeg", "png", "gif", "webp"],
                "matching": "Image filenames in spreadsheet must match filenames in ZIP"
            },
            "example_row": {
                "sku": "LAPTOP-001",
                "name": "Gaming Laptop",
                "price": 1299.99,
                "description": "High-performance laptop",
                "url": "https://example.com/laptop",
                "image": "laptop.jpg",
                "tags": "electronics,gaming,computers"
            },
            "limits": {
                "max_file_size": "10MB for spreadsheet, 50MB for images ZIP",
                "max_products": "5000 products per import",
                "max_image_size": "5MB per image"
            }
        }
    }