"""Data validation utilities for the pipeline."""

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when data validation fails."""


def validate_schema(df: pd.DataFrame, expected_columns: list[str]) -> None:
    """Validate that a DataFrame has the expected columns."""
    missing = set(expected_columns) - set(df.columns)
    if missing:
        raise ValidationError(f"Missing columns: {missing}")


def validate_not_empty(df: pd.DataFrame) -> None:
    """Validate that a DataFrame is not empty."""
    if df.empty:
        raise ValidationError("DataFrame is empty.")


def validate_no_duplicates(df: pd.DataFrame, subset: list[str]) -> None:
    """Validate that there are no duplicate rows for a given subset of columns."""
    dupes = df.duplicated(subset=subset).sum()
    if dupes > 0:
        logger.warning("Found %d duplicate rows on columns %s.", dupes, subset)
        raise ValidationError(f"Found {dupes} duplicate rows.")


def validate_range(
    df: pd.DataFrame, column: str, min_val: Any = None, max_val: Any = None
) -> None:
    """Validate that values in a column are within an expected range."""
    if min_val is not None and (df[column] < min_val).any():
        raise ValidationError(f"Values in {column} below minimum {min_val}.")
    if max_val is not None and (df[column] > max_val).any():
        raise ValidationError(f"Values in {column} above maximum {max_val}.")
