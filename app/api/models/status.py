from pydantic import BaseModel, Field


class StatusOut(BaseModel):
    """
    Статус
    """

    status: bool = Field(description="Статус")
