import sqlite3
import json
import datetime

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
    def __init__(self, id_account, id_user, cart_nb, name, solde, creation_date, end_date, transactions, monthly_saving, credits, debits, credits_for_year, debits_for_year):
        self.id_account = id_account
        self.id_user = id_user
        self.cart_nb = cart_nb
        self.name = name
        self.solde = solde
        self.creation_date = creation_date
        self.end_date = end_date
        self.transactions = transactions
        self.monthly_saving = monthly_saving
        self.credits = credits
        self.debits = debits
        self.credits_for_year = credits_for_year
        self.debits_for_year = debits_for_year

    
    def get_accounts_by_user(id_user):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Accounts WHERE id_user = ? ORDER BY id_account ASC', (id_user,))
        accounts = cursor.fetchall()
        new_accounts = []
        for index, account in enumerate(accounts):
            cursor.execute('SELECT * FROM Transactions WHERE id_account = ? ORDER BY transaction_date DESC', (account[0],))
            transactions = cursor.fetchall()
            monthly_saving = Monthly_saving.get_monthly_saving_by_account_by_user(id_user)[index]
            credits = Transactions.get_credit_by_user(id_user)[index]
            debits = Transactions.get_debit_by_user(id_user)[index]
            credits_for_year = Transactions.get_credit_by_mounth(id_user)[index]
            debits_for_year = Transactions.get_debit_by_mounth(id_user)[index]
            new_account = Accounts(
                account[0], account[1], account[2], account[3], account[4], 
                account[5], account[6], transactions, monthly_saving, credits, debits,
                credits_for_year, debits_for_year
            )
            new_accounts.append(new_account)
        conn.close()
        return new_accounts

    
    def get_account_by_user_and_name(id_user, name):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Accounts WHERE id_user = ? AND name = ?', (id_user, name))
        account = cursor.fetchone()
        if account != None:
            new_account = Accounts(account[0], account[1], account[2], account[3], account[4], account[5], account[6], None, None, None, None, None, None)
            return new_account
        else:
            return None

class Monthly_saving:
    def __init__(self, id_monthly_saving, id_account, amount, date):
        self.id_monthly_saving = id_monthly_saving
        self.id_account = id_account
        self.amount = amount
        self.date = date

    def get_monthly_saving_by_account_by_user(user_id):
        list_all_savings = []
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_account FROM Accounts WHERE id_user = ?", (user_id,))
        account_ids = cursor.fetchall()
        for account_id in account_ids:
            cursor.execute('SELECT sum(amount) FROM Monthly_saving WHERE id_account = ? ORDER BY id_monthly_saving ASC', (account_id[0],))
            monthly_saving = cursor.fetchone()[0]
            list_all_savings.append(monthly_saving)
        conn.close()
        return list_all_savings
        
    
    def add_monthly_saving(id_account, amount, date):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Monthly_saving (id_account, amount, date) VALUES (?, ?, ?)', (id_account, amount, date))
        cursor.execute('UPDATE Accounts SET solde = solde - ? WHERE id_account = ?', (amount, id_account))
        conn.commit()
        conn.close()

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
    def __init__(self, id_transaction, id_account, beneficiary_name, operation_type, amount, transaction_date):
        self.id_transaction = id_transaction
        self.id_account = id_account
        self.beneficiary_name = beneficiary_name
        self.operation_type = operation_type
        self.amount = amount
        self.transaction_date = transaction_date
    

    def get_credit_by_user(user_id):
        list_credit_accounts = []
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        month_year_str = datetime.datetime.now().strftime('%m-%Y')
        cursor.execute("SELECT id_account FROM Accounts WHERE id_user = ?", (user_id,))
        account_ids = cursor.fetchall()
        for account_id in account_ids:
            cursor.execute("SELECT SUM(amount) FROM Transactions WHERE id_account = ? AND operation_type = 'credit' AND strftime('%m-%Y', transaction_date) = ?", (account_id[0], month_year_str))
            credit_sum = cursor.fetchone()[0]
            list_credit_accounts.append(credit_sum)
        conn.close()
        return list_credit_accounts



    
    def get_debit_by_user(id_user):
        list_debit_accounts = []
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        month_year_str = datetime.datetime.now().strftime('%m-%Y')
        cursor.execute("SELECT id_account FROM Accounts WHERE id_user = ?", (id_user,))
        account_ids = cursor.fetchall()
        for account_id in account_ids:
            cursor.execute("SELECT SUM(amount) FROM Transactions WHERE id_account = ? AND operation_type = 'debit' AND strftime('%m-%Y', transaction_date) = ?", (account_id[0], month_year_str))
            debit_sum = cursor.fetchone()[0]
            list_debit_accounts.append(debit_sum)
        conn.close()
        return list_debit_accounts
    

    def get_credit_by_mounth(id_user):
        credit_list = []
        credit_list_all_accounts = []
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_account FROM Accounts WHERE id_user = ?", (id_user,))
        account_ids = cursor.fetchall()
        for account_id in account_ids:
            for i in range(1, 13):
                cursor.execute("SELECT SUM(amount) FROM Transactions WHERE id_account = ? AND operation_type = 'credit' AND strftime('%m', transaction_date) = ?", (account_id[0], str(i).zfill(2)))
                credit_sum = cursor.fetchone()[0]
                credit_list.append(credit_sum)
            credit_list_all_accounts.append(credit_list)
            credit_list = []
        conn.close()
        return credit_list_all_accounts
    

    def get_debit_by_mounth(id_user):
        debit_list = []
        debit_list_all_accounts = []
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_account FROM Accounts WHERE id_user = ?", (id_user,))
        account_ids = cursor.fetchall()
        for account_id in account_ids:
            for i in range(1, 13):
                cursor.execute("SELECT SUM(amount) FROM Transactions WHERE id_account = ? AND operation_type = 'debit' AND strftime('%m', transaction_date) = ?", (account_id[0], str(i).zfill(2)))
                debit_sum = cursor.fetchone()[0]
                debit_list.append(debit_sum)
            debit_list_all_accounts.append(debit_list)
            debit_list = []
        conn.close()
        return debit_list_all_accounts
            

    def get_transactions_by_user(id_user):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id_account FROM Accounts WHERE id_user = ?', (id_user,))
        account_ids = cursor.fetchall()
        all_transactions = []
        for account_id in account_ids:
            cursor.execute('SELECT * FROM Transactions WHERE id_account = ? ORDER BY id_transaction DESC', (account_id[0],))
            transactions = cursor.fetchall()
            if transactions != None:
                new_transactions = []
                for transaction in transactions:
                    new_transaction = Transactions(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[5])
                    new_transactions.append(new_transaction)
                all_transactions.append(new_transactions)
                new_transactions = []
        conn.close()
        return all_transactions



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
            cart_nb INTEGER,
            name TEXT NOT NULL,
            solde INTEGER NOT NULL,
            creation_date DATE NOT NULL,
            end_date DATE,
            FOREIGN KEY (id_user) REFERENCES Users(id_user)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Monthly_saving (
            id_monthly_saving INTEGER PRIMARY KEY AUTOINCREMENT,
            id_account INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            date DATE NOT NULL,
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
            beneficiary_name TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            transaction_date DATE NOT NULL,
            FOREIGN KEY (id_account) REFERENCES Account(id_account)
        );
    ''')

    conn.commit()
    conn.close()
