# File generated from our OpenAPI spec by Stainless.

from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ModelLevel2"]


class ModelLevel2(BaseModel):
    depth: Optional[Literal["level 2"]] = None
