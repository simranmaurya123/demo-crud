from sqlalchemy.orm import Session
from models import User

def create_user(db: Session, first_name: str, last_name: str, email: str, age: int):
    new_user = User(first_name=first_name, last_name=last_name, email=email, age=age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db:Session):
    return db.query(User).all()

def get_user(db:Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def update_user(db: Session, user_id: int, first_name: str,last_name: str, email: str, age: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.age = age
        db.commit()
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
