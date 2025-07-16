import controller.SecurityController as security
import controller.DatabaseController as database 
from passlib.hash import pbkdf2_sha256
import sqlite3

def open_sqlite_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    return connection

passwd = input("Ingrese la clave a encriptar >> ")

hash_passwd = pbkdf2_sha256.hash(passwd)

print("Clave encriptada: ", hash_passwd)
