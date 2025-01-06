import io
from typing import Self

from ase import Atoms
from ase.io import write
from pydantic import BaseModel, Field

from services.relaxation.job import Job


class StructureResponse(BaseModel):
    format: str = Field(..., description="Format of the structure")
    structure: str = Field(..., description="Structure in the given format")


class StructuresResponse(BaseModel):
    chemical_formula: str = Field(..., description="Chemical formula")
    bulk: StructureResponse = Field(..., description="Bulk structure in CIF format")
    slab: StructureResponse = Field(..., description="Slab structure in CIF format")

    @classmethod
    def from_job(cls, job: Job) -> Self:
        structure_format = "cif"

        atoms = Atoms.fromdict(job["atoms"])
        atoms_slab = Atoms.fromdict(job["atoms_slab"])

        structures = {
            'bulk': io.BytesIO(),
            'slab': io.BytesIO()
        }

        write(structures['bulk'], atoms, format=structure_format)
        write(structures['slab'], atoms_slab, format=structure_format)

        bulk_str = structures['bulk'].getvalue().decode('utf-8')
        slab_str = structures['slab'].getvalue().decode('utf-8')

        return cls(
            chemical_formula=job["chemical_formula"],
            bulk=StructureResponse(
                format=structure_format,
                structure=bulk_str,
            ),
            slab=StructureResponse(
                format=structure_format,
                structure=slab_str,
            )
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
