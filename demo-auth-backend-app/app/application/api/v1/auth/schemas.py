from pydantic import BaseModel, Field


class ProfileResponseSchema(BaseModel):
    username: str | None = None
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
