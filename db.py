import sqlite3
import os
from flask import Flask, render_template, request, g, flash
from FDataBase import FDataBase

DATABASE = '/tmp/db.db'
DEBUG = True
SECRET_KEY = 'LKFPWIF092342342SDFS'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE = os.path.join(app.root_path,'db.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route('/')
def index():
    db = get_db()
    dbase =FDataBase(db)
    return render_template('main_page.html', menu = dbase.getMenu())

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/add_post', method = ['GET','POST'])
def add_Post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Post add error', category='error')
            else:
                flash ('Post added', category='success')
        else:
            flash ('Post add error', category='error')
    return render_template('create.html', menu = dbase.getMenu(), title = 'Post add')
if __name__ == "__main__":
    app.run(debug=True)


