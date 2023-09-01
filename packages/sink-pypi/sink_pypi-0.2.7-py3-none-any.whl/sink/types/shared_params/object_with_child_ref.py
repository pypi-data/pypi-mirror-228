# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .simple_object import SimpleObject

__all__ = ["ObjectWithChildRef"]


class ObjectWithChildRef(TypedDict, total=False):
    bar: Required[SimpleObject]

    foo: Required[str]
