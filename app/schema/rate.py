from pydantic import BaseModel


class Rate(BaseModel):
    current_rate: float
    avg_volume: float

    class Config:
        orm_mode = True
