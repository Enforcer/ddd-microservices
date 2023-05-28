from negotiations.events import NegotiationAccepted
from negotiations.repository import NegotiationsRepository


def on_negotiation_accepted(event: NegotiationAccepted) -> None:
    repository = NegotiationsRepository()
    other_negotiations = repository.get_pending_negotiations_for_item(
        item_id=event.item_id
    )
    for negotiation in other_negotiations:
        negotiation.cancel()
        repository.update(negotiation)
