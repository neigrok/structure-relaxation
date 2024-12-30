from threading import Lock

from services.relaxation.job import Job
from services.relaxation.repository.abstract import AbstractRelaxationJobRepository


class InMemoryRelaxationJobRepository(AbstractRelaxationJobRepository):
    """
    In memory repository stores all jobs in the RAM.

    Pros:
        - Fast
        - Easy to implement
    Cons:
        - No persistence (data will be lost after restart)
        - Memory usage scales linearly with job count
        - Limited by available system memory (risk to be killed by OOM)
    """

    def __init__(self) -> None:
        self.jobs: dict[str, Job] = {}
        self._lock = Lock()

    def create(self, job: Job) -> None:
        job_id = job["id"]

        with self._lock:
            if job_id in self.jobs:
                self._raise_already_exists(job_id)

            self.jobs[job_id] = job

    def get(self, job_id: str) -> Job:
        if job := self.jobs.get(job_id):
            return job

        self._raise_not_found(job_id)

    def update(self, job: Job) -> None:
        job_id = job["id"]
        if job_id not in self.jobs:
            self._raise_not_found(job_id)

        self.jobs[job_id] = job
