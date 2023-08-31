# project_classes.py

from sqlalchemy import Column, String
from ddopy.db.model.base import Base


class EndpointUrl(Base):
    __tablename__ = 'endpoint_urls'

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)

    def update_from(self, other):
        if other.url:
            self.url = other.url
