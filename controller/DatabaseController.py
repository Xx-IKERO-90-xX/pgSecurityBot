import sqlite3
import requests
import controller.AlertsController as alerts

async def open_sqlite_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    return connection

