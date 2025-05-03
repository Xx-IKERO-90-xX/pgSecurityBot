from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'fdsf435t34t3f34fw'


# Página principal
@app.route('/')
async def index():
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

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )