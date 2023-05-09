from flask import Flask, render_template, request, flash, session, redirect, url_for
import hashlib
from models import *
import sqlite3
import random
import datetime
import smtplib


app = Flask(__name__)
app.secret_key = "YP0VRND5VDXEhnC8gTABzjLU4C9obISR"


@app.route('/', methods=['GET', 'POST'])
def index():
    user = None
    accounts = None
    credits = None
    debits = None
    monthly_saving = None
    transactions = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
        accounts = Accounts.get_accounts_by_user(user.id_user)
        credits = Transactions.get_credit_by_account(accounts[0].id_account)
        debits = Transactions.get_debit_by_account(accounts[0].id_account)
        transactions = Transactions.get_transactions_by_account(accounts[0].id_account)
        monthly_saving = Monthly_saving.get_monthly_saving_by_account(accounts[0].id_account)
    return render_template('index.html', user=user, accounts=accounts, credits=credits, debits=debits, transactions=transactions, monthly_saving=monthly_saving)


@app.route('/monthly_saving', methods=['GET', 'POST'])
def monthly_saving():
    saving = request.form['saving']
    accounts = Accounts.get_accounts_by_user(session['user_id'])
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    Monthly_saving.add_monthly_saving(accounts[0].id_account, saving, date)
    return redirect(url_for('index'))


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
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("INSERT INTO Users (first_name, last_name, gender, email, password, phone_number, birthday, address, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, gender, email, hashed_password, phone_number, birthday, address, role))
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
                return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = Users.get_user_by_email(email, hashed_password)
        if user != None:
            session['user_id'] = user.id_user
            return redirect(url_for('transactions'))
        else:
            flash("Email ou mot de passe incorrect")
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def profile():
    user = None
    accounts = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
        if user != None:
            accounts = Accounts.get_accounts_by_user(user.id_user)
            for account in accounts:
                account.cart_nb = str(account.cart_nb)
            if request.method == 'POST':
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()
                if request.form['email'] == "":
                    email = user.email
                else:
                    email = request.form['email']
                if request.form['phone'] == "":
                    phone_number = user.phone_number
                else:
                    phone_number = request.form['phone']
                if request.form['address'] == "":
                    address = user.address
                else:
                    address = request.form['address']
                if request.form['password'] == "":
                    password = user.password
                else:
                    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
                cursor = conn.cursor()
                cursor.execute("UPDATE Users SET email=?, password=?, phone_number=?, address=? WHERE id_user=?", (email, password, phone_number, address, user.id_user))
                conn.commit()
    return render_template('profile.html', user=user, accounts=accounts)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    user = None
    accounts = None
    if 'user_id' in session:
        conn = sqlite3.connect('app.db')
        user = Users.get_user_by_id(session['user_id'])
        if user != None:
            accounts = Accounts.get_accounts_by_user(user.id_user)
            if request.method == 'POST':
                beneficiary_name = request.form['beneficiary_name']
                operation_type = request.form['operation_type']
                amount = request.form['amount']
                transaction_date = datetime.date.today().strftime("%Y-%m-%d")
                cursor = conn.cursor()
                if operation_type == "debit" and int(amount) > accounts[0].solde:
                    flash("Solde insuffisant")
                else:
                    cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (accounts[0].id_account, beneficiary_name, operation_type, amount, transaction_date))
                    conn.commit()
                    if operation_type == "credit":
                        cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (accounts[0].solde + int(amount), accounts[0].id_account))
                        conn.commit()
                    else:
                        cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (accounts[0].solde - int(amount), accounts[0].id_account))
                        conn.commit()
                    
    return render_template('transactions.html', user=user, accounts=accounts)

                
if __name__ == "__main__":
    create_db()
    app.run(debug=True)
