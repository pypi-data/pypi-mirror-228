# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BodyParamWithModelPropertyParams", "MyModel"]


class BodyParamWithModelPropertyParams(TypedDict, total=False):
    foo: str

    my_model: MyModel


class MyModel(TypedDict, total=False):
    bar: bool
