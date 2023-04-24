import sqlite3

all_users = []

class Users:
    def __init__(self, id_user, first_name, last_name, gender, email, password, phone_number, birthday, address, role):
        self.id_user = id_user
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.birthday = birthday
        self.address = address
        self.role = role

    def get_user_by_email(email, password):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user != None:
            new_user = Users(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9])
            return new_user
        else:
            return None
    
    def get_user_by_id(id_user):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE id_user = ?', (id_user,))
        user = cursor.fetchone()
        if user != None:
            new_user = Users(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9])
            return new_user
        else:
            return None


class Accounts:
    def __init__(self, id_account, id_user, cart_nb, name, solde, creation_date, end_date):
        self.id_account = id_account
        self.id_user = id_user
        self.cart_nb = cart_nb
        self.name = name
        self.solde = solde
        self.creation_date = creation_date
        self.end_date = end_date


class Loans:
    def __init__(self, id_loan, id_account, duration, loan_amount, interest, amount_reimbursed, monthly_payment, start_date, end_date, status):
        self.id_loan = id_loan
        self.id_account = id_account
        self.duration = duration
        self.loan_amount = loan_amount
        self.interest = interest
        self.amount_reimbursed = amount_reimbursed
        self.monthly_payment = monthly_payment
        self.start_date = start_date
        self.end_date = end_date
        self.status = status


class Transactions:
    def __init__(self, id_transaction, id_account, store_name, operation_type, amount, transaction_date):
        self.id_transaction = id_transaction
        self.id_account = id_account
        self.store_name = store_name
        self.operation_type = operation_type
        self.amount = amount
        self.transaction_date = transaction_date


def create_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT, 
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            birthday DATE NOT NULL,
            address TEXT NOT NULL,
            role TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            id_account INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            cart_nb INTEGER NOT NULL,
            name TEXT NOT NULL,
            solde INTEGER NOT NULL,
            creation_date DATE NOT NULL,
            end_date DATE,
            FOREIGN KEY (id_user) REFERENCES Users(id_user)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bank_accounts (
            id_bank_account INTEGER PRIMARY KEY AUTOINCREMENT,
            id_account INTEGER NOT NULL,
            FOREIGN KEY (id_account) REFERENCES Account(id_account)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Loans (
            id_loan INTEGER PRIMARY KEY AUTOINCREMENT,
            id_account INTEGER NOT NULL,
            duration TEXT NOT NULL,
            loan_amount INTEGER NOT NULL,
            interest INTEGER NOT NULL,
            amount_reimbursed INTEGER NOT NULL,
            monthly_payment INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (id_account) REFERENCES Account(id_account)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            id_transaction INTEGER PRIMARY KEY AUTOINCREMENT,
            id_account INTEGER NOT NULL,
            store_name TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            transaction_date DATE NOT NULL,
            FOREIGN KEY (id_account) REFERENCES Account(id_account)
        );
    ''')

    conn.commit()
    conn.close()
