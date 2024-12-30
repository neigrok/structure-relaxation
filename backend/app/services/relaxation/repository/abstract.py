from abc import abstractmethod
from typing import NoReturn

from services.relaxation.job import Job


class JobNotFound(Exception):
    pass


class JobAlreadyExists(Exception):
    pass


class AbstractRelaxationJobRepository:
    """I will implement in-memory repository, you can implement whatever you want"""

    @abstractmethod
    def create(self, job: Job) -> None:
        """Save new job in the storage"""
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job:
        """Get job from the storage"""
        pass

    @abstractmethod
    def update(self, job: Job) -> None:
        """Update job in the storage"""
        pass

    def _raise_not_found(self, job_id: str) -> NoReturn:
        """Raise exception if job with given id does not exist"""
        raise JobNotFound(f"Job with id {job_id} does not exist")

    def _raise_already_exists(self, job_id: str) -> NoReturn:
        """Raise exception if job with given id already exists"""
        raise JobAlreadyExists(f"Job with id {job_id} already exists")
