import controller.DatabaseController as database


async def get_alerts():
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM alerts;")

    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results

async def insert_alert(type, message, status):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(f'''
        INSERT INTO alerts (type, message, status)
        VALUES ("{type}", "{message}", "{status}");
    ''')

    connection.commit()
    connection.close()
    

