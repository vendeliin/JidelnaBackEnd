from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from models import User, Lunch, AdminUser
import schemas

def delete_all_users( db: Session):
    try:
        users = db.query(User).all()

        # Delete related lunch records for each user
        for user in users:
            db.query(Lunch).filter(Lunch.owner_id == user.id).delete(synchronize_session=False)

        # Delete all users
        db.query(User).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def delete_users_by_grade(db: Session, grade: int):
    try:
        users = db.query(User).filter(User.grade == grade).all()
        for user in users:
            db.query(Lunch).filter(Lunch.owner_id == user.id).delete(synchronize_session=False)
            db.query(User).filter(User.id == user.id).delete(synchronize_session=False)
        db.commit()
        return grade
    except Exception as e:
        db.rollback()
        raise e


def delete_user(user_id: str, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        lunch_of_user = db.query(Lunch).filter(Lunch.owner_id == user_id).first()
        db.delete(user)
        db.delete(lunch_of_user)
        db.commit()
        return user.name
    except Exception as e:
        db.rollback()
        raise e