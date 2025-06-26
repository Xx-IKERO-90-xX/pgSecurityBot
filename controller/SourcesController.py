import controller.DatabaseController as database

async def insert_new_source(link):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()
    
    cursor.execute(f"""
        INSERT INTO external_sources (link)
        VALUES ('{link}');
    """)

    connection.commit()

async def get_external_sources():
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM external_sources;
    """)
    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results

async def delete_external_source(id):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        DELETE FROM external_sources
        WHERE id = '{id}';
    """)

    connection.commit()
    connection.close()