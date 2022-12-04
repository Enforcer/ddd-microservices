from likes.db import ScopedSession
from likes.models import Like
from sqlalchemy.exc import IntegrityError


class Likes:
    def like(self, liker: int, item_id: int) -> None:
        session = ScopedSession()
        like = Like(item_id=item_id, liker=liker)
        session.add(like)
        try:
            session.flush()
        except IntegrityError:  # already have such a like
            session.rollback()
            return

    def unlike(self, liker: int, item_id: int) -> None:
        session = ScopedSession()
        session.query(Like).filter(
            Like.item_id == item_id, Like.liker == str(liker)
        ).delete()

    def count(self, item_id: int) -> int:
        session = ScopedSession()
        return session.query(Like).filter(Like.item_id == item_id).count()
