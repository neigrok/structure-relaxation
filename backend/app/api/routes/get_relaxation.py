from fastapi import APIRouter, Response

from api.dependencies.relaxation_service import RelaxationServiceDependency
from api.responses.errors import JobNotFoundError, TrajectoryNotFoundError
from api.responses.job import JobResponse
from services.relaxation.repository.abstract import JobNotFound
from services.relaxation.service import TrajectoryIsEmpty

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


@router.get("/relaxations/{relaxation_id}/trajectory")
def get_trajectory(
    relaxation_id: str,
    service: RelaxationServiceDependency,
) -> Response:
    """Returns the trajectory of the relaxation in XYZ format"""
    try:
        job = service.get_job(relaxation_id)
        buffer = service.get_trajectory_xyz(job)
        return Response(
            content=buffer.getvalue(),
            media_type="chemical/x-xyz",
            headers={
                "Content-Disposition": f"attachment; filename=trajectory_{relaxation_id}.xyz"
            }
        )
    except JobNotFound as e:
        raise JobNotFoundError.raise_http(e)
    except TrajectoryIsEmpty as e:
        raise TrajectoryNotFoundError.raise_http(e)
