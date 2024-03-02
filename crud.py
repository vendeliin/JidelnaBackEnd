from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import delete
from models import User, Lunch
import schemas



def create_user(user: schemas.UserBase, db: Session):
    new_user = User(id=user.id, name=user.name)
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
def update_lunch_for_user(user_id: str, type_of_lunch: int, db: Session):
    # Retrieve the existing lunch for the user
    existing_lunch = db.query(Lunch).filter(Lunch.owner_id == user_id).first()

    # Check if the user exists
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_lunch:
        existing_lunch.type_of_lunch = type_of_lunch
        existing_lunch.lunch_out = False
    else:
        # If the user doesn't have an existing lunch, create a new one
        new_lunch = Lunch(type_of_lunch=type_of_lunch, owner_id=user_id)
        if int(new_lunch.type_of_lunch) > 3 or int(new_lunch.type_of_lunch) < 0:
            raise HTTPException(status_code=404, detail="Invalid type of lunch")

        db.add(new_lunch)

    # Commit changes to the database
    db.commit()

    # If a new lunch was created, return its type_of_lunch
    if not existing_lunch:
        return new_lunch.lunch_out
    else:
        # If an existing lunch was updated, return its type_of_lunch
        return existing_lunch.lunch_out
def get_user_by_id(db: Session, user_id: str):
    db_user: object = db.query(User).filter(User.id == user_id).options(joinedload(User.lunches)).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user_copy = copy.deepcopy(db_user)

    existing_lunch = db.query(Lunch).filter(Lunch.owner_id == user_id).first()
    if not existing_lunch.lunch_out:
        existing_lunch.lunch_out = True

    return db_user_copy


def delete_all_users(db: Session):
    try:
        # Fetch all users
        users = db.query(User).all()

        # Delete related lunch records for each user
        for user in users:
            db.query(Lunch).filter(Lunch.owner_id == user.id).delete(synchronize_session=False)

        # Delete all users
        db.query(User).delete()

        # Commit the changes
        db.commit()
    except Exception as e:
        # Rollback the transaction if an error occurs
        db.rollback()
        raise e