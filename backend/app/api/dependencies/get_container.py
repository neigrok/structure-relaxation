from typing import Annotated, cast

from fastapi import Depends
from starlette.requests import Request

from app import AppContainer


def _get_container(request: Request) -> AppContainer:
    return cast(AppContainer, request.app.state.container)


ContainerDependency = Annotated[AppContainer, Depends(_get_container)]
