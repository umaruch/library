from datetime import datetime

from app.models import User, Book, Author
from app import db

def drop_table():
    db.drop_all()
    db.create_all()

    admin = User(username = "admin", password = "admin")
    db.session.add(admin)
    db.session.commit()
    print("DataBase created.")


def db_test():
    books = ['Seath Dtranding', 'Kira Fuka', 'JoJo Bizzare Adventure']
    authors = ['Hideo Kodjima', 'Xopoiiiuu', 'Pidor']
    dates = ['28-04-2010', '23-11-1998', '12-12-2012']

    for i in range(len(books)):
        db.session.add(Author(name = authors[i]))
        author_id = Author.query.get(i+1).id
        db.session.add(Book(name = books[i], date = dates[i], author_id = author_id ))
        db.session.commit()