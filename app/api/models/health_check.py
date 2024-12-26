from typing import Optional

from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    version: str = Field(description="Версия сервиса")
    commit: Optional[str] = Field(description="Коммит")
    branch: Optional[str] = Field(description="Ветка")
    status: bool = Field(description="Статус сервиса")
    service: str = Field(description="Название сервиса")
