import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base


class RateOrm(Base):
    __tablename__ = 'rate'
    id = sa.Column(sa.Integer, primary_key=True)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey('currency.id'))
    date = sa.Column(sa.Date, nullable=False)
    rate = sa.Column(sa.Float, nullable=False)
    volume = sa.Column(sa.Float, nullable=False)

    currency = relationship("Currency", back_populates="rate")
