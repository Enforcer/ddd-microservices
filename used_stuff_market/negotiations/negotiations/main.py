import abc

from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration

container = Container()


deps = FastApiIntegration(container)
# How to use it ☟
# https://lagom-di.readthedocs.io/en/stable/framework_integrations/#fastapi


# Example:
class AbstractClass(abc.ABC):
    @abc.abstractmethod
    def foo(self) -> None:
        pass


class ConcreteClass(AbstractClass):
    def __init__(self, name: str) -> None:
        self._name = name

    def foo(self) -> None:
        pass


# factory that passes arguments
container[AbstractClass] = lambda: ConcreteClass(name="123")  # type: ignore
# if no arguments are needed, just assign concrete class to abstract class
container[AbstractClass] = ConcreteClass  # type: ignore
