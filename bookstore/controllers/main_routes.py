from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash

from models import db
from models.user import User
from models.book import Book

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Home page of the bookstore
    """

    # Only show books on the storefront that have inventory
    books = Book.query.filter(Book.Stock >= 1).filter(Book.OutOfPrint == False)
    return render_template('index.html', books=books)


@main.route('/all_users')
def all_users():
    """
    Allows an administrator to see all users in the user table of the database
    """
    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to access admin view books')
        return redirect(url_for('user.login'))

    # This route only works for Admins
    if session['UserType'] != 'Admin':
        flash('You must be an admin to preform this operation')
        return redirect(url_for('main.index'))

    # Fetch all users from the database
    users = User.query.all()
    return render_template('all_users.html', users=users)


@main.route('/reset_password', defaults={'user_id': None}, methods=['GET', 'POST'])
@main.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    """
    Allows users to reset their own passwords, and allow admins to reset anyone's password
    :param user_id: Optional: The primary key of the user DB table representing the user to have their password reset
    """
    # If user is not logged in, redirect them to login page
    if 'UserID' not in session:
        flash('Please login to reset password')
        return redirect(url_for('user.login'))

    # Default to resetting your own password, unless indicated in the URL
    if user_id is None:
        user_id = session['UserID']

    # Customers can only reset their own passwords
    if session['UserType'] == 'Customer' and user_id != session['UserID']:
        flash('You can only try to change your own password.')
        return redirect(url_for('main.index'))

    # The user has submitted the password reset form
    if request.method == 'POST':
        # Fetch the specified user from the database and update the row with the new password
        password_reset_user = User.query.get(user_id)
        password_reset_user.Password = generate_password_hash(request.form['password'], method='scrypt')
        db.session.commit()

        # Don't log out admins when they reset another user's password
        if session['UserType'] == 'Admin':
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('user.logout'))

    return render_template('reset_password.html', user_id=user_id)


@main.route('/dashboard')
def dashboard():
    """
    A dashboard of links to navigate the user to order history, profile, password reset, etc.
    Admins see more options than users do and can also edit the bookstore contents.
    """
    if 'UserID' in session:
        user = User.query.filter_by(UserID=session['UserID']).first()
        return render_template('dashboard.html', user=user)
    return redirect(url_for('user.login'))
