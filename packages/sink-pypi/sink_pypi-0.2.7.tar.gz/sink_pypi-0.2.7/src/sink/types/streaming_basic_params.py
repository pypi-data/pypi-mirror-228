# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

__all__ = ["StreamingBasicParams", "BasicStreamingRequestNonStreaming", "BasicStreamingRequestStreaming"]


class BasicStreamingRequestNonStreaming(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]

    stream: Literal[False]


class BasicStreamingRequestStreaming(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]

    stream: Required[Literal[True]]


StreamingBasicParams = Union[BasicStreamingRequestNonStreaming, BasicStreamingRequestStreaming]
