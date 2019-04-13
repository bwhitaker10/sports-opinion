import re
from flask import Flask, redirect, request, render_template, session, flash
from mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "wassup"

SCHEMA = "sports"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/users/create', methods=['POST'])
def users_create():
    errors = []
    query =  "SELECT id FROM users WHERE email=%(email)s;"
    data = {
        'email' : request.form['email']
    }
    db = connectToMySQL(SCHEMA)
    existing_users = db.query_db(query, data)
    if len(existing_users) > 0:
        errors.append("This email already exists")

    if len(request.form['first_name']) < 1:
        errors.append("First Name cannot be left blank")

    if len(request.form['last_name']) < 1:
        errors.append("Last Name cannot be left blank")
        
    if not EMAIL_REGEX.match(request.form['email']):
        errors.append("Email is not valid")

    if len(errors) > 0:
        for error in errors:
            flash(error)
        return redirect('/')

    query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    db = connectToMySQL(SCHEMA)
    db.query_db(query, data)
    return redirect('/success')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)