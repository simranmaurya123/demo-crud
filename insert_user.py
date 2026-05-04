from db_connect import get_connection

def insert_user(first_name,last_name,email,age):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute(
        "INSERT INTO users(first_name,last_name,email,age) VALUES(%s,%s,%s,%s)",
        (first_name, last_name, email, age)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("User added successfully")
    
 
if __name__ == "__main__":
    first_name=input("Enter first name: ")
    last_name=input("Enter last name: ")
    email=input("Enter email: ")
    age=int(input("Enter age: "))

    insert_user(first_name,last_name,email,age)
