from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

    # Define the relationship between User and Lunch
    lunches = relationship("Lunch", back_populates="user")


class Lunch(Base):
    __tablename__ = 'lunches'

    id = Column(Integer, primary_key=True, index=True)
    type_of_lunch = Column(Integer, default=0)
    lunch_out = Column(Boolean, default=False)

    owner_id = Column(String, ForeignKey("users.id"))

    # Define the reverse relationship from Lunch to User
    user = relationship("User", back_populates="lunches")