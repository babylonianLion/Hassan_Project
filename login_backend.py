# Author: Hussain Al Zerjawi
# Date: 05/08/2023

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# SQLite database file name
DB_NAME = "login_database.db"

# Function to create the users table
def create_users_table():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL,
                full_name TEXT
            )
            """
        )
        conn.commit()

# Function to create the login_sessions table
def create_login_sessions_table():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS login_sessions (
                session_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            """
        )
        conn.commit()

# Function to insert a new user into the users table
def insert_user(username, password_hash, email, full_name=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, full_name) VALUES (?, ?, ?, ?)",
            (username, password_hash, email, full_name),
        )
        conn.commit()

# Function to check login credentials
def check_login_credentials(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and user[1] == password:
        return user[0]  # Return the user_id if the password matches
    else:
        return None

# Function to fetch user data for the landing page
def fetch_user_data(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, email, login_time FROM login_sessions JOIN users USING(user_id) WHERE user_id = ? ORDER BY login_time DESC LIMIT 1",
            (user_id,),
        )
        user_data = cursor.fetchone()
    return user_data

# Function to update the password for a user
def update_password(user_id, new_password_hash):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_password_hash, user_id))
        conn.commit()

# Function to create the necessary tables
def create_database():
    create_users_table()
    create_login_sessions_table()

# Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # In a real application, you should hash the password securely

        # Check login credentials
        user_id = check_login_credentials(username, password)
        if user_id:
            session["user_id"] = user_id

            # Log the login session
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO login_sessions (user_id) VALUES (?)", (user_id,))
                conn.commit()

            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login_failed"))

    return render_template("login.html")

@app.route("/login_failed")
def login_failed():
    return render_template("login_failed.html")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        username = request.form["username"]
        password_hash = request.form["password"]  # In a real application, you should hash the password securely
        email = request.form["email"]
        full_name = request.form["full_name"]

        # Insert the new user into the database
        insert_user(username, password_hash, email, full_name)

        # Redirect to the login page after creating the user
        return redirect(url_for("login"))

    return render_template("create_user.html")

@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if user_id:
        # Fetch user data for the landing page
        user_data = fetch_user_data(user_id)

        return render_template("dashboard.html", user_data=user_data)

    # Redirect to login page if the user is not logged in
    return redirect(url_for("login"))

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    user_id = session.get("user_id")
    if user_id:
        if request.method == "POST":
            new_password_hash = request.form["new_password"]
            update_password(user_id, new_password_hash)
            return redirect(url_for("dashboard"))

        return render_template("change_password.html")

    # Redirect to login page if the user is not logged in
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# Start the Flask application
if __name__ == "__main__":
    create_database()  # Create the necessary tables before starting the application
    app.run(debug=True)
