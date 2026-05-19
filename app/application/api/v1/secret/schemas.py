from pydantic import BaseModel


class EditSecretRequestSchema(BaseModel):
    data: str
