from pydantic import BaseModel
from typing import List


class LunchBase(BaseModel):
    type_of_lunch: int


class UserBase(BaseModel):
    name: str
    lunches: List[LunchBase]