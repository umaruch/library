from app import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), nullable = False, unique = True, index = True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return f"<Login:{self.login}>"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, index = True, unique = True)
    date = db.Column(db.String(10), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete = 'cascade'))

    def __repr__(self):
        return f"<Book name: {self.name}, author: {self.author_id}>"

    @staticmethod
    def save(name, date, author_id):
        obj = Book(name = name, date = date, author_id = author_id)
        db.session.add(obj)
        db.session.commit()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    books = db.relationship('Book', backref = 'author', lazy = 'dynamic', cascade = "all, delete, delete-orphan", passive_deletes = True)

    def __repr__(self):
        return f"Author name:{self.name}"

    @staticmethod
    def save(name):
        obj = Author(name = name)
        db.session.add(obj)
        db.session.commit()
