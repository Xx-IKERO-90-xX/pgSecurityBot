import controller.DatabaseController as database
import requests
import controller.AlertsController as alerts

async def update_evil_domains():
    await alerts.clear_external_sources_alerts()

    connection = await database.open_sqlite_connection()
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
            message = f"La siguiente fuente externa no funciona. ({fila['link']})"
            await alerts.insert_alert('Error', 'EXTERNAL_SOURCES', message, None)

    connection.close()


async def get_evil_domains():
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM evil_domains;
    """)
    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results


async def add_evil_domain(domain):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"""
            INSERT INTO evil_domains (domain)
            VALUES ('{domain}');
        """)
    except:
        connection.close()
        return "Failed"

    connection.commit()
    connection.close()

    return "Ok"


async def get_filtered_domains(text):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT * FROM evil_domains
        WHERE domain LIKE %{text}%;
    """)

    results = [dict(fila) for fila in cursor.fetchall()]
    connection.close()

    return results

async def delete_evil_domain(domain):
    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        DELETE FROM evil_domains
        WHERE domain = '{domain}';
    """)
    connection.commit()
    connection.close()