# backend/app/schemas/review.py
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBasic(BaseModel):
    """Basic user info for review author display."""
    id: int
    username: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProductReviewIn(BaseModel):
    """Fields a client may send when creating a review."""
    product_rating: int = Field(..., ge=1, le=5, description="Product quality rating (1-5 stars)")
    info_rating: int = Field(..., ge=1, le=5, description="Information accuracy rating (1-5 stars)")
    comment: Optional[str] = Field(None, max_length=5000, description="Optional review comment")

    model_config = ConfigDict(from_attributes=True)


class ProductReviewUpdate(BaseModel):
    """PATCH body – all fields optional for partial updates."""
    product_rating: Optional[int] = Field(None, ge=1, le=5)
    info_rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=5000)

    model_config = ConfigDict(from_attributes=True)


class ProductReviewOut(ProductReviewIn):
    """What the API returns."""
    id: int
    product_id: int
    user_id: int
    user: Optional[UserBasic] = None
    helpful_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductRatingSummary(BaseModel):
    """Aggregated rating statistics for a product."""
    product_id: int
    total_reviews: int
    average_product_rating: Optional[float] = None
    average_info_rating: Optional[float] = None
    rating_distribution: dict[int, int] = Field(
        default_factory=dict,
        description="Distribution of product ratings: {1: count, 2: count, ..., 5: count}"
    )

    model_config = ConfigDict(from_attributes=True)
