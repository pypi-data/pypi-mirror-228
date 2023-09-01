# File generated from our OpenAPI spec by Stainless.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ModelLevel1"]


class ModelLevel1(BaseModel):
    depth: Optional[Literal["level 1"]] = None
