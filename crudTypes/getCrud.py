from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from models import User, Lunch

def get_user_by_id(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).options(joinedload(User.lunches)).first()

    if not db_user:
        return 0


    existing_lunch = db.query(Lunch).filter(Lunch.owner_id == user_id).first()

    if existing_lunch:
        if existing_lunch.lunch_out == 0:
            existing_lunch.lunch_out = 1
        elif existing_lunch.lunch_out == 1:
            existing_lunch.lunch_out = 2

        try:
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update lunch_out")

    return db_user


def get_all_users_with_lunch_out(db: Session):
    db_users = db.query(User).filter(User.lunches.any(lunch_out=2)).options(joinedload(User.lunches)).all()

    if not db_users:
        return 0
    return db_users


def get_all_users_who_have_lunch(db: Session):
    db_users = db.query(User).filter(
        and_(
            or_(
                User.lunches.any(lunch_out=1),
                User.lunches.any(lunch_out=2)
            ),
            or_(
                User.lunches.any(type_of_lunch=1),
                User.lunches.any(type_of_lunch=2),
                User.lunches.any(type_of_lunch=3)
            )
        )
    ).options(joinedload(User.lunches)).all()

    if not db_users:
        return 0
    return db_users


def get_count_of_users(db: Session):
    users_count = db.query(User).count()
    return users_count

def get_count_of_lunches_rest(db: Session):
    count_of_lunches_all = db.query(Lunch).filter(Lunch.type_of_lunch > 0).count()
    count_of_lunches_out = db.query(Lunch).filter(Lunch.lunch_out > 0, Lunch.type_of_lunch>0).count()
    return count_of_lunches_all - count_of_lunches_out


def get_count_of_lunches_out(db: Session):
    count_of_lunches_out = db.query(Lunch).filter(Lunch.lunch_out > 0, Lunch.type_of_lunch>0).count()
    return count_of_lunches_out

def get_user_name_by_id(user_id: str, db: Session):
    user_name = db.query(User).filter(User.id == user_id).first()
    return user_name.name