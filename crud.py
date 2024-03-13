from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from models import User, Lunch, AdminUser
import schemas
def create_user(user: schemas.UserBase, db: Session):
    new_user = User(id=user.id, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db_lunch = Lunch(type_of_lunch=0, owner_id=new_user.id)

    if int(db_lunch.type_of_lunch) > 3 or int(db_lunch.type_of_lunch) < 0:
        raise HTTPException(status_code=500, detail="Invalid type of lunch.")

    db.add(db_lunch)
    db.commit()
    return new_user.id

def create_admin_user(user: schemas.AdminUserBase, db: Session):
    admin_user = AdminUser(**user.dict())
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return admin_user.name

def login(user:schemas.AdminUserBase, db: Session):
    db_user = db.query(AdminUser).filter(AdminUser.name==user.name, AdminUser.password==user.password).first()
    return True if db_user else False
def update_lunch_for_user(user_id: str, type_of_lunch: int, db: Session):
    existing_lunch = db.query(Lunch).filter(Lunch.owner_id == user_id).first()

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_lunch:
        existing_lunch.type_of_lunch = type_of_lunch
        existing_lunch.lunch_out = 0
    else:
        # If the user doesn't have an existing lunch, create a new one
        new_lunch = Lunch(type_of_lunch=type_of_lunch, owner_id=user_id)
        if int(new_lunch.type_of_lunch) > 3 or int(new_lunch.type_of_lunch) < 0:
            raise HTTPException(status_code=404, detail="Invalid type of lunch")

        db.add(new_lunch)

    # Commit changes to the database
    db.commit()
def get_user_by_id(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).options(joinedload(User.lunches)).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")


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
def get_all_users(db: Session):
    db_users = db.query(User).filter(
        and_ (
            or_(
                User.lunches.any(lunch_out=1),
                User.lunches.any(lunch_out=2),
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
def delete_all_users(db: Session):
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