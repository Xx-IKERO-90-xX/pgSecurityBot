from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import controller.DatabaseController as DatabaseController
from flask_sqlalchemy import SQLAlchemy
import controller.AlertsController as alerts
import controller.SecurityController as security
import controller.UserController as users
import controller.EvilDomainsController as domains
import controller.SourcesController as sources

app = Flask(__name__)
app.secret_key = 'fdsf435t34t3f34fw'


# Página principal
@app.route('/')
async def index():
    if 'id' in session:
        alertas = await alerts.get_alerts()
        return render_template(
            'index.jinja',
            alerts=alertas
        )
    
    else:
        return redirect(url_for('login'))


@app.route('/sources')
async def sources():
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        per_page = 5

        offset = (page - 1) * per_page

        connection = await DatabaseController.open_sqlite_connection()
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
    
    else:
        return redirect(url_for('login'))

## SOURCES
@app.route('/sources/new', methods=['POST'])
async def new_source():
    if 'id' in session:
        source = request.form['new_source']
        await sources.insert_new_source(source)    
        return redirect(url_for('sources'))
    
    else:
        return redirect(url_for('login'))

@app.route('/sources/delete/<int:id>', methods=["GET"])
async def delete_source(id):
    if 'id' in session:
        await sources.delete_external_source(id)
        return redirect(url_for('sources'))
   
    else:
        return redirect(url_for('login'))

## DOMINIOS MALICIOSOS
@app.route('/evildomains')
async def evil_domains():
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        per_page = 10

        offset = (page - 1) * per_page

        connection = await DatabaseController.open_sqlite_connection()
        evil_domains = connection.execute("SELECT * FROM evil_domains LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
        total_domains = connection.execute("SELECT COUNT(*) FROM evil_domains").fetchone()[0]
    
        total_pages = (total_domains + per_page - 1) // per_page
    
        connection.close()

        return render_template(
            "evil_domains.jinja",
            domains=evil_domains,
            page=page,
            total_domains=total_domains,
            total_pages=total_pages
        )
    
    else:
        return redirect(url_for('login'))



@app.route('/evildomains/reload', methods=["GET"])
async def reload_evil_domains():
    if 'id' in session:
        await domains.update_evil_domains()
        return redirect(url_for('evil_domains'))
    
    else:
        return redirect(url_for('login'))



## AUTENTICACIÓN
@app.route('/auth/login', methods=["GET", "POST"])
async def login():
    if request.method == "GET":
        return render_template('login.jinja')

    else:
        username = request.form['username']
        passwd = request.form['passwd']

        user = await users.get_user_by_name(username)

        if user:
            if await security.check_login(username, passwd):
                session['id'] = user['id']
                session['username'] = user['username']

                return redirect(url_for('index'))

            else:
                error_msg = "El login ha fallado!!!"    
                return render_template(
                    'login.jinja', 
                    error_msg=error_msg
                )
        else:
            error_msg = "Usuario no encontrado."
            return render_template(
                'login.jinja',
                error_msg=error_msg
            )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
    )