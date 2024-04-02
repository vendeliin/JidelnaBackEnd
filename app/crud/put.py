from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import User, Lunch


def update_lunch_for_user(user_name: str, type_of_lunch: int, db: Session):
    db_user = db.query(User).filter(User.name == user_name).first()

    existing_lunch = db.query(Lunch).filter(Lunch.owner_id == db_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_lunch:
        if int(type_of_lunch) > 3 or int(type_of_lunch) < 0:
            raise HTTPException(status_code=404, detail="Invalid type of lunch")
        existing_lunch.type_of_lunch = type_of_lunch
        existing_lunch.lunch_out = 0
    else:
        # If the user doesn't have an existing lunch, create a new one
        new_lunch = Lunch(type_of_lunch=type_of_lunch, owner_id=db_user.id)
        if int(new_lunch.type_of_lunch) > 3 or int(new_lunch.type_of_lunch) < 0:
            raise HTTPException(status_code=404, detail="Invalid type of lunch")

        db.add(new_lunch)

    # Commit changes to the database
    db.commit()
    return True

def update_lunch_for_users_with_no_lunch(db: Session, user_name: str):
    db_user = db.query(User).filter(User.name == user_name).first()

    existing_lunch = db.query(Lunch).filter(Lunch.owner_id == db_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_lunch:
        existing_lunch.type_of_lunch = 0
        existing_lunch.lunch_out = 0
    else:
        # If the user doesn't have an existing lunch, create a new one
        new_lunch = Lunch(owner_id=db_user.id)
        if int(new_lunch.type_of_lunch) > 3 or int(new_lunch.type_of_lunch) < 0:
            raise HTTPException(status_code=404, detail="Invalid type of lunch")

        db.add(new_lunch)

    # Commit changes to the database
    db.commit()