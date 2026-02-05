from dishka import make_async_container

from .infrastructure import InfrastructureProvider


container = make_async_container(
    InfrastructureProvider(),
)