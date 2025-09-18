"""Admin dashboard API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Dict, Any, List

from app.api.deps import get_db
from app.db.models import User, Product, Store, Tag, UserRole
from app.auth.security import get_current_user

router = APIRouter()

# Fallback admin email for backwards compatibility (before role migration is run)
FALLBACK_ADMIN_EMAIL = "ruben.jimenezmejias@gmail.com"


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Verify the current user is an admin."""
    # Check if user has role field (after migration) or fallback to email check
    if hasattr(current_user, 'role'):
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Admin access required")
    else:
        # Fallback for before migration is run
        if current_user.email != FALLBACK_ADMIN_EMAIL:
            raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
) -> Dict[str, Any]:
    """Get dashboard statistics for admin."""

    # Basic counts
    total_users = db.query(func.count(User.id)).scalar()
    total_products = db.query(func.count(Product.id)).scalar()
    total_stores = db.query(func.count(Store.id)).scalar()
    total_tags = db.query(func.count(Tag.id)).scalar()

    # Recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)

    # Products by store type
    store_type_stats = db.query(
        Store.type,
        func.count(Store.id).label('count')
    ).group_by(Store.type).all()

    # Most active users (by products created)
    top_creators = db.query(
        User.email,
        User.username,
        func.count(Product.id).label('product_count')
    ).join(Product, Product.creator_id == User.id)\
     .group_by(User.id, User.email, User.username)\
     .order_by(desc('product_count'))\
     .limit(5)\
     .all()

    # Most used tags
    top_tags = db.query(
        Tag.name,
        func.count(Product.id).label('usage_count')
    ).join(Product.tags)\
     .group_by(Tag.id, Tag.name)\
     .order_by(desc('usage_count'))\
     .limit(10)\
     .all()

    # Recent products
    recent_products = db.query(
        Product.name,
        Product.price,
        Store.name.label('store_name')
    ).join(Store)\
     .order_by(desc(Product.id))\
     .limit(10)\
     .all()

    return {
        "counts": {
            "users": total_users,
            "products": total_products,
            "stores": total_stores,
            "tags": total_tags
        },
        "store_types": [
            {"type": st[0].value if st[0] else "unknown", "count": st[1]}
            for st in store_type_stats
        ],
        "top_creators": [
            {
                "email": creator[0],
                "username": creator[1],
                "product_count": creator[2]
            }
            for creator in top_creators
        ],
        "top_tags": [
            {"name": tag[0], "count": tag[1]}
            for tag in top_tags
        ],
        "recent_products": [
            {
                "name": p[0],
                "price": float(p[1]) if p[1] else 0,
                "store": p[2]
            }
            for p in recent_products
        ]
    }


@router.get("/users")
def get_users_list(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
) -> List[Dict[str, Any]]:
    """Get list of users with their statistics."""

    users = db.query(
        User.id,
        User.email,
        User.username,
        func.count(func.distinct(Product.id)).label('product_count'),
        func.count(func.distinct(Store.id)).label('store_count')
    ).outerjoin(Product, Product.creator_id == User.id)\
     .outerjoin(Store, Store.owner_id == User.id)\
     .group_by(User.id, User.email, User.username)\
     .offset(skip)\
     .limit(limit)\
     .all()

    return [
        {
            "id": u[0],
            "email": u[1],
            "username": u[2],
            "products": u[3],
            "stores": u[4]
        }
        for u in users
    ]