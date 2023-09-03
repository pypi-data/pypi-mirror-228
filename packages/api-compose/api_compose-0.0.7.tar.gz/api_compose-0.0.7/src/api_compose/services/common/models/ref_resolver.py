"""
Intermediate models with references still not yet resolved
"""

from typing import Dict, Any

from pydantic import Field

from api_compose.services.common.models.base import BaseModel


class RefResolverModel(BaseModel):
    id: str = ''
    ref: str = Field(description='Reference Path to Manifest File')
    context: Dict[str, Any] = Field(description='Context used to render manifest file')
