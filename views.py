from flask import Flask, render_template, request, flash, session, redirect, url_for
import hashlib
from models import *
import sqlite3
import random
import datetime


app = Flask(__name__)
app.secret_key = "YP0VRND5VDXEhnC8gTABzjLU4C9obISR"


@app.route('/')
def index():
    user = None
    accounts = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
        if user != None:
            accounts = Accounts.get_accounts_by_user(user.id_user)
    return render_template('index.html', user=user, accounts=accounts)


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
                #hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("INSERT INTO Users (first_name, last_name, gender, email, password, phone_number, birthday, address, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, gender, email, password, phone_number, birthday, address, role))
                conn.commit()
                user = Users.get_user_by_email(email, password)
                session['user_id'] = user.id_user

                new_cart_nb = random.randint(10**15, 10**16-1)
                cursor.execute("SELECT * FROM Accounts WHERE cart_nb = ?", (new_cart_nb,))
                existing_cart_nb = cursor.fetchone()
                while existing_cart_nb != None:
                    new_cart_nb += 1
                    cursor.execute("SELECT * FROM Accounts WHERE cart_nb = ?", (new_cart_nb,))
                    existing_cart_nb = cursor.fetchone()
                current_date = datetime.date.today().strftime("%d-%m-%Y")
                cursor.execute("INSERT INTO Accounts (id_user, cart_nb, name, solde, creation_date) VALUES (?, ?, ?, ?, ?)", (user.id_user, new_cart_nb, "Compte courant", 50, current_date))
                conn.commit()
                conn.close()
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


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'user_id' in session:
        conn = sqlite3.connect('app.db')
        user = Users.get_user_by_id(session['user_id'])
        if user != None:
            accounts = Accounts.get_accounts_by_user(user.id_user)
            if request.method == 'POST':
                beneficiary_name = request.form['beneficiary_name']
                operation_type = request.form['operation_type']
                amount = request.form['amount']
                transaction_date = datetime.date.today().strftime("%d-%m-%Y")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (accounts[0].id_account, beneficiary_name, operation_type, amount, transaction_date))
                conn.commit()
    return render_template('transactions.html', user=user, accounts=accounts)

                
if __name__ == "__main__":
    create_db()
    app.run()
    