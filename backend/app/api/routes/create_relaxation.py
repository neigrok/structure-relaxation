from fastapi import APIRouter
from pydantic import BaseModel, Field

from api.dependencies.relaxation_service import RelaxationServiceDependency
from api.responses.errors import ApiKeyOutdatedError, ApiKeyMalformedError, MaterialMalformedError, \
    MaterialNotFoundError
from api.responses.job import JobResponse
from services.relaxation.service import ApiKeyOutdated, ApiKeyMalformed, MaterialMalformedName, MaterialNotFound

router = APIRouter()

class RelaxationRequest(BaseModel):
    mp_api_key: str = Field(..., description="Materials Project API key")
    material_id: str = Field(..., description="Materials Project material ID")
    fmax: float = Field(0.05, description="Maximum force in eV/Å")
    max_steps: int = Field(30, description="Maximum number of steps")


@router.post("/relaxations", response_model=JobResponse)
def create_relaxation(
    request: RelaxationRequest,
    service: RelaxationServiceDependency,
) -> JobResponse:
    """The relaxation would be done in the background, poll for the results using job_id"""
    try:
        job = service.create_job(
            material_id=request.material_id,
            fmax=request.fmax,
            max_steps=request.max_steps,
            mpr_api_key=request.mp_api_key,
        )

        return JobResponse.from_job(job)
    except MaterialNotFound as e:
        raise MaterialNotFoundError.raise_http(e)
    except MaterialMalformedName as e:
        raise MaterialMalformedError.raise_http(e)
    except ApiKeyMalformed as e:
        raise ApiKeyMalformedError.raise_http(e)
    except ApiKeyOutdated as e:
        raise ApiKeyOutdatedError.raise_http(e)
