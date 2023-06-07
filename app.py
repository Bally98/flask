from flask import Flask, render_template, request,flash, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), primary_key = False)
    intro = db.Column(db.String(300), primary_key = False)
    text = db.Column (db.Text, nullable = False)
    date = db.Column (db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route("/")
def hello():
    return render_template('main_page.html')

@app.route("/test")
def test():
    return render_template('test.html')

@app.route('/bmw')
def bmw():
    return render_template('bmw.html')

@app.route('/mercedes')
def mercedes():
    return render_template('mercedes.html')

@app.route('/audi')
def audi():
    return render_template('audi.html')

@app.route('/main')
def main():
    return render_template('main_page.html')

@app.route('/posts/<int:id>/update', methods = ['POST', 'GET'])
def update(id):
    article = Article.query.get (id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Error'
    else:
        return render_template('post_update.html', article=article)

@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title = title, intro = intro, text = text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            'Error'
    else:
        return render_template('create.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles = articles)

@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_det.html', article = article)

@app.route('/posts/<int:id>/del')
def del_post(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Error'

@app.errorhandler(404)
def PageNotFound(error):
    return render_template('page404.html', title = 'Page not found')

def user(username):
    return f'Username is {username}'
if __name__ == "__main__":
    app.run(debug=False, host = '0.0.0.0')
