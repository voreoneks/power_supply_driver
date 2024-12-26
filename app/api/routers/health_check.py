from fastapi import APIRouter

from app.api.models.health_check import HealthCheck
from app.config import settings


class HealthCheckRouter:
    api_router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])

    @api_router.get("/")
    def get_health_check() -> HealthCheck:
        """
        Запрос здоровья
        """
        return HealthCheck(
            version=settings.VERSION,
            service=settings.NAME,
            branch=settings.BRANCH,
            commit=settings.COMMIT,
            status=True,
        )
