import io
import time
from multiprocessing import Process, Queue

from ase import Atoms
from ase.optimize.precon import PreconLBFGS
from mace.calculators import MACECalculator

from logger import logger
from utils.calculator_factory import MACECalculatorFactory
from .job import Job, JobStatus


class RelaxationWorker(Process):
    def __init__(self,
                 calculator_factory: MACECalculatorFactory,
                 task_queue: 'Queue[Job]',
                 message_queue: 'Queue[Job]') -> None:
        super().__init__()
        self.task_queue = task_queue
        self.message_queue = message_queue

        self.calculator_factory = calculator_factory

    def run(self) -> None:
        while True:
            try:
                calculator = self.calculator_factory.create()
                break
            except Exception as e:
                logger.exception(f"Error creating calculator: {e}")
                time.sleep(10)

        while True:
            job = self.task_queue.get()

            try:
                self._process_job(calculator, job)
            except Exception as e:
                job["status"] = JobStatus.FAILED
                job["progress"] = 100
                self.message_queue.put(job)

                logger.exception(f"Error occurred while processing: {e} (job {job['id']})")

    def _process_job(self, calculator: MACECalculator, job: Job) -> None:
        job_id = job["id"]
        fmax = job["fmax"]
        max_steps = job["max_steps"]

        logger.info(f"Processing job with fmax {fmax} and max_steps {max_steps} (job {job_id})")

        job["status"] = JobStatus.RUNNING
        self.message_queue.put(job)

        atoms = Atoms.fromdict(job["atoms_slab"])
        atoms.calc = calculator

        log_buffer = io.StringIO()

        optimizer = PreconLBFGS(
            atoms,
            logfile=log_buffer,
            precon='Exp',
            use_armijo=False
        )

        def callback(_: Atoms | None = None) -> None:
            """
            Callback is called after each optimization step,
                so we can steal energy and force from the log.

            Not optimal implementation, but looks fine for now
            """
            log_buffer.seek(0)
            last_line = log_buffer.readlines()[-1]

            log_parts = last_line.split()

            energy = float(log_parts[3])
            force = float(log_parts[4])

            job["energies"].append(energy)
            job["forces"].append(force)

            current_step = optimizer.get_number_of_steps() + 1
            progress = current_step / max_steps

            job["progress"] = progress

            logger.info(f"Step {current_step}/{max_steps} with energy {energy} and force {force} (job {job_id})")

            self.message_queue.put(job)

        optimizer.attach(callback)
        optimizer.run(fmax=fmax, steps=max_steps)

        logger.info(f"Optimization finished (job {job_id})")

        job["status"] = JobStatus.FINISHED
        job["progress"] = 1

        self.message_queue.put(job)
