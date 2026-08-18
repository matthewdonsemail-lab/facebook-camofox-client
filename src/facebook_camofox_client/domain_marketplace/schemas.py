"""Marketplace listing contracts."""
from __future__ import annotations

from pydantic import BaseModel, Field


class MarketplaceListingInput(BaseModel):
    title: str = Field(min_length=1)
    price: str = Field(min_length=1)
    category: str = "Miscellaneous"
    condition: str = "Used - Good"
    description: str = ""
    image_paths: list[str] = Field(default_factory=list)


class MarketplaceListingOutput(BaseModel):
    published: bool
    listing_url: str | None = None
    error: str | None = None
