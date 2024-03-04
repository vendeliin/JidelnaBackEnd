from fastapi import FastAPI, Depends
import schemas
from models import Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import crud
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
Base.metadata.create_all(engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
async def update_user_lunch(user_id: str, type_of_lunch, db: Session = Depends(get_db)):
    return crud.update_lunch_for_user(user_id=user_id, type_of_lunch=type_of_lunch, db=db)


@app.get("/users/{user_id}")
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db=db, user_id=user_id)


@app.get("/users")
async def get_users_with_lunch_out(db: Session = Depends(get_db)):
    return crud.get_all_users_with_lunch_out(db=db)

@app.get("/usersAll")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)
@app.get("/")
async def def_func():
    return {"message": "Hello"}

@app.delete("/users/delete")
async def delete_user(db: Session = Depends(get_db)):
    return crud.delete_all_users(db=db)
