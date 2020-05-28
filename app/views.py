from flask import redirect, url_for, render_template, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required


from app import app, lm, db
from app.models import User, Book, Author
from app.forms import LoginRegisterForm, BookForm, AuthorForm

##################      USER
@lm.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('books'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginRegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        user = User.query.filter_by(username = name).first()
        if user:
            if user.password == password:
                login_user(user, True)
                return redirect(url_for("books"))    
    return render_template(
        'login.html',
        title = 'Вход',
        form = form  
    )


########                Books
@app.route('/')
@app.route('/books')
def books():
    table_titles = ['Функции','Название', 'Дата', 'Автор']
    return render_template(
        'index.html',
        title = "Книги",
        titles = table_titles,
        url = url_for('load_books'),
        add_url = url_for('add_book')
    )

@app.route('/books/get')
def load_books():
    books = []
    try:
        text = request.args['search']
        all_books = db.engine.execute(f"select * from book where name like '%{text}%'")
        for book in all_books:
            el = []
            el.append(url_for('delete_book', book_id = book.id))
            el.append(url_for('change_book', book_id = book.id))
            el.append(book.name)
            el.append(book.date)
            el.append(Author.query.get(book.author_id).name)
            books.append(el)
    except:
        all_books = Book.query.all()
        for book in all_books:
            el = []
            el.append(url_for('delete_book', book_id = book.id))
            el.append(url_for('change_book', book_id = book.id))
            print(book.name)
            el.append(book.name)
            el.append(book.date)
            el.append(book.author.name)
            books.append(el)
    return jsonify(books)   

@app.route('/books/add', methods = ['POST', 'GET'])
@login_required
def add_book():
    form = BookForm()
    form.author.choices = [(i.id, i.name) for i in Author.query.all()]
    if form.validate_on_submit():
        Book.save(name = form.name.data, date = form.date.data, author_id = form.author.data)
        return redirect(url_for('books'))
    return render_template(
        'form.html',
        title = "Добавление новой книги",
        form = form,
        url = url_for('add_book')
        )


@app.route('/books/change/<book_id>', methods = ['POST', 'GET'])
@login_required
def change_book(book_id):
    form = BookForm()
    form.author.choices = [(i.id, i.name) for i in Author.query.all()]
    book = Book.query.get(book_id)

    if request.method == "POST":
        if form.validate_on_submit():
            book.name = form.name.data
            book.date = form.date.data
            book.author_id = form.author.data
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('books'))
    else:
        form.name.data = book.name
        form.date.data = book.date
        form.author.data = book.author_id
        return render_template(
        'form.html',
        title = "Изменение данных о книге",
        form = form,
        url = url_for('change_book', book_id = book.id)
        )

@app.route('/books/delete/<book_id>')
@login_required
def delete_book(book_id):
    el = Book.query.get(book_id)
    db.session.delete(el)
    db.session.commit()
    return redirect(url_for('books'))


###########             Authors
@app.route('/authors')
def authors():
    table_titles = ['Функции','Имя']
    authors = Author.query.all()
    return render_template(
        'index.html',
        title = "Авторы",
        titles = table_titles,
        elements = authors, 
        url = url_for('load_authors'),
        add_url = url_for('add_authors')
    )

@app.route('/authors/get')
def load_authors():
    authors = []
    try:
        text = request.args['search']
        all_authors = db.engine.execute(f"select * from author where name like '%{text}%'")
        for author in all_authors:
            print(author)
            el = []
            el.append(url_for('delete_author', author_id = author.id))
            el.append(url_for('change_author', author_id = author.id))
            el.append(author.name)
            authors.append(el)    
    except:
        all_authors = Author.query.all()
        for author in all_authors:
            el = []
            el.append(url_for('delete_author', author_id = author.id))
            el.append(url_for('change_author', author_id = author.id))
            el.append(author.name)
            authors.append(el)
    return jsonify(authors)

@app.route('/authors/add', methods = ['POST', 'GET'])
@login_required
def add_authors():
    form = AuthorForm()
    if form.validate_on_submit():
        Author.save(name = form.name.data)
        return redirect(url_for('authors'))
    return render_template(
        'form.html',
        title = "Добавление нового автора",
        form = form,
        url = url_for('add_authors')
        )

@app.route('/authors/change/<author_id>', methods = ['POST', 'GET'])
@login_required
def change_author(author_id):
    form = AuthorForm()

    author = Author.query.get(author_id)

    if request.method == "POST":
        if form.validate_on_submit():
            author.name = form.name.data
            db.session.add(author)
            db.session.commit()
        return redirect(url_for('authors'))
    else:
        form.name.data = author.name
        return render_template(
        'form.html',
        title = "Изменение данных об авторе",
        form = form,
        url = url_for('change_author', author_id = author.id)
        )

@app.route('/authors/delete/<author_id>')
@login_required
def delete_author(author_id):
    el = Author.query.get(author_id)
    db.session.delete(el)
    db.session.commit()
    return redirect(url_for('authors'))