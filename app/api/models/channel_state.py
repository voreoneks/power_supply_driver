from pydantic import BaseModel, Field


class ChannelState(BaseModel):
    number: int = Field(description="Номер канала")
    voltage: float = Field(description="Напряжение")
    current: float = Field(description="Сила тока")
