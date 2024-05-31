from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, BookForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book
from urllib.parse import urlparse

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@login_required
def index():
    form = BookForm()

    return render_template('index.html', form=form)


@app.route('/book/<int:id>')
@login_required
def book_detail(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    return render_template('book_detail.html', book=book, form=form)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            publication_date=form.publication_date.data,
            summary=form.summary.data,
            rating=form.rating.data,
            status=form.status.data,
            date_started=form.date_started.data,
            date_finished=form.date_finished.data,
            user_id=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html', title='Add Book', form=form)

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    if book.user_id != current_user.id:
        flash('You do not have permission to edit this book.')
        return redirect(url_for('index'))
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.publication_date = form.publication_date.data
        book.summary = form.summary.data
        book.rating = form.rating.data
        book.status = form.status.data
        book.date_started = form.date_started.data
        book.date_finished = form.date_finished.data
        db.session.commit()
        flash('Book updated successfully!')
        return redirect(url_for('book_detail', id=book.id))
    return render_template('edit_book.html', title='Edit Book', form=form, book=book)

@app.route('/delete_book/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    if book.user_id != current_user.id:
        flash('You do not have permission to delete this book.')
        return redirect(url_for('index'))
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('index'))