from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.book import Book
from models.order import Order

book_routes = Blueprint('book', __name__)


@book_routes.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Allows a logged-in user to add new books to the bookstore database.
    """

    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to add books')
        return redirect(url_for('user.login'))

    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # If user submits a new book through the form, persist it to the database and redirect to the dashboard
    if request.method == 'POST':
        new_book = Book(
            Title=request.form['title'],
            Author=request.form['author'],
            Price=request.form['price'],
            Stock=request.form['stock']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    # If the user landed on the add book form
    return render_template('add_book.html')


@book_routes.route('/order_book/<int:book_id>', methods=['GET', 'POST'])
def order_book(book_id):
    """
    Allows a user to order a book.
    This will subtract the order quantity from the stock and create an order for the user.
    :param book_id: The primary key of a row in the book database table
    """

    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to order books', 'danger')
        return redirect(url_for('user.login'))

    book = Book.query.get(book_id)

    # If the book_id passed in through the URL doesn't match any book
    # in the database, return an error and redirect to the book index
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('book.index'))

    # If the user is submitting an order through the order book form:
    # Verify quantity ordered is within bounds
    # If so, subtract quantity from book stock and persist that change to the database
    # Then redirect to the order book page
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        if quantity <= 0:
            flash('You must order a minimum of 1 book', 'danger')
            return redirect(url_for('book.order_book', book_id=book_id))
        if quantity > book.Stock:
            flash('Not enough stock available!', 'danger')
            return redirect(url_for('book.order_book', book_id=book_id))
        
        new_order = Order(UserID=session['UserID'], BookID=book_id, Quantity=quantity)
        book.Stock -= quantity
        db.session.add(new_order)
        db.session.commit()
        flash('Book ordered successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    # If the user landed on the order book form
    return render_template('order_book.html', book=book)
