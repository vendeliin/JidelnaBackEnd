from fastapi import FastAPI, Depends
import schemas
from models import Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import crud
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create/user/")
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return crud.create_user(user=user, db=db)


@app.put("/users/{user_id}/update-lunch/{lunch_id}")
async def update_user_lunch(user_id: int, type_of_lunch, db: Session = Depends(get_db)):
    return crud.update_lunch_for_user(user_id=user_id, type_of_lunch=type_of_lunch, db=db)


@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id=user_id)


@app.get("/")
async def def_func():
    return {"message": "Hello"}
