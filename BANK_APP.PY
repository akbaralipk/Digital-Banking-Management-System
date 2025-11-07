import streamlit as st
from abc import ABC, abstractmethod

# =========================================================
# Abstract Base Class for Bank Operations
# =========================================================
class Bank(ABC):
    @abstractmethod
    def withdraw(self, amount, pin):
        pass

    @abstractmethod
    def deposit(self, amount, pin):
        pass

    @abstractmethod
    def check_balance(self, pin):
        pass


# =========================================================
# Account Class for Customer Operations
# =========================================================
class Account(Bank):
    def __init__(self, ac_no, pin):
        self.ac_no = ac_no
        self.__pin = pin
        self.balance = 0.0
        self.transactions = []

    def verify_pin(self, pin):
        return self.__pin == pin

    def deposit(self, amount, pin):
        if self.verify_pin(pin):
            self.balance += amount
            self.transactions.append(f"Deposited ₹{amount}")
            return f"Transaction Successful: ₹{amount} credited to Account {self.ac_no}. Current Balance: ₹{self.balance}"
        return "Invalid PIN. Please try again."

    def withdraw(self, amount, pin):
        if self.verify_pin(pin):
            if self.balance >= amount:
                self.balance -= amount
                self.transactions.append(f"Withdrawn ₹{amount}")
                return f"Transaction Successful: ₹{amount} debited from Account {self.ac_no}. Current Balance: ₹{self.balance}"
            return "Insufficient Balance. Please check your account."
        return "Invalid PIN. Please try again."

    def check_balance(self, pin):
        if self.verify_pin(pin):
            return f"Account Number: {self.ac_no} | Current Balance: ₹{self.balance}"
        return "Invalid PIN. Please try again."

    def get_transactions(self, pin):
        if self.verify_pin(pin):
            return self.transactions if self.transactions else ["No transactions available."]
        return ["Invalid PIN. Please try again."]


# =========================================================
# Streamlit Application Interface
# =========================================================
st.set_page_config(page_title="Digital Banking System", layout="wide")
st.title("Digital Banking Management System")
st.markdown(
    """
    Welcome to the Digital Banking Management System (DBMS).  
    A secure and efficient platform to manage your bank accounts.  
    Perform Deposits, Withdrawals, and Balance Inquiries with verified PIN authentication.
    """
)

# Initialize account storage in session
if "accounts" not in st.session_state:
    st.session_state["accounts"] = {}  # Key: Account Number | Value: Account Object

# Sidebar Navigation
st.sidebar.header("Customer Services")
menu = st.sidebar.radio(
    "Select Operation",
    ["Open New Account", "Deposit Funds", "Withdraw Funds", "Balance Inquiry", "Transaction History"],
)

# =========================================================
# Account Creation Section
# =========================================================
if menu == "Open New Account":
    st.subheader("Open a New Account")
    ac_no = st.text_input("Enter a Unique Account Number:")
    pin = st.number_input("Set a 4-digit PIN:", min_value=1000, max_value=9999, step=1)

    if st.button("Create Account"):
        if ac_no and pin:
            if ac_no in st.session_state["accounts"]:
                st.warning("Account number already exists. Please use a different one.")
            else:
                st.session_state["accounts"][ac_no] = Account(ac_no, pin)
                st.success(f"Account {ac_no} successfully created with an opening balance of ₹0.00.")
        else:
            st.error("Please provide both Account Number and PIN.")


# =========================================================
# Deposit Funds Section
# =========================================================
elif menu == "Deposit Funds":
    st.subheader("Deposit Funds")
    ac_no = st.text_input("Enter Account Number:")
    pin = st.number_input("Enter 4-digit PIN:", min_value=1000, max_value=9999, step=1)
    amount = st.number_input("Enter Deposit Amount (₹):", min_value=0.0, step=100.0)

    if st.button("Proceed with Deposit"):
        if ac_no in st.session_state["accounts"]:
            account = st.session_state["accounts"][ac_no]
            st.info(account.deposit(amount, pin))
        else:
            st.error("Account not found. Please check the account number.")


# =========================================================
# Withdraw Funds Section
# =========================================================
elif menu == "Withdraw Funds":
    st.subheader("Withdraw Funds")
    ac_no = st.text_input("Enter Account Number:")
    pin = st.number_input("Enter 4-digit PIN:", min_value=1000, max_value=9999, step=1)
    amount = st.number_input("Enter Withdrawal Amount (₹):", min_value=0.0, step=100.0)

    if st.button("Proceed with Withdrawal"):
        if ac_no in st.session_state["accounts"]:
            account = st.session_state["accounts"][ac_no]
            st.warning(account.withdraw(amount, pin))
        else:
            st.error("Account not found. Please check the account number.")


# =========================================================
# Balance Inquiry Section
# =========================================================
elif menu == "Balance Inquiry":
    st.subheader("Account Balance Inquiry")
    ac_no = st.text_input("Enter Account Number:")
    pin = st.number_input("Enter 4-digit PIN:", min_value=1000, max_value=9999, step=1)

    if st.button("Check Balance"):
        if ac_no in st.session_state["accounts"]:
            account = st.session_state["accounts"][ac_no]
            st.success(account.check_balance(pin))
        else:
            st.error("Account not found. Please check the account number.")


# =========================================================
# Transaction History Section
# =========================================================
elif menu == "Transaction History":
    st.subheader("Transaction History")
    ac_no = st.text_input("Enter Account Number:")
    pin = st.number_input("Enter 4-digit PIN:", min_value=1000, max_value=9999, step=1)

    if st.button("View Transaction History"):
        if ac_no in st.session_state["accounts"]:
            account = st.session_state["accounts"][ac_no]
            history = account.get_transactions(pin)
            for t in history:
                st.write(f"- {t}")
        else:
            st.error("Account not found. Please check the account number.")
