from flask import Flask, render_template, request, flash, session, redirect, url_for
import hashlib
from models import *
import sqlite3

app = Flask(__name__)
app.secret_key = "YP0VRND5VDXEhnC8gTABzjLU4C9obISR"


@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
    return render_template('index.html', user=user)


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
        correct_password = request.form['confirm_password']
        phone_number = request.form['phone']
        birthday = request.form['birthday']
        address = request.form['address']
        role = "user"

        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user != None:
            flash("Compte bancaire déjà existant")
        else:
            if password != correct_password:
                flash("Les mots de passe ne correspondent pas")
            else:
                cursor.execute("INSERT INTO Users (first_name, last_name, gender, email, password, phone_number, birthday, address, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, gender, email, password, phone_number, birthday, address, role))
                conn.commit()
                conn.close()
                user = Users.get_user_by_email(email, password)
                session['user_id'] = user.id_user
                return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.get_user_by_email(email, password)
        if user != None:
            session['user_id'] = user.id_user
            return redirect(url_for('index'))
        else:
            flash("Email ou mot de passe incorrect")
    return render_template('login.html')


@app.route('/profil')
def profil():
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
    return render_template('profil.html', user=user)


if __name__ == "__main__":
    create_db()
    app.run()