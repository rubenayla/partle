# backend/app/api/v1/reviews.py
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.models import ProductReview, Product, User
from app.schemas import review as schema
from app.auth.security import get_current_user, get_optional_user
from app.api.deps import get_db
from app.logging_config import get_logger

router = APIRouter()
logger = get_logger("api.reviews")


# ───────────────────────────────────────────
# Product Reviews CRUD endpoints
# ───────────────────────────────────────────

@router.get("/{product_id}/reviews", response_model=list[schema.ProductReviewOut])
def list_product_reviews(
    product_id: int,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """List all reviews for a specific product."""
    # Verify product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    reviews = (
        db.query(ProductReview)
        .options(joinedload(ProductReview.user))
        .filter(ProductReview.product_id == product_id)
        .order_by(ProductReview.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return reviews


@router.get("/{product_id}/ratings", response_model=schema.ProductRatingSummary)
def get_product_rating_summary(
    product_id: int,
    db: Session = Depends(get_db),
):
    """Get aggregated rating statistics for a product."""
    # Verify product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    # Get aggregate statistics
    stats = db.query(
        func.count(ProductReview.id).label('total_reviews'),
        func.avg(ProductReview.product_rating).label('avg_product_rating'),
        func.avg(ProductReview.info_rating).label('avg_info_rating'),
    ).filter(ProductReview.product_id == product_id).first()

    # Get rating distribution
    rating_dist = db.query(
        ProductReview.product_rating,
        func.count(ProductReview.id).label('count')
    ).filter(
        ProductReview.product_id == product_id
    ).group_by(
        ProductReview.product_rating
    ).all()

    # Convert to dict
    distribution = {rating: count for rating, count in rating_dist}

    return schema.ProductRatingSummary(
        product_id=product_id,
        total_reviews=stats.total_reviews or 0,
        average_product_rating=round(stats.avg_product_rating, 1) if stats.avg_product_rating else None,
        average_info_rating=round(stats.avg_info_rating, 1) if stats.avg_info_rating else None,
        rating_distribution=distribution
    )


@router.post("/{product_id}/reviews", response_model=schema.ProductReviewOut, status_code=status.HTTP_201_CREATED)
def create_product_review(
    product_id: int,
    review_in: schema.ProductReviewIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new review for a product. Users can only have one review per product."""
    # Verify product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    # Check if user already reviewed this product
    existing_review = db.query(ProductReview).filter(
        ProductReview.product_id == product_id,
        ProductReview.user_id == current_user.id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already reviewed this product. Use PUT to update your review."
        )

    # Create new review
    review = ProductReview(
        product_id=product_id,
        user_id=current_user.id,
        product_rating=review_in.product_rating,
        info_rating=review_in.info_rating,
        comment=review_in.comment,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    # Eager load user relationship
    review = db.query(ProductReview).options(
        joinedload(ProductReview.user)
    ).filter(ProductReview.id == review.id).first()

    logger.info(f"User {current_user.id} created review {review.id} for product {product_id}")
    return review


@router.get("/{product_id}/reviews/my", response_model=schema.ProductReviewOut | None)
def get_my_review_for_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the current user's review for a specific product."""
    review = db.query(ProductReview).options(
        joinedload(ProductReview.user)
    ).filter(
        ProductReview.product_id == product_id,
        ProductReview.user_id == current_user.id
    ).first()

    return review


@router.put("/{product_id}/reviews/{review_id}", response_model=schema.ProductReviewOut)
def update_product_review(
    product_id: int,
    review_id: int,
    review_update: schema.ProductReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing review. Users can only update their own reviews."""
    review = db.query(ProductReview).filter(
        ProductReview.id == review_id,
        ProductReview.product_id == product_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # Check ownership
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )

    # Update fields
    update_data = review_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)

    # Eager load user relationship
    review = db.query(ProductReview).options(
        joinedload(ProductReview.user)
    ).filter(ProductReview.id == review.id).first()

    logger.info(f"User {current_user.id} updated review {review_id}")
    return review


@router.delete("/{product_id}/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_review(
    product_id: int,
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a review. Users can only delete their own reviews."""
    review = db.query(ProductReview).filter(
        ProductReview.id == review_id,
        ProductReview.product_id == product_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # Check ownership
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )

    db.delete(review)
    db.commit()

    logger.info(f"User {current_user.id} deleted review {review_id}")
    return None
