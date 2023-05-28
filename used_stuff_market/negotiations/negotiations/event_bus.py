import inspect
from typing import Type, TypeAlias, Any, Callable
from collections import defaultdict


Listener: TypeAlias = Callable[[Any], None]


class EventBus:
    """
    Simple, in-memory event-bus. Mostly copy-pasted from pybuses library.

    1. Define event as e.g. dataclass or pydantic model

    class DinnerIsServed(BaseModel):
        waiter_wished_bon_appetit: bool = False

    2. Define listener as either:
        - function with single argument annotated with event type

        def on_dinner_is_served_function(event: DinnerIsServed) -> None:
            ...  # logic inside

        - method with single argument annotated with event type

        class RestaurantVisit:
            def on_dinner_is_served_method(self, event: DinnerIsServed) -> None:
                ...  # logic inside

    3. Subscribe listener to event bus

    from event_bus import event_bus
    event_bus.subscribe(on_dinner_is_served_function)
    event_bus.subscribe(RestaurantVisit().on_dinner_is_served_method)

    """

    def __init__(self) -> None:
        self._listeners: dict[Type, list[Listener]] = defaultdict(list)

    def subscribe(self, listener: Listener) -> None:
        event = self._get_subscribed(listener)
        self._listeners[event].append(listener)

    @staticmethod
    def _get_subscribed(listener: Listener) -> Type:
        arg_spec = inspect.getfullargspec(listener)
        if inspect.ismethod(listener):
            allowed_args_len = 2
        else:
            allowed_args_len = 1
        if len(arg_spec.args) != allowed_args_len:
            raise ValueError(f"{listener} is not accepting a single argument!")

        annotated_arg = arg_spec.annotations.get(arg_spec.args[-1])
        return annotated_arg  # type: ignore

    def post(self, event: Any) -> None:
        event_class = type(event)
        for listener in self._listeners[event_class]:
            listener(event)


event_bus = EventBus()
