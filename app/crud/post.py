from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.models import User, Lunch
from app.schemas import schemas


def create_user(user: schemas.UserBase, db: Session):
    db_user = db.query(User).filter(User.id == user.id).options(joinedload(User.lunches)).first()

    if db_user:
        raise HTTPException(status_code=500, detail="User already exists")

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db_lunch = Lunch(type_of_lunch=0, owner_id=new_user.id)

    if int(db_lunch.type_of_lunch) > 3 or int(db_lunch.type_of_lunch) < 0:
        raise HTTPException(status_code=500, detail="Invalid type of lunch.")

    db.add(db_lunch)
    db.commit()
    return new_user.name
