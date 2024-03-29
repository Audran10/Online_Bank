from flask import Flask, render_template, request, flash, session, redirect, url_for
import json
import hashlib
from models import *
import sqlite3
import random
import datetime


app = Flask(__name__)
app.secret_key = "YP0VRND5VDXEhnC8gTABzjLU4C9obISR"


@app.route('/', methods=['GET', 'POST'])
def index():
    user = None
    account = None
    accounts = None
    credits = None
    debits = None
    monthly_saving = None
    transactions = None
    credits_for_year = None
    debits_for_year = None
    accounts_list = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
        if user != None:
            account = Accounts.get_account_by_user_and_name(user.id_user, "Checking Account")
            accounts = Accounts.get_accounts_by_user(user.id_user)
            credits = Transactions.get_credit_by_user(user.id_user)
            debits = Transactions.get_debit_by_user(user.id_user)
            transactions = Transactions.get_transactions_by_user(user.id_user)
            monthly_saving = Monthly_saving.get_monthly_saving_by_account_by_user(user.id_user, "Checking Account")
            credits_for_year = json.dumps(Transactions.get_credit_by_mounth(user.id_user))
            debits_for_year = json.dumps(Transactions.get_debit_by_mounth(user.id_user))
    return render_template('index.html', account=account, user=user, accounts=accounts, 
                           credits=credits, debits=debits, transactions=transactions, 
                           monthly_saving=monthly_saving, credits_for_year=credits_for_year,
                           debits_for_year=debits_for_year, accounts_list=accounts_list)


@app.route('/add_monthly_saving', methods=['GET', 'POST'])
def monthly_saving():
    saving = request.form['saving']
    accounts = Accounts.get_accounts_by_user(session['user_id'])
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    Monthly_saving.add_monthly_saving(accounts[0].id_account, saving, date)
    return redirect(url_for('index'))


@app.route('/remove_monthly_saving', methods=['GET', 'POST'])
def delete_monthly_saving():
    user = Users.get_user_by_id(session['user_id'])
    remove_saving = request.form['remove_saving']
    accounts = Accounts.get_accounts_by_user(session['user_id'])
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    Monthly_saving.remove_monthly_saving(user.id_user, accounts[0].id_account, remove_saving, date)
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
                user = Users.get_user_by_email(email, hashed_password)
                session['user_id'] = user.id_user
                new_cart_nb = random.randint(10**15, 10**16-1)
                cursor.execute("SELECT * FROM Accounts WHERE cart_nb = ?", (new_cart_nb,))
                existing_cart_nb = cursor.fetchone()
                while existing_cart_nb != None:
                    new_cart_nb += 1
                    cursor.execute("SELECT * FROM Accounts WHERE cart_nb = ?", (new_cart_nb,))
                    existing_cart_nb = cursor.fetchone()
                current_date = datetime.date.today().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO Accounts (id_user, cart_nb, name, solde, creation_date) VALUES (?, ?, ?, ?, ?)", (user.id_user, new_cart_nb, "Checking Account", 50, current_date))
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
            return redirect(url_for('index'))
        else:
            flash("Email ou mot de passe incorrect")
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def profile():
    user = None
    accounts = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
    else :
        return render_template('index.html', user=user, accounts=accounts)
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


@app.route('/delete_account', methods=['DELETE', 'POST'])
def delete_account():
    if request.method == 'POST':
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Transactions WHERE id_account IN (SELECT id_account FROM Accounts WHERE id_user=?)", (session['user_id'],))
        conn.commit()
        cursor.execute("DELETE FROM Monthly_saving WHERE id_account IN (SELECT id_account FROM Accounts WHERE id_user=?)", (session['user_id'],))
        conn.commit()
        cursor.execute("DELETE FROM Users WHERE id_user=?", (session['user_id'],))
        conn.commit()
        cursor.execute("DELETE FROM Accounts WHERE id_user=?", (session['user_id'],))
        conn.commit()
        session.pop('user_id', None)
        conn.close()
        return redirect(url_for('index'))
    return render_template('profile.html')


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    user = None
    accounts = None
    if 'user_id' in session:
        conn = sqlite3.connect('app.db')
        user = Users.get_user_by_id(session['user_id'])
    else :
        return render_template('index.html', user=user, accounts=accounts)
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


