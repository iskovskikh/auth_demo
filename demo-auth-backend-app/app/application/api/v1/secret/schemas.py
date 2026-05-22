from pydantic import BaseModel


class EditSecretRequestSchema(BaseModel):
    value: str
