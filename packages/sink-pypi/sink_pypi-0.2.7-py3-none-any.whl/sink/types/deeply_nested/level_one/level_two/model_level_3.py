# File generated from our OpenAPI spec by Stainless.

from typing import Optional
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["ModelLevel3"]


class ModelLevel3(BaseModel):
    depth: Optional[Literal["level 3"]] = None
