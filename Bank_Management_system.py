# ==========================================
# Project: Smart Bank Management System
# Technologies: Python, SQLite & File Handling
# ==========================================

import sqlite3
from datetime import datetime
import os

# FILES USED IN PROJECT

ACCOUNTS_FILE = "accounts.txt"
BALANCE_FILE = "balance.txt"
TRANSACTIONS_FILE = "transactions.txt"
DATABASE_FILE = "bank.db"

# DATABASE CONNECTION

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    account_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL NOT NULL
)
""")

conn.commit()

# TRANSACTION FILE

def save_transaction(message):
    with open(TRANSACTIONS_FILE, "a") as file:
        file.write(message + "\n")


# UPDATE BALANCE FILE

def update_balance_file():

    cursor.execute("SELECT * FROM accounts")
    records = cursor.fetchall()

    with open(BALANCE_FILE, "w") as file:

        file.write("===== ACCOUNT BALANCES =====\n\n")

        for record in records:

            file.write(f"Account No : {record[0]}\n")
            file.write(f"Name       : {record[1]}\n")
            file.write(f"Balance    : Rs.{record[2]}\n")
            file.write("---------------------------\n")

# CREATE ACCOUNT

def create_account():

    account_no = int(input("Enter Account Number: "))
    name = input("Enter Account Holder Name: ")
    balance = float(input("Enter Initial Deposit: "))

    try:

        cursor.execute(
            "INSERT INTO accounts VALUES (?, ?, ?)",
            (account_no, name, balance)
        )

        conn.commit()

        with open(ACCOUNTS_FILE, "a") as file:
            file.write(f"{account_no},{name},{balance}\n")

        update_balance_file()

        save_transaction(
            f"{datetime.now()} | Account Created | "
            f"Account No: {account_no} | Balance: {balance}"
        )

        print("\nAccount Created Successfully!")

    except sqlite3.IntegrityError:
        print("\nAccount Number Already Exists!")

# CHECK BALANCE

def check_balance():

    account_no = int(input("Enter Account Number: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=?",
        (account_no,)
    )

    result = cursor.fetchone()

    if result:
        print(f"\nCurrent Balance = Rs.{result[0]}")
    else:
        print("\nAccount Not Found!")

# DEPOSIT MONEY

def deposit_money():

    account_no = int(input("Enter Account Number: "))
    amount = float(input("Enter Deposit Amount: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=?",
        (account_no,)
    )

    result = cursor.fetchone()

    if result:

        new_balance = result[0] + amount

        cursor.execute(
            "UPDATE accounts SET balance=? WHERE account_no=?",
            (new_balance, account_no)
        )

        conn.commit()

        update_balance_file()

        save_transaction(
            f"{datetime.now()} | Deposit | "
            f"Account No: {account_no} | Amount: {amount}"
        )

        print("\nDeposit Successful!")
        print(f"Updated Balance = Rs.{new_balance}")

    else:
        print("\nAccount Not Found!")

# WITHDRAW MONEY

def withdraw_money():

    account_no = int(input("Enter Account Number: "))
    amount = float(input("Enter Withdraw Amount: "))

    cursor.execute(
        "SELECT balance FROM accounts WHERE account_no=?",
        (account_no,)
    )

    result = cursor.fetchone()

    if result:

        if amount <= result[0]:

            new_balance = result[0] - amount

            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_no=?",
                (new_balance, account_no)
            )

            conn.commit()

            update_balance_file()

            save_transaction(
                f"{datetime.now()} | Withdraw | "
                f"Account No: {account_no} | Amount: {amount}"
            )

            print("\nWithdrawal Successful!")
            print(f"Remaining Balance = Rs.{new_balance}")

        else:
            print("\nInsufficient Balance!")

    else:
        print("\nAccount Not Found!")

# VIEW TRANSACTION HISTORY

def transaction_history():

    try:

        with open(TRANSACTIONS_FILE, "r") as file:

            print("\n===== TRANSACTION HISTORY =====\n")

            data = file.read()

            if data:
                print(data)
            else:
                print("No Transactions Available!")

    except FileNotFoundError:
        print("Transaction File Not Found!")

# VIEW ALL ACCOUNTS

def view_all_accounts():

    cursor.execute("SELECT * FROM accounts")

    records = cursor.fetchall()

    if records:

        print("\n===== ALL ACCOUNTS =====\n")

        for record in records:

            print(f"Account No : {record[0]}")
            print(f"Name       : {record[1]}")
            print(f"Balance    : Rs.{record[2]}")
            print("-------------------------")

    else:
        print("\nNo Accounts Found!")


# MAIN MENU

while True:

    print("\n")
    print("=" * 45)
    print("     SMART BANK MANAGEMENT SYSTEM")
    print("=" * 45)

    print("1. Create Account")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transaction History")
    print("6. View All Accounts")
    print("7. Exit")

    choice = input("\nEnter Your Choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        check_balance()

    elif choice == "3":
        deposit_money()

    elif choice == "4":
        withdraw_money()

    elif choice == "5":
        transaction_history()

    elif choice == "6":
        view_all_accounts()

    elif choice == "7":
        print("\nThank You For Using Smart Bank Management System!")
        break

    else:
        print("\nInvalid Choice! Please Try Again.")

conn.close()