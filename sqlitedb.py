import sqlite3
from secret_tokens import deletepassword



def startsqlite():
    global conn
    conn = sqlite3.connect("telegram_bot_users.db")
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
    c.execute(f"""SELECT Phone FROM users WHERE ID == {user_id}""")
    print(c.fetchone())
    if c.fetchone() != None:
        global savednumber
        savednumber = c.fetchone()
        c.execute(f"""SELECT Password FROM users WHERE ID =={user_id}""")
        if c.fetchone() != None:
            c.execute(f"""SELECT Password FROM users WHERE ID == {user_id}""")
            global savedpassword
            savedpassword = c.fetchone()
            endsqlite()
            return True
        else:
            endsqlite()
            return False
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
