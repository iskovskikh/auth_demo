from typing import (
    Generic,
    TypeVar,
)

from pydantic import BaseModel


class ErrorDescriptionSchema(BaseModel):
    error: str


class ErrorSchema(BaseModel):
    detail: ErrorDescriptionSchema


IT = TypeVar("IT")


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    offset: int
    limit: int
    items: IT
