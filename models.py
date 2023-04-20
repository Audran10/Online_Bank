import sqlite3

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

class Account:
    def __init__(self, id_account, id_user, cart_nb, name, solde, creation_date, end_date):
        self.id_account = id_account
        self.id_user = id_user
        self.cart_nb = cart_nb
        self.name = name
        self.solde = solde
        self.creation_date = creation_date
        self.end_date = end_date

class Loan:
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

class Transaction:
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
            id_user SERIAL PRIMARY KEY, 
            first_name STRING NOT NULL,
            last_name STRING NOT NULL,
            gender STRING NOT NULL,
            email STRING NOT NULL,
            password STRING NOT NULL,
            phone_number int NOT NULL,
            birthday DATE NOT NULL,
            address STRING NOT NULL,
            role STRING NOT NULL
        )

        CREATE TABLE IF NOT EXISTS Account (
            id_account SERIAL PRIMARY KEY,
            id_user SERIAL FOREIGN KEY REFERENCES Users(id_user),
            cart_nb int NOT NULL,
            name STRING NOT NULL,
            solde int NOT NULL,
            creation_date DATE NOT NULL,
            end_date DATE
        )

        CREATE TABLE IF NOT EXISTS Bank_account (
            id_bank_account SERIAL PRIMARY KEY,
            id_account SERIAL FOREIGN KEY REFERENCES Account(id_account),
        )

        CREATE TABLE IF NOT EXISTS Loan (
            id_loan SERIAL PRIMARY KEY,
            id_account SERIAL FOREIGN KEY REFERENCES Account(id_account),
            duration string NOT NULL,
            loan_amount int NOT NULL,
            interest int NOT NULL,
            amount_reimbursed int NOT NULL,
            monthly_payment int NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status STRING NOT NULL
        )

        CREATE TABLE IF NOT EXISTS Transaction (
            id_transaction SERIAL PRIMARY KEY,
            id_account SERIAL FOREIGN KEY REFERENCES Account(id_account),
            store_name STRING NOT NULL,
            operation_type STRING NOT NULL,
            amount int NOT NULL,
            transaction_date DATE NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
