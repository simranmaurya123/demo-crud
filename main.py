from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
   
@app.post("/users/")
def create_user(first_name: str, last_name: str, email: str, age: int, db: Session = Depends(get_db)):
    return crud.create_user(db, first_name, last_name, email, age)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

@app.put("/users/{user_id}")
def update_user(user_id: int, first_name: str, last_name: str, email: str, age: int, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, first_name, last_name, email, age)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)