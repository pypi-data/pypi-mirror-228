# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Optional

from .._compat import PYDANTIC_V2
from .._models import BaseModel

__all__ = ["MutualRecursionB"]


class MutualRecursionB(BaseModel):
    a: Optional[MutualRecursionA] = None


from .mutual_recursion_a import MutualRecursionA

if PYDANTIC_V2:
    MutualRecursionB.model_rebuild()
else:
    MutualRecursionB.update_forward_refs()  # type: ignore
