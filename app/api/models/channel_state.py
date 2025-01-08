from datetime import datetime

from pydantic import BaseModel, Field


class ChannelState(BaseModel):
    number: int = Field(description="Номер канала")
    measure_time: datetime = Field(description="Время измерения")
    voltage: float = Field(description="Напряжение")
    current: float = Field(description="Сила тока")
