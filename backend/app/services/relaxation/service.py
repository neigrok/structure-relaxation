import queue
import threading
import uuid
from multiprocessing import Queue
from typing import cast

from ase import Atoms
from mp_api.client import MPRester, MPRestError  # type: ignore[import-untyped]
from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor

from logger import logger
from utils.calculator_factory import MACECalculatorFactory
from .job import Job, JobStatus
from .repository.abstract import AbstractRelaxationJobRepository
from .worker import RelaxationWorker


class MaterialNotFound(Exception):
    pass


class MaterialMalformedName(Exception):
    pass


class ApiKeyMalformed(Exception):
    pass


class ApiKeyOutdated(Exception):
    pass


class RelaxationService:
    def __init__(self,
                 repository: AbstractRelaxationJobRepository,
                 calculator_factory: MACECalculatorFactory,
                 num_workers: int) -> None:
        self.repository = repository
        self.task_queue: Queue[Job] = Queue()
        self.message_queue: Queue[Job] = Queue()

        self._workers: list[RelaxationWorker] = []

        self._shutdown_flag = False

        for i, _ in enumerate(range(num_workers), start=1):
            logger.info(f"Starting worker {i}/{num_workers}")
            worker = RelaxationWorker(calculator_factory, self.task_queue, self.message_queue)
            worker.start()
            self._workers.append(worker)

        logger.info("Workers started")

        self._message_listener = self._start_message_listener()

    def create_job(self,
                   material_id: str,
                   fmax: float,
                   max_steps: int,
                   mpr_api_key: str) -> Job:
        job_id = str(uuid.uuid4())

        logger.info(f"Creating new job for material {material_id} (job {job_id})")
        structure = self.fetch_structure(material_id, mpr_api_key)

        logger.info(f"Structure fetched for material {material_id} (job {job_id})")

        ase_atoms = AseAtomsAdaptor.get_atoms(structure)

        job: Job = {
            "id": job_id,
            "fmax": fmax,
            "max_steps": max_steps,
            "chemical_formula": ase_atoms.get_chemical_formula(),
            "atoms": ase_atoms.todict(),
            "atoms_slab": self.make_slab(ase_atoms).todict(),
            "status": JobStatus.PENDING,
            "progress": 0.0,
            "energies": [],
            "forces": [],
        }

        self.repository.create(job)
        logger.info(f"Job created in repository (job {job_id})")

        self.task_queue.put(job)
        logger.info(f"Job added to processing queue (job {job_id})")

        return job

    def get_job(self, job_id: str) -> Job:
        logger.info(f"Retrieving the job (job {job_id})")
        return self.repository.get(job_id)

    def _start_message_listener(self) -> threading.Thread:
        logger.info("Starting message listener")
        thread = threading.Thread(target=self._listen_for_updates, daemon=True)
        thread.start()
        return thread

    def _listen_for_updates(self) -> None:
        while not self._shutdown_flag:
            try:
                job = self.message_queue.get(timeout=5.0)
                self.repository.update(job)
            except queue.Empty:
                continue

    def shutdown(self) -> None:
        logger.info("Shutting down relaxation service")

        logger.info("Shutting message listener")
        self._shutdown_flag = True
        self._message_listener.join(timeout=10.0)
        logger.info("Message listener shut down")

        logger.info("Killing workers")
        for i, worker in enumerate(self._workers, start=1):
            logger.info(f"Killing worker {i}/{len(self._workers)}")
            # I'm too lazy to implement a proper shutdown mechanism here c:
            worker.kill()
        logger.info("Workers killed")

        logger.info("Relaxation service shut down")

    @classmethod
    def fetch_structure(cls, material_id: str, mpr_api_key: str) -> Structure:
        try:
            with MPRester(mpr_api_key) as mpr:
                docs = mpr.materials.summary.search(material_ids=[material_id], fields=["structure"])
        except ValueError as e:
            if "is not formatted correctly" in str(e):
                raise MaterialMalformedName from e

            if "Please use a new API key from" in str(e):
                raise ApiKeyMalformed from e

            logger.exception(f"Error fetching structure for material {material_id}: {e}")
            raise

        except MPRestError as e:
            if "status code 401" in str(e):
                raise ApiKeyOutdated from e

            logger.exception(f"Error fetching structure for material {material_id}: {e}")
            raise

        if not docs:
            raise MaterialNotFound(f"Material {material_id} not found")

        return cast(Structure, docs[0].structure)

    @staticmethod
    def make_slab(atoms: Atoms) -> Atoms:
        while len(atoms) < 30:
            atoms *= (1, 1, 2)

        cell = atoms.get_cell()
        cell[2, 2] += 20.0
        atoms.set_cell(cell)

        atoms.wrap()
        atoms.rattle(0.05)

        return atoms
