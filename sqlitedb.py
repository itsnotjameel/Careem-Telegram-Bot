import sqlite3
import platform
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



def checkifsamedetails(user_id, goodphonenum, goodpassword):
    startsqlite()
    c.execute(f"""SELECT ID, Phone, Password FROM users WHERE ID ={user_id} AND Phone ={goodphonenum} AND Password ='{goodpassword}'   """)
    if c.fetchone() != None:
        return True
    else:
        return False
    endsqlite()

def checkifregistered(user_id):
    startsqlite()
    c.execute(f"""SELECT Phone, Password FROM users WHERE ID ={user_id}""")
    checkifregisteredinfo = c.fetchone()
    if checkifregisteredinfo != None and len(checkifregisteredinfo) == 2:
        global savednumber
        savednumber = checkifregisteredinfo[0]
        global savedpassword
        savedpassword = checkifregisteredinfo[1]
        endsqlite()
        return True
    else:
        endsqlite()
        return False
    

def replacedata(user_id, goodphonenum, goodpassword):
    startsqlite()
    c.execute(f"""DELETE FROM users WHERE ID == {user_id}""")
    c.execute(f"""INSERT INTO users VALUES ({user_id}, {goodphonenum}, '{goodpassword}')""")
    endsqlite()

def enternewdata(user_id, goodphonenum, goodpassword):
    startsqlite()
    c.execute(f"""INSERT INTO users VALUES ({user_id}, {goodphonenum}, '{goodpassword}')""")
    print(c.fetchone())
    endsqlite()

def deleteeverything():
    startsqlite()
    while True:
        password = input("What's the password?")
        if password == deletepassword:
            c.execute(f"""DELETE FROM users""")
            break
        else:
            print("Wrong password!")
    endsqlite()

def endsqlite():
    conn.commit()
    conn.close()
