from fastapi import FastAPI, Depends
import schemas
from models import Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from crudTypes import putCrud, getCrud, deleteCrud, postCrud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Base.metadata.create_all(engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=['*']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create/user")
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return postCrud.create_user(user=user, db=db)


@app.post("/login")
async def login(user: schemas.AdminUserBase, db: Session = Depends(get_db)):
    return postCrud.login(user=user, db=db)


@app.post("/create/admin")
async def create_admin(user: schemas.AdminUserBase, db: Session = Depends(get_db)):
    return postCrud.create_admin_user(user=user, db=db)


@app.put("/user/{user_name}/update-lunch/{lunch_id}")
async def update_user_lunch(user_name: str, type_of_lunch, db: Session = Depends(get_db)):
    return putCrud.update_lunch_for_user(user_name=user_name, type_of_lunch=type_of_lunch, db=db)


@app.put("/user/{user_name}/null/lunch")
async def null_user_lunch(user_name: str, db: Session = Depends(get_db)):
    return putCrud.update_lunch_for_users_with_no_lunch(user_name=user_name, db=db)


@app.get("/user/{user_id}")
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return getCrud.get_user_by_id(db=db, user_id=user_id)


@app.get("/users/WithLunchOut")
async def get_users_with_lunch_out(db: Session = Depends(get_db)):
    return getCrud.get_all_users_with_lunch_out(db=db)


@app.get("/users/All")
async def get_users(db: Session = Depends(get_db)):
    return getCrud.get_all_users_who_have_lunch(db=db)

@app.get("/users/count")
async def get_count_of_users(db: Session = Depends(get_db)):
    return getCrud.get_count_of_users(db=db)


@app.get("/lunches/count/rest")
async def get_lunches_count_rest(db: Session = Depends(get_db)):
    return getCrud.get_count_of_lunches_rest(db=db)


@app.get("/user/name/{user_id}")
async def get_user_name(user_id: str, db: Session = Depends(get_db)):
    return getCrud.get_user_name_by_id(user_id=user_id, db=db)


@app.get("/lunches/count/out")
async def get_lunches_count_out(db: Session = Depends(get_db)):
    return getCrud.get_count_of_lunches_out(db=db)


@app.delete("/users/delete")
async def delete_users(db: Session = Depends(get_db)):
    return deleteCrud.delete_all_users(db=db)


@app.delete("/user/delete/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    return deleteCrud.delete_user(user_id=user_id, db=db)

@app.delete("/user/delete/by/grade/{grade}")
async def delete_user_by_grade(grade: int, db: Session = Depends(get_db)):
    return deleteCrud.delete_users_by_grade(db=db, grade=grade)


