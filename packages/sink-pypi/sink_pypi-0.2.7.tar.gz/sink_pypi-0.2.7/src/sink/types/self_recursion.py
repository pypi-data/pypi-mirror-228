# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional

from .._compat import PYDANTIC_V2
from .._models import BaseModel

__all__ = ["SelfRecursion"]


class SelfRecursion(BaseModel):
    name: str

    child: Optional[SelfRecursion] = None


if PYDANTIC_V2:
    SelfRecursion.model_rebuild()
else:
    SelfRecursion.update_forward_refs()  # type: ignore
