# Database-Management Project

## Project Overview
This project, named 'Database-Management', is a web-based application designed for managing a bookstore. It utilizes Python for backend processing and a MySQL database for data storage. The application facilitates various operations related to book management, such as browsing books, managing inventory, and processing sales.

## Prerequisites
- Python (version as specified in `requirements.txt`)
- MySQL Server
- Any modern web browser

## Installation and Setup
1. **Clone the Repository**
   - Use Git to clone the repository to your local machine.
   - `git clone [repository-url]`
2. **Install Dependencies**
   - Navigate to the project's root directory.
   - Run `pip install -r requirements.txt` to install the necessary Python packages.
3. **Database Setup**
   - Start your MySQL server.
   - Create a new database and import the `mysql-db.sql` file for the initial database schema.
4. **Configuration**
   - Edit the `config.py` file to align with your database credentials and other settings.

## Running the Application
1. Navigate to the project's root directory.
2. Run `python run.py` to start the application.
3. Open your web browser and navigate to `http://localhost:[port-number]` (port number will be defined in `run.py` or `config.py`).

## Project Structure
- `run.py`: The entry point of the web application.
- `config.py`: Contains configuration settings.
- `models/`: Python modules for database models.
- `static/`: Static files such as CSS and JavaScript.
- `templates/`: HTML templates for the web interface.
- `mysql-db.sql`: SQL file for database setup.
- `controllers/`: Scripts for application logic.
