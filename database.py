import sqlite3
import requests

async def open_sqlite_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    return connection

async def insert_new_source(link):
    connection = await open_sqlite_connection()
    cursor = connection.cursor()
    
    cursor.execute(f"""
        INSERT INTO external_sources (link)
        VALUES ('{link}');
    """)

    connection.commit()

async def update_evil_domains():
    connection = await open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM external_sources;
    """)

    list_result = [dict(fila) for fila in cursor.fetchall()]

    for fila in list_result:
        badlinks_request = requests.get(fila["link"])
        badlinks = badlinks_request.text.strip().splitlines()

        for line in badlinks:
            try:
                cursor.execute(f"""
                    INSERT INTO evil_domains (domain)
                    VALUES ('{line}');
                """)
            except:
                pass
        connection.commit()
    
    connection.close()

async def get_evil_domains():
    connection = await open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM evil_domains;
    """)
    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results

async def get_external_sources():
    connection = await open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM external_sources;
    """)
    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results

async def delete_external_source(id):
    connection = await open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        DELETE FROM external_sources
        WHERE id = '{id}'
    """)

    connection.commit()
    connection.close()