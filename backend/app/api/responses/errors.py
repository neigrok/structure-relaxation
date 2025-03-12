from typing import NoReturn

from fastapi import HTTPException
from starlette import status


class ApiError:
    status_code: int
    detail: str

    @classmethod
    def raise_http(cls, exc: Exception) -> NoReturn:
        raise HTTPException(
            status_code=cls.status_code,
            detail=cls.detail
        )


class MaterialNotFoundError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Material not found"


class MaterialMalformedError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid material name format"


class ApiKeyMalformedError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid API key format"


class ApiKeyOutdatedError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "API key has expired"


class JobNotFoundError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Job not found"


class TrajectoryNotFoundError(ApiError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Trajectory not found"
