import controller.DatabaseController as database

async def update_evil_domains():
    connection = await open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM external_sources;
    """)

    list_result = [dict(fila) for fila in cursor.fetchall()]

    for fila in list_result:
        badlinks_request = requests.get(fila["link"])
        
        if badlinks_request.status_code == 200:
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
        else:
            message = f"Error: La siguiente fuente externa no funciona. ({fila['link']})"
            await alerts.insert_alert('Error', message, None)

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