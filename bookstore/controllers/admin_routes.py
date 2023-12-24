from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.book import Book
from models import db
from models.order import Order
from models.user import User

admin = Blueprint('admin', __name__)


@admin.route('/books')
def admin_books():
    """
    Allows a logged-in admin to see all books in the database
    """

    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to access admin view books')
        return redirect(url_for('user.login'))

    # This route only works for Admins
    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # Query for all books in the DB
    books = Book.query.all()
    return render_template('admin_books.html', books=books)


@admin.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """
    Allows a logged-in admin to edit a book
    :param book_id: The primary key of the books database table
    """

    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to access admin view books')
        return redirect(url_for('user.login'))

    # This route only works for Admins
    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # Fetch the book from the database by its primary key
    book = Book.query.get(book_id)

    # If a non-existent BookID was searched for
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('admin.admin_books'))

    # User has submitted the edit book form
    if request.method == 'POST':
        # Update the database with the new book information
        book.Title = request.form['title']
        book.Author = request.form['author']
        book.Price = float(request.form['price'])
        book.Stock = int(request.form['stock'])
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin.admin_books'))

    return render_template('edit_books.html', book=book)


@admin.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    """
    Allows an admin to delete a book from the books table in the database
    :param book_id: The primary key of the Book table in the database representing the book to be deleted
    """
    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to access admin view books')
        return redirect(url_for('user.login'))

    # This route only works for Admins
    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # If a non-existent BookID was searched for
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('admin.admin_books'))

    # Delete the book from the database
    book.OutOfPrint = True
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.admin_books'))


@admin.route('/restore_book/<int:book_id>')
def restore_book(book_id):
    """
    Allows an admin to restore a deleted book from the books table in the database
    :param book_id: The primary key of the Book table in the database representing the book to be deleted
    """
    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to access admin view books')
        return redirect(url_for('user.login'))

    # This route only works for Admins
    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # If a non-existent BookID was searched for
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found!', 'danger')
        return redirect(url_for('admin.admin_books'))

    # Delete the book from the database
    book.OutOfPrint = False
    db.session.commit()
    flash('Book restored successfully!', 'success')
    return redirect(url_for('admin.admin_books'))



@admin.route('/all_orders')
def all_orders():
    """
    Allows an admin to see all orders, and find the total sales value
    """
    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to access admin view all orders')
        return redirect(url_for('user.login'))

    # This route only works for Admins
    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # Query the database for all orders, joining the user data
    orders = db.session.query(Order, User).join(User).filter(Order.UserID == User.UserID)

    return render_template('all_orders.html', orders=orders)
