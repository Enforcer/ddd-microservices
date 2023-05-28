import pytest
from negotiations.negotiation import Negotiation
from negotiations.repository import NegotiationsRepository
from tests.factories import NegotiationFactory


@pytest.fixture()
def repo() -> NegotiationsRepository:
    return NegotiationsRepository()


@pytest.fixture()
def negotiation() -> Negotiation:
    return NegotiationFactory.build()


def test_saved_negotiation_can_be_retrieved(
    repo: NegotiationsRepository,
    negotiation: Negotiation,
) -> None:
    repo.insert(negotiation)

    read_negotiation = repo.get(
        item_id=negotiation.item_id,
        buyer_id=negotiation.buyer_id,
        seller_id=negotiation.seller_id,
    )

    assert read_negotiation == negotiation


def test_updating_not_existing_negotiation_raises_exception(
    repo: NegotiationsRepository,
    negotiation: Negotiation,
) -> None:
    with pytest.raises(NegotiationsRepository.NotFound):
        repo.update(negotiation)


def test_updates_negotation(
    repo: NegotiationsRepository, negotiation: Negotiation
) -> None:
    repo.insert(negotiation)

    try:
        repo.update(negotiation)
    except NegotiationsRepository.NotFound:
        pytest.fail("should not raise an exception")


def test_inserting_same_negotiation_twice_raises_exception(
    repo: NegotiationsRepository, negotiation: Negotiation
) -> None:
    repo.insert(negotiation)

    with pytest.raises(NegotiationsRepository.AlreadyExists):
        repo.insert(negotiation)


def test_raises_exception_when_negotiation_wasnt_saved_before(
    repo: NegotiationsRepository,
    negotiation: Negotiation,
) -> None:
    with pytest.raises(NegotiationsRepository.NotFound):
        repo.get(
            item_id=negotiation.item_id,
            buyer_id=negotiation.buyer_id,
            seller_id=negotiation.seller_id,
        )


def test_updating_negotiation_with_wrong_version_raises_exception(
    repo: NegotiationsRepository,
    negotiation: Negotiation,
) -> None:
    repo.insert(negotiation)

    one_instance = repo.get(
        item_id=negotiation.item_id,
        buyer_id=negotiation.buyer_id,
        seller_id=negotiation.seller_id,
    )
    second_instance = repo.get(
        item_id=negotiation.item_id,
        buyer_id=negotiation.buyer_id,
        seller_id=negotiation.seller_id,
    )

    repo.update(one_instance)

    with pytest.raises(NegotiationsRepository.OptimisticLockFailed):
        repo.update(second_instance)
