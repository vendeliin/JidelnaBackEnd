from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import delete
from models import User, Lunch
import schemas


def create_user(user: schemas.UserBase, db: Session):
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    for lunch in user.lunches:
        db_lunch = Lunch(type_of_lunch=lunch.type_of_lunch, owner_id=new_user.id)

        if int(db_lunch.type_of_lunch) > 3 or int(db_lunch.type_of_lunch) < 0:
            raise HTTPException(status_code=500, detail="Invalid type of lunch.")

        db.add(db_lunch)
    db.commit()

    return new_user.id


def update_lunch_for_user(user_id: int, type_of_lunch: int, db: Session):
    db.execute(delete(Lunch).where(Lunch.owner_id == user_id))

    # Check if the user exists
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new Lunch instance
    new_lunch = Lunch(type_of_lunch=type_of_lunch, owner_id=user_id)
    if int(new_lunch.type_of_lunch) > 3 or int(new_lunch.type_of_lunch) < 0:
        raise HTTPException(status_code=404, detail="Invalid type of lunch")

    # Add the new lunch to the database
    db.add(new_lunch)
    db.commit()
    db.refresh(new_lunch)
    return new_lunch.type_of_lunch


def get_user_by_id(db: Session, user_id: int):
    db_user: object = db.query(User).filter(User.id == user_id).options(joinedload(User.lunches)).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user