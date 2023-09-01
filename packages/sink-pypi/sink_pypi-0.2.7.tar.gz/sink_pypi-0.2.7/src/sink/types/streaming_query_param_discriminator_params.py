# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "StreamingQueryParamDiscriminatorParams",
    "QueryParamDiscriminatorRequestNonStreaming",
    "QueryParamDiscriminatorRequestStreaming",
]


class QueryParamDiscriminatorRequestNonStreaming(TypedDict, total=False):
    prompt: Required[str]

    should_stream: Literal[False]


class QueryParamDiscriminatorRequestStreaming(TypedDict, total=False):
    prompt: Required[str]

    should_stream: Required[Literal[True]]


StreamingQueryParamDiscriminatorParams = Union[
    QueryParamDiscriminatorRequestNonStreaming, QueryParamDiscriminatorRequestStreaming
]
