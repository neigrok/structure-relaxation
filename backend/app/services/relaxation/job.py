import enum
from typing import TypedDict, Any


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class Job(TypedDict):
    """Job is a process that is running in the background"""
    id: str

    # Fields that store data for calculations
    fmax: float
    max_steps: int

    # Fields that are used to create the job
    chemical_formula: str
    atoms: dict[str, Any]
    atoms_slab: dict[str, Any]

    # Fields that are updated during the job
    status: str
    progress: float

    energies: list[float]
    forces: list[float]
