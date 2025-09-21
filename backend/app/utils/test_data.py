"""Utilities for managing test/mock data in the system."""
from typing import List

# Tags that identify test/mock/fake data that should be excluded by default
TEST_DATA_TAGS = [
    "mock-data",      # General mock/fake data
    "test-data",      # Test data
    "staging-only",   # Staging environment test data
    "test-location",  # Location testing data
]

# Tags for demo data that should remain visible
DEMO_DATA_TAGS = [
    "demo-data",      # Demonstration products that should be visible
    "sample-data",    # Sample products for showcasing features
]


def get_excluded_test_tags() -> List[str]:
    """
    Get list of tags that should be excluded by default from search results.

    Returns:
        List of tag names that identify test/mock data
    """
    return TEST_DATA_TAGS.copy()


def should_exclude_tag(tag_name: str) -> bool:
    """
    Check if a tag should be excluded by default.

    Args:
        tag_name: Name of the tag to check

    Returns:
        True if the tag identifies test/mock data that should be excluded
    """
    return tag_name in TEST_DATA_TAGS