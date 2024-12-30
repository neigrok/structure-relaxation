from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable, Awaitable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from logger import logger
from services.relaxation.repository.in_memory import InMemoryRelaxationJobRepository
from services.relaxation.service import RelaxationService
from settings import Settings
from utils.calculator_factory import MACECalculatorFactory


class AppContainer:
    """All dependencies should be initialized here"""
    def __init__(self) -> None:
        settings = Settings()

        calculator_factory = MACECalculatorFactory(
            model=settings.MODEL,
        )

        job_repository = InMemoryRelaxationJobRepository()

        self.relaxation_service = RelaxationService(
            repository=job_repository,
            calculator_factory=calculator_factory,
            num_workers=settings.NUM_WORKERS,
        )

    def shutdown(self) -> None:
        self.relaxation_service.shutdown()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Creating app container")
    container = AppContainer()
    app.state.container = container
    logger.info("App container created")

    yield

    logger.info("Shutting down app container")
    container.shutdown()
    logger.info("App container shut down")


def create_app() -> FastAPI:
    from api.routes import router

    app = FastAPI(lifespan=lifespan)

    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Lock this down in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"{request.method} {request.url} {response.status_code}")
        return response

    return app
