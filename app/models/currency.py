import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base


class CurrencyOrm(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(20), nullable=False)

    rate = relationship("Rate", back_populates="currency")

