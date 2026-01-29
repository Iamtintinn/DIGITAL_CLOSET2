import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  #py your root password
    database="dress"
)
cursor = db.cursor()


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary user (for testing only)
USER = {
    "username": "admin",
    "password": "1234"
}

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



@app.route('/add_clothes', methods=['POST'])
def add_clothes():
    name = request.form['Name']
    color = request.form['color']
    category = request.form['category']

    image_file = request.files.get('image')
    image_filename = image_file.filename
    image_file.save(f'static/uploads/{image_filename}')

    sql = "INSERT INTO clothes (name, color, category, image) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, color, category, image_filename))
    db.commit()

    return redirect(url_for('input_page'))
@app.route('/input')
def input_page():
    cursor.execute("SELECT id, name, color, category, image FROM clothes")
    clothes = cursor.fetchall()
    return render_template('input.html', clothing_list=clothes)
@app.route('/delete_clothes/<int:id>', methods=['POST'])
def delete_clothes(id):
    sql = "DELETE FROM clothes WHERE id = %s"
    cursor.execute(sql,(id,))
    db.commit()
    return redirect (url_for('input_page'))

 
@app.route('/edit_clothes/<int:id>', methods=['POST'])
def update_clothes(id):
    name = request.form ['Name']
    color = request.form ['color']
    category = request.form['category']

    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        image_filename = image_file.filename
        image_file.save(f'static/uploads/{image_filename}')
        sql = "UPDATE clothes SET name=%s, color=%s, category=%s, image=%s WHERE id=%s"
        cursor.execute(sql, (name, color, category, image_filename, id))
    else:
        sql = "UPDATE clothes SET name=%s, color=%s, category=%s WHERE id=%s"
        cursor.execute(sql, (name, color, category, id))

    db.commit()
    return redirect(url_for('input_page'))


@app.route('/closet')
def closet_page(): 
    cursor.execute("SELECT id, name, color, category, image FROM clothes")
    clothes = cursor.fetchall()
    return render_template('closet.html', clothing_list=clothes)


if __name__ == '__main__':
    app.run(debug=True)
