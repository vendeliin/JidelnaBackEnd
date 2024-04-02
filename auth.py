from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import AdminUser
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.AdminUserBase):
    hashed_password = get_password_hash(user.password)
    db_user = AdminUser(name=user.name, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.name


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, user: schemas.AdminUserBase):
    db_user = db.query(AdminUser).filter(AdminUser.name == user.name).first()
    if not db_user:
        return "1"
    if not verify_password(user.password, db_user.password):
        return "2"
    return True



