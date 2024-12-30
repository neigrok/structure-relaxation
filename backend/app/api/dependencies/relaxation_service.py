from typing import Annotated

from fastapi import Depends

from api.dependencies.get_container import ContainerDependency
from services.relaxation.service import RelaxationService


def _get_relaxation_service(container: ContainerDependency) -> RelaxationService:
    return container.relaxation_service


RelaxationServiceDependency = Annotated[RelaxationService, Depends(_get_relaxation_service)]
