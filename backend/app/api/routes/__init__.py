from fastapi import APIRouter

from .create_relaxation import router as optimize_router
from .get_relaxation import router as get_job_router

router = APIRouter()

router.include_router(optimize_router)
router.include_router(get_job_router)
