import io
from typing import Self

from ase import Atoms
from ase.io import write
from pydantic import BaseModel, Field

from services.relaxation.job import Job


class StructuresResponse(BaseModel):
    chemical_formula: str = Field(..., description="Chemical formula")
    bulk: str = Field(..., description="Bulk structure in XYZ format")
    slab: str = Field(..., description="Slab structure in XYZ format")

    @classmethod
    def from_job(cls, job: Job) -> Self:
        atoms = Atoms.fromdict(job["atoms"])
        atoms_slab = Atoms.fromdict(job["atoms_slab"])

        structures = {
            'bulk': io.StringIO(),
            'slab': io.StringIO()
        }

        write(structures['bulk'], atoms, format='xyz')
        write(structures['slab'], atoms_slab, format='xyz')

        return cls(
            chemical_formula=job["chemical_formula"],
            bulk=structures['bulk'].getvalue(),
            slab=structures['slab'].getvalue()
        )


class JobOptimizationResponse(BaseModel):
    progress: float = Field(0.0, description="Progress in percents")
    fmax: float = Field(..., description="Maximum force (eV/Å)")
    max_steps: int = Field(..., description="Maximum number of steps")
    forces: list[float] = Field(..., description="Max force (eV)")
    energies: list[float] = Field(..., description="Energy (eV/Å)")

    @classmethod
    def from_job(cls, job: Job) -> Self:
        return cls(
            progress=job["progress"],
            fmax=job["fmax"],
            max_steps=job["max_steps"],
            energies=job["energies"],
            forces=job["forces"]
        )

class JobResponse(BaseModel):
    id: str = Field(..., description="Job ID")
    status: str = Field(..., description="Status of the job")
    optimization: JobOptimizationResponse = Field(..., description="Optimization results")
    structures: StructuresResponse = Field(..., description="Structures")

    @classmethod
    def from_job(cls, job: Job) -> Self:
        optimization = JobOptimizationResponse.from_job(job)
        structures = StructuresResponse.from_job(job)

        return cls(
            id=job["id"],
            status=job["status"],
            optimization=optimization,
            structures=structures,
        )
