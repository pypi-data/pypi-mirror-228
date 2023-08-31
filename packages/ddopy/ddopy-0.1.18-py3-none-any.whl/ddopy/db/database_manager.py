"""
Database manager module.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from ddopy.db.model.base import Base


class DatabaseManager:
    def __init__(self, db_url):
        self._engine = create_engine(db_url, echo=False)
        self._session_maker = sessionmaker(bind=self._engine)
        self._active_session = None

        Base.metadata.create_all(self._engine)

    def set(self, obj):
        try:
            existing_obj = self._get_session().merge(obj)
        except NoResultFound:
            existing_obj = None

        if existing_obj is not None:
            existing_obj.update_from(obj)
        else:
            self._get_session().add(obj)

        self._commit_session()

    def get(self, obj):
        return self._get_session().query(obj).first()

    def _get_session(self):
        if self._active_session is None:
            self._active_session = self._session_maker()
        return self._active_session

    def _commit_session(self):
        if self._active_session is not None:
            self._active_session.commit()
