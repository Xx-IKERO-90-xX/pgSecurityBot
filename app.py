from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'fdsf435t34t3f34fw'


# Página principal
@app.route('/')
async def evil_domains():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    offset = (page - 1) * per_page

    connection = await database.open_sqlite_connection()
    cursor = connection.cursor()
    evil_domains = connection.execute("SELECT * FROM evil_domains LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    total_domains = connection.execute("SELECT COUNT(*) FROM evil_domains").fetchone()[0]
    
    total_pages = (total_domains + per_page - 1) // per_page
    
    connection.close()

    return render_template(
        "index.jinja",
        domains=evil_domains,
        page=page,
        total_domains=total_domains,
        total_pages=total_pages
    )


@app.route('/sources')
async def sources():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    offset = (page - 1) * per_page

    connection = await database.open_sqlite_connection()
    external_sources = connection.execute("SELECT * FROM external_sources LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    total_domains = connection.execute("SELECT COUNT(*) FROM external_sources").fetchone()[0]
    
    total_pages = (total_domains + per_page - 1) // per_page
    
    connection.close()

    return render_template(
        "sources.jinja",
        sources=external_sources,
        page=page,
        total_domains=total_domains,
        total_pages=total_pages
    )

@app.route('/sources/new', methods=['POST'])
async def new_source():
    source = request.form['new_source']
    
    try:
        await database.insert_new_source(source)
    except e:
        print("Fallo con la subida de la nueva fuente externa")
    
    return redirect(url_for('sources'))

@app.route('/sources/delete/<int:id>', methods=["GET"])
async def delete_source(id):
    await database.delete_external_source(id)
    return redirect(url_for('sources'))

@app.route('/evildomains/reload', methods=["GET"])
async def reload_evil_domains():
    await database.update_evil_domains()
    return redirect(url_for('evil_domains'))
    


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )