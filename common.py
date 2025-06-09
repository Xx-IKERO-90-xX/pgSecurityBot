import controller.SecurityController as security
import controller.DatabaseController as database 
from passlib.hash import pbkdf2_sha256
import sqlite3

def open_sqlite_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    return connection

passwd = 'admin123'

hash_passwd = pbkdf2_sha256.hash(passwd)

connection = open_sqlite_connection()
cursor = connection.cursor()

cursor.execute(f"""
    UPDATE users
        set password = '{hash_passwd}' 
    WHERE username = 'admin';   
""")

connection.commit()
connection.close()