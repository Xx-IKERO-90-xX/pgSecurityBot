import controller.DatabaseController as database

async def get_users():
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users;")

    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results

async def get_user_by_name(username):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT * FROM users
        WHERE username = '{username}';
    """)

    result = [dict(fila) for fila in cursor.fetchall()]

    connection.close()
    return result[0]