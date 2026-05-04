import psycopg2
from dotenv import load_dotenv
import os

#load environment variables from .env file

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_User"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    
# test the connection

if __name__== "__main__":
    conn=get_connection()
    print("Connection succesful")
    conn.close()