from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# from data import Article, Author


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(255), nullable=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    articles = db.relationship('Article', backref='author')

@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/authors')
def authors():
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)

if __name__ == '__main__':
    app.run(debug=True)
