from fastapi import APIRouter

from api.dependencies.relaxation_service import RelaxationServiceDependency
from api.responses.errors import JobNotFoundError
from api.responses.job import JobResponse
from services.relaxation.repository.abstract import JobNotFound

router = APIRouter()


@router.get("/relaxations/{relaxation_id}", response_model=JobResponse)
def get_relaxation(
    relaxation_id: str,
    service: RelaxationServiceDependency,
) -> JobResponse:
    """Returns the job with the given id"""
    try:
        job = service.get_job(relaxation_id)
        return JobResponse.from_job(job)
    except JobNotFound as e:
        raise JobNotFoundError.raise_http(e)
