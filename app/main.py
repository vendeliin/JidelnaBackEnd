from fastapi import FastAPI, Depends

from app.auth import auth
from app.schemas import schemas
from app.models.models import Base
from app.models.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.crud import get, post, put, delete
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    fastapi_app = FastAPI()
    Base.metadata.create_all(engine)
    origins = ["*"]
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=['*']
    )
    return fastapi_app


app = create_app()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users")
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return post.create_user(user=user, db=db)



@app.put("/users/{user_name}/lunches/{type_of_lunch}")
async def update_user_lunch(user_name: str, type_of_lunch: int, db: Session = Depends(get_db)):
    return put.update_lunch_for_user(user_name=user_name, type_of_lunch=type_of_lunch, db=db)


@app.get("/users/total")
async def get_users_count_rest(db: Session = Depends(get_db)):
    return get.get_count_of_users(db=db)


@app.get("/users/lunch")
async def get_users(db: Session = Depends(get_db)):
    return get.get_all_users_who_have_lunch(db=db)


@app.get("/users/{user_id}")
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return get.get_user_by_id(db=db, user_id=user_id)



@app.get("/users/{user_id}/name")
async def get_user_name(user_id: str, db: Session = Depends(get_db)):
    return get.get_user_name_by_id(user_id=user_id, db=db)


@app.get("/users/lunch/out")
async def get_users_with_lunch_out(db: Session = Depends(get_db)):
    return get.get_all_users_with_lunch_out(db=db)


@app.get("/lunches/rest/total")
async def get_lunches_count_rest(db: Session = Depends(get_db)):
    return get.get_count_of_lunches_rest(db=db)


@app.get("/lunches/out/total")
async def get_lunches_count_out(db: Session = Depends(get_db)):
    return get.get_count_of_lunches_out(db=db)


@app.post("/admins/login")
async def login(user: schemas.AdminUserBase, db: Session = Depends(get_db)):
    return auth.authenticate_user(user=user, db=db)


@app.post("/admins")
async def create_admin(user: schemas.AdminUserBase, db: Session = Depends(get_db)):
    return auth.create_admin_user(user=user, db=db)


@app.delete("/users")
async def delete_users(db: Session = Depends(get_db)):
    return delete.delete_all_users(db=db)


@app.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    return delete.delete_user(user_id=user_id, db=db)


@app.delete("/users/grade/{grade}")
async def delete_user_by_grade(grade: int, db: Session = Depends(get_db)):
    return delete.delete_users_by_grade(db=db, grade=grade)
