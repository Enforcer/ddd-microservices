from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from negotiations.app.repository import NegotiationsRepository, NotFound
from negotiations.domain.negotiation import Negotiation, Status


class SqlAlchemyNegotiationsRepository(NegotiationsRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def pending_for_item(self, item_id: int, buyer_id: int) -> Negotiation:
        stmt = select(Negotiation).filter(
            Negotiation._item_id == item_id,
            Negotiation._buyer_id == buyer_id,
            Negotiation._status == Status.PENDING,
        )
        result = self._session.execute(stmt)
        try:
            return result.scalars().one()
        except NoResultFound:
            raise NotFound

    def add(self, negotiation: Negotiation) -> None:
        self._session.add(negotiation)
        self._session.flush([negotiation])
