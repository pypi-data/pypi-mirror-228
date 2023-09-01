# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional

from .._compat import PYDANTIC_V2
from .._models import BaseModel

__all__ = ["MutualRecursionA"]


class MutualRecursionA(BaseModel):
    b: Optional[MutualRecursionB] = None


from .mutual_recursion_b import MutualRecursionB

if PYDANTIC_V2:
    MutualRecursionA.model_rebuild()
else:
    MutualRecursionA.update_forward_refs()  # type: ignore
