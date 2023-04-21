from flask import Flask, render_template, request, flash
from models import *
import sqlite3
from pprint import pprint

app = Flask(__name__)
app.secret_key = "YP0VRND5VDXEhnC8gTABzjLU4C9obISR"


@app.route('/')
def index():
    create_db()
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        first_name = request.form['firstname']
        last_name = request.form['lastname']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone']
        birthday = request.form['birthday']
        address = request.form['address']
        role = "user"

        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user != None:
            flash("Compte bancaire déjà existant")
        else:
            cursor.execute("INSERT INTO Users (first_name, last_name, gender, email, password, phone_number, birthday, address, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, gender, email, password, phone_number, birthday, address, role))
            conn.commit()
            conn.close()
            return render_template('index.html')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    Users.user_list()
    return render_template('login.html')

if __name__ == "__main__":
    app.run()