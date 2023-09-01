# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "StreamingNestedParamsParams",
    "NestedStreamingRequestNonStreaming",
    "NestedStreamingRequestNonStreamingParentObject",
    "NestedStreamingRequestNonStreamingParentObjectArrayProp",
    "NestedStreamingRequestNonStreamingParentObjectChildProp",
    "NestedStreamingRequestStreaming",
    "NestedStreamingRequestStreamingParentObject",
    "NestedStreamingRequestStreamingParentObjectArrayProp",
    "NestedStreamingRequestStreamingParentObjectChildProp",
]


class NestedStreamingRequestNonStreaming(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]

    parent_object: NestedStreamingRequestNonStreamingParentObject

    stream: Literal[False]


class NestedStreamingRequestNonStreamingParentObjectArrayProp(TypedDict, total=False):
    from_array_items: bool


class NestedStreamingRequestNonStreamingParentObjectChildProp(TypedDict, total=False):
    from_object: str


class NestedStreamingRequestNonStreamingParentObject(TypedDict, total=False):
    array_prop: List[NestedStreamingRequestNonStreamingParentObjectArrayProp]

    child_prop: NestedStreamingRequestNonStreamingParentObjectChildProp


class NestedStreamingRequestStreaming(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]

    stream: Required[Literal[True]]

    parent_object: NestedStreamingRequestStreamingParentObject


class NestedStreamingRequestStreamingParentObjectArrayProp(TypedDict, total=False):
    from_array_items: bool


class NestedStreamingRequestStreamingParentObjectChildProp(TypedDict, total=False):
    from_object: str


class NestedStreamingRequestStreamingParentObject(TypedDict, total=False):
    array_prop: List[NestedStreamingRequestStreamingParentObjectArrayProp]

    child_prop: NestedStreamingRequestStreamingParentObjectChildProp


StreamingNestedParamsParams = Union[NestedStreamingRequestNonStreaming, NestedStreamingRequestStreaming]
