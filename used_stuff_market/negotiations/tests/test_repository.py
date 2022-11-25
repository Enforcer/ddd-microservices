import pytest
from negotiations.negotiation import Negotiation
from negotiations.repository import NegotiationsRepository


@pytest.fixture()
def repo() -> NegotiationsRepository:
    return NegotiationsRepository()


@pytest.fixture()
def negotiation() -> Negotiation:
    return Negotiation(item_id=1, seller_id=1, buyer_id=1)


def test_saved_negotiation_can_be_retrieved(
    repo: NegotiationsRepository,
    negotiation: Negotiation,
) -> None:
    repo.save(negotiation)

    read_negotiation = repo.get(
        item_id=negotiation.item_id,
        buyer_id=negotiation.buyer_id,
        seller_id=negotiation.seller_id,
    )

    assert read_negotiation == negotiation


def test_raises_exception_when_negotiation_not_found(
    repo: NegotiationsRepository,
) -> None:
    with pytest.raises(NegotiationsRepository.NotFound):
        repo.get(
            item_id=2,
            buyer_id=2,
            seller_id=2,
        )
