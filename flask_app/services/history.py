from datetime import datetime

import sqlalchemy.orm

from database.db import engine
from database.db_models import History
from database.session_decorator import get_session


class HistoryService:
    def __init__(self):
        self.engine = engine

    @get_session()
    def create_history_record(
            self,
            user_id,
            user_agent,
            session: sqlalchemy.orm.Session = None
    ):
        user_info = History(
            user_id=user_id,
            user_agent=user_agent,
            auth_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        )
        session.add(user_info)
        session.commit()
