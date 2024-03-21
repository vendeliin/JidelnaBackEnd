from pydantic import BaseModel
from typing import List


class LunchBase(BaseModel):
    type_of_lunch: int


class UserBase(BaseModel):
    id: str
    name: str
    grade: int
    lunches: List[LunchBase]


class AdminUserBase(BaseModel):
    password: str
    name: str
