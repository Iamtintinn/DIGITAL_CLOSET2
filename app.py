import mysql.connector

import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import os

# ----------------- AUTO DATABASE SETUP -----------------
def setup_database():
    # Connect to MySQL server (no database yet)
    db = mysql.connector.connect(
        host="localhost",
        user="root",    # XAMPP default
        password="",    # XAMPP default
        port=3306       # XAMPP default port
    )
    cursor = db.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS dress")
    cursor.execute("USE dress")

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clothes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        color VARCHAR(50),
        category VARCHAR(50),
        image VARCHAR(255)
    )
    """)

    db.commit()
    db.close()
    print("Database and table are ready!")

# Run setup immediately
setup_database()
# --------------------------------------------------------

# MySQL connection for Flask app
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",      # XAMPP default
    database="dress",
    port=3306
)
cursor = db.cursor()

# Initialize Flask app
app = Flask(__name__)

# Temporary user (for testing)
USER = {
    "username": "admin",
    "password": "1234"
}

# ----------------- ROUTES -----------------

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == USER['username'] and password == USER['password']:
        return redirect(url_for('mainpage'))
    else:
        return "Invalid username or password. Try again."

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

@app.route('/input')
def input_page():
    cursor.execute("SELECT id, name, color, category, image FROM clothes")
    clothes = cursor.fetchall()
    return render_template('input.html', clothing_list=clothes)

@app.route('/add_clothes', methods=['POST'])
def add_clothes():
    name = request.form['Name']
    color = request.form['color']
    category = request.form['category']

    image_file = request.files.get('image')
    if image_file:
        image_filename = image_file.filename
        upload_path = os.path.join('static', 'uploads', image_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        image_file.save(upload_path)
    else:
        image_filename = ""

    sql = "INSERT INTO clothes (name, color, category, image) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, color, category, image_filename))
    db.commit()

    return redirect(url_for('input_page'))

@app.route('/edit_clothes/<int:id>', methods=['POST'])
def update_clothes(id):
    name = request.form['Name']
    color = request.form['color']
    category = request.form['category']

    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        image_filename = image_file.filename
        upload_path = os.path.join('static', 'uploads', image_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        image_file.save(upload_path)
        sql = "UPDATE clothes SET name=%s, color=%s, category=%s, image=%s WHERE id=%s"
        cursor.execute(sql, (name, color, category, image_filename, id))
    else:
        sql = "UPDATE clothes SET name=%s, color=%s, category=%s WHERE id=%s"
        cursor.execute(sql, (name, color, category, id))

    db.commit()
    return redirect(url_for('input_page'))

@app.route('/delete_clothes/<int:id>', methods=['POST'])
def delete_clothes(id):
    sql = "DELETE FROM clothes WHERE id=%s"
    cursor.execute(sql, (id,))
    db.commit()
    return redirect(url_for('input_page'))

@app.route('/closet')
def closet_page():
    cursor.execute("SELECT id, name, color, category, image FROM clothes")
    clothes = cursor.fetchall()
    return render_template('closet.html', clothing_list=clothes)

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    app.run(debug=True)