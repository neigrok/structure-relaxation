from typing import Any

import torch
from mace.calculators import MACECalculator, mace_mp


_DEFAULT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class MACECalculatorFactory:
    """
    MACECalculator should be created in each process to avoid serialization issues.

    Since we pass the factory between processes,
        we have to redefine __getstate__ and __setstate__ to avoid serialization issues.
    """
    def __init__(self, model: str, device: str = _DEFAULT_DEVICE):
        self.model = model
        self.device = device

    def create(self) -> MACECalculator:
        return mace_mp(
            model=self.model,
            dispersion=False,
            default_dtype="float64",
            device=self.device
        )

    def __getstate__(self) -> dict[str, str]:
        return {"model": self.model, "device": self.device}

    def __setstate__(self, state: dict[str, str]) -> None:
        self.__init__(**state)  # type: ignore[misc]
