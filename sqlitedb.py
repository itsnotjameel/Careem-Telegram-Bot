import sqlite3
import platform
from functools import wraps
from back_or_forward_slash import back_or_forward_slash
from secret_tokens import dbpath, dbname, deletepassword





def startsqlite():
    global conn
    conn = sqlite3.connect(back_or_forward_slash(dbpath, dbname))
    global c
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
	ID INTEGER,
   	Phone INTEGER,
	Password TEXT
    )""")

def endsqlite():
    conn.commit()
    conn.close()

def start_and_end(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        startsqlite()
        fn(*args, **kwargs)
        endsqlite()
    return wrapper

@start_and_end
def checkifsamedetails(user_id, goodphonenum, goodpassword):    
    c.execute(f"""SELECT ID, Phone, Password FROM users WHERE ID ={user_id} AND Phone ={goodphonenum} AND Password ='{goodpassword}'   """)
    if c.fetchone() != None:
        return True
    else:
        return False
    
@start_and_end
def checkifregistered(user_id):
    c.execute(f"""SELECT Phone, Password FROM users WHERE ID ={user_id}""")
    checkifregisteredinfo = c.fetchone()
    if checkifregisteredinfo != None and len(checkifregisteredinfo) == 2:
        global savednumber
        savednumber = checkifregisteredinfo[0]
        global savedpassword
        savedpassword = checkifregisteredinfo[1]
        return True
    else:
        return False
    
@start_and_end
def replacedata(user_id, goodphonenum, goodpassword):
    c.execute(f"""DELETE FROM users WHERE ID == {user_id}""")
    c.execute(f"""INSERT INTO users VALUES ({user_id}, {goodphonenum}, '{goodpassword}')""")

@start_and_end
def enternewdata(user_id, goodphonenum, goodpassword):
    c.execute(f"""INSERT INTO users VALUES ({user_id}, {goodphonenum}, '{goodpassword}')""")

@start_and_end
def deleteeverything():
    while True:
        password = input("What's the password?")
        if password == deletepassword:
            print("Correct password, executing...")
            c.execute(f"""DELETE FROM users""")
            print("Deleted all items successfully.")
            break
        else:
            print("Wrong password!")