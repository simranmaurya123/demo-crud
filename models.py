from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class User(Base):
    __tablename__="users"
    
    user_id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String(255))
    last_name=Column(String(255))
    email=Column(String(100),unique=True)
    age=Column(Integer)
    
    
