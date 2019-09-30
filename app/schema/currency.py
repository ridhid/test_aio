from typing import List

from pydantic import BaseModel, constr


class Currency(BaseModel):
    id: int
    name: constr(max_length=20) = ''

    class Config:
        orm_mode = True


class CurrencyList(BaseModel):
    currencies: List[Currency]