@app.route('/transactions_admin', methods=['GET', 'POST'])
def transactions_admin():
    user = None
    accounts = None
    if 'user_id' in session:
        conn = sqlite3.connect('app.db')
        user = Users.get_user_by_id(session['user_id'])
    else :
        return render_template('index.html', user=user, accounts=accounts)
    if request.method == 'POST':
        beneficiary_name = request.form['beneficiary_name']
        operation_type = request.form['operation_type']
        amount = request.form['amount']
        card_nb = request.form['card_number']
        transaction_date = datetime.date.today().strftime("%Y-%m-%d")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE cart_nb = ?", (card_nb,))
        account = cursor.fetchone()
        if account == None:
            flash("Numéro de carte invalide")
        else:
            cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (account[0], beneficiary_name, operation_type, amount, transaction_date))
            conn.commit()
            if operation_type == "credit":
                cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (account[4] + int(amount), account[0]))
                conn.commit()
            else:
                cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (account[4] - int(amount), account[0]))
                conn.commit()
    return redirect(url_for('admin'))


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    user = None
    accounts = None
    if 'user_id' in session:
        conn = sqlite3.connect('app.db')
        user = Users.get_user_by_id(session['user_id'])
    else :
        return render_template('index.html', user=user, accounts=accounts)
    operation_type = request.form['operation_type']
    epargne_account = request.form['epargne_account']
    amount = request.form['amount']
    transaction_date = datetime.date.today().strftime("%Y-%m-%d")
    cursor = conn.cursor()
    if operation_type == "debit" and int(amount) < Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").solde:
        cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").id_account, "Transfer", "credit", amount, transaction_date))
        conn.commit()
        cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (Accounts.get_account_by_user_and_name(user.id_user, epargne_account).id_account, "Transfer", "debit", amount, transaction_date))
        conn.commit()
        cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").solde + int(amount), Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").id_account))
        conn.commit()
        cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (Accounts.get_account_by_user_and_name(user.id_user, epargne_account).solde - int(amount), Accounts.get_account_by_user_and_name(user.id_user, epargne_account).id_account))
        conn.commit()
    elif operation_type == "credit" and int(amount) < Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").solde:
        cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").id_account, "Transfer", "debit", amount, transaction_date))
        conn.commit()
        cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (Accounts.get_account_by_user_and_name(user.id_user, epargne_account).id_account, "Transfer", "credit", amount, transaction_date))
        conn.commit()
        cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").solde - int(amount), Accounts.get_account_by_user_and_name(user.id_user, "Checking Account").id_account))
        conn.commit()
        cursor.execute("UPDATE Accounts SET solde = ? WHERE id_account = ?", (Accounts.get_account_by_user_and_name(user.id_user, epargne_account).solde + int(amount), Accounts.get_account_by_user_and_name(user.id_user, epargne_account).id_account))
        conn.commit()
    return redirect(url_for('transactions'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    user = None 
    accounts = None
    if 'user_id' in session:
        user = Users.get_user_by_id(session['user_id'])
    else :
        return render_template('index.html', user=user, accounts=accounts)
    accounts = Accounts.get_accounts_by_user(user.id_user)
    if request.method == 'POST':
        accounts = Accounts.get_accounts_by_user(user.id_user)
        name = request.form['name']
        user_id = session['user_id']
        creation_date = datetime.date.today().strftime("%Y-%m-%d")
        cart_nb = None
        solde_compte_courant = Accounts.get_account_by_user_and_name(user_id, "Checking Account").solde 
        solde = request.form['solde']
        if int(solde) <= 50:
            solde = 50 
        else : 
            solde = solde
        if solde_compte_courant < int(solde):
            flash("Solde insuffisant")
        elif name == "A Account" and Accounts.get_account_by_user_and_name(user_id, "A Account") != None:
            flash("You cannot create more than one A Account")
        elif name == "DDS Account" and Accounts.get_account_by_user_and_name(user_id, "DDS Account") != None:
            flash("You cannot create more than one A Account")
        else:
            new_solde_compte_courant = Accounts.get_account_by_user_and_name(user_id, "Checking Account").solde - int(solde) 
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Accounts (id_user, cart_nb, name, solde, creation_date) VALUES (?, ?, ?, ?, ?)", (user_id, cart_nb, name, solde, creation_date))
            cursor.execute("UPDATE Accounts SET solde = ? WHERE id_user = ? AND name = ?", (new_solde_compte_courant, user_id, "Checking Account"))
            conn.commit()
            cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (Accounts.get_account_by_user_and_name(user_id, name).id_account, "Account opening", "credit", solde, creation_date))
            cursor.execute("INSERT INTO Transactions (id_account, beneficiary_name, operation_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)", (Accounts.get_account_by_user_and_name(user_id, "Checking Account").id_account, "Account opening", "debit", solde, creation_date))
            conn.commit()
            conn.close()
            flash("New account created successfully")
            return redirect(url_for('index'))
    return render_template('create_account.html', user=user, accounts=accounts)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    user = None
    if 'user_id' in session :
        user = Users.get_user_by_id(session['user_id'])
    else :
        return render_template('index.html', user=user)
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return render_template('admin.html', user=user, users=users)
 
        
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

                
if __name__ == "__main__":
    create_db()
    app.run(debug=True)