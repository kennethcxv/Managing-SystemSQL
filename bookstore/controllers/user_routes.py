from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.order import Order
from models import db

user = Blueprint('user', __name__)


@user.route('/register', methods=['POST', 'GET'])
def register():
    """
    Allow an unauthenticated visitor to create a new Customer account
    """

    # The visitor submitted the registration form
    if request.method == 'POST':
        # Hash the provided password for security
        hashed_pw = generate_password_hash(request.form['password'], method='scrypt')

        # Create a new user row in the database
        new_user = User(Name=request.form['name'], Email=request.form['email'], Password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html')


@user.route('/login', methods=['POST', 'GET'])
def login():
    """
    Allow a visitor with a valid email address / password to log in.
    This sets session variables in a browser cookie to persist the login status after closing and re-opening a tab
    """

    # Visitor has submitted the login form
    if request.method == 'POST':

        # Search for the user corresponding to the provided email address in the database
        user = User.query.filter_by(Email=request.form['email']).first()

        # If the email address exists in the database and the hash of the provided password matches, set session
        if user and check_password_hash(user.Password, request.form['password']):
            session['UserID'] = user.UserID
            session['UserEmail'] = user.Email
            session['UserType'] = user.UserType
            session['UserName'] = user.Name
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html')


@user.route('/logout')
def logout():
    """
    Deletes session variables, requiring a user whom visits this page to log back in
    """
    session.pop('UserID', None)
    session.pop('UserEmail', None)
    session.pop('UserName', None)
    session.pop('UserType', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.index'))


@user.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Allows a user to view/edit their name and email address
    """
    if 'UserID' not in session:
        flash('Please login to view profile', 'danger')
        return redirect(url_for('user.login'))

    #  Fetch the logged in user's ID from the session cookie
    user = User.query.get(session['UserID'])

    # User has submitted the user profile form
    if request.method == 'POST':

        # Update the user's row in the database with the new values
        user.Name = request.form['name']
        user.Email = request.form['email']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))

    return render_template('profile.html', user=user)


@user.route('/my_orders')
def my_orders():
    """
    Allows a user to see the orders they placed
    """
    if 'UserID' not in session:
        flash('Please login to view your orders', 'danger')
        return redirect(url_for('user.login'))

    # Query the database for all orders that belong to the signed-in user
    orders = Order.query.filter_by(UserID=session['UserID']).all()
    return render_template('my_orders.html', orders=orders)
