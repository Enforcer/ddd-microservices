import mqlib
from likes.db import ScopedSession
from likes.models import Like
from sqlalchemy.exc import IntegrityError

from likes.queues import item_liked, item_unliked


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
        else:
            mqlib.publish(item_liked, {"item_id": item_id})

    def unlike(self, liker: int, item_id: int) -> None:
        session = ScopedSession()
        removed = session.query(Like).filter(
            Like.item_id == item_id, Like.liker == str(liker)
        ).delete()
        if removed > 0:
            mqlib.publish(item_unliked, {"item_id": item_id})

    def count(self, item_id: int) -> int:
        session = ScopedSession()
        return session.query(Like).filter(Like.item_id == item_id).count()
