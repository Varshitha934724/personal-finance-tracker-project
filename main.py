import csv
import os

# -------------------------------
# Base Class: Transaction
# -------------------------------
class Transaction:
    def __init__(self, amount, category, date_str, description=""):
        self.amount = amount
        self.category = category
        self.date = date_str
        self.description = description

    def get_type(self):
        return self.__class__.__name__


# -------------------------------
# Derived Classes
# -------------------------------
class Income(Transaction):
    pass


class Expense(Transaction):
    pass


# -------------------------------
# Account Class
# -------------------------------
class Account:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.transactions = []
        self._load_transactions()

    def _load_transactions(self):
        """Load existing transactions from CSV file."""
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Type'] == "Income":
                        tx = Income(float(row['Amount']), row['Category'], row['Date'], row['Description'])
                    else:
                        tx = Expense(float(row['Amount']), row['Category'], row['Date'], row['Description'])
                    self.transactions.append(tx)

    def add_transaction(self, transaction):
        """Add new transaction and append it to the CSV file."""
        self.transactions.append(transaction)
        with open(self.filename, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # If file is new, write header
            if file.tell() == 0:
                writer.writerow(["Date", "Type", "Category", "Description", "Amount"])
            writer.writerow([transaction.date, transaction.get_type(), transaction.category, transaction.description, transaction.amount])

    def show_all_transactions(self):
        """Display all transactions."""
        print("\nDate       | Type     | Category   | Amount   | Description")
        print("------------------------------------------------------------")
        for tx in self.transactions:
            print(f"{tx.date} | {tx.get_type():8} | {tx.category:10} | ₹{tx.amount:.2f} | {tx.description}")
        print("------------------------------------------------------------")
        total_income = sum(tx.amount for tx in self.transactions if isinstance(tx, Income))
        total_expense = sum(tx.amount for tx in self.transactions if isinstance(tx, Expense))
        balance = total_income - total_expense
        print(f"Total Income: ₹{total_income:.2f}")
        print(f"Total Expense: ₹{total_expense:.2f}")
        print(f"Current Balance: ₹{balance:.2f}\n")


# -------------------------------
# User Interface
# -------------------------------
def main():
    account = Account()

    while True:
        print("\n📊 PERSONAL FINANCE TRACKER")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Exit")


        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            date_str = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Salary, Bonus): ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: ₹"))
            tx = Income(amount, category, date_str, description)
            account.add_transaction(tx)
            print("✅ Income added successfully!")

        elif choice == "2":
            date_str = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Food, Rent, Travel): ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: ₹"))
            tx = Expense(amount, category, date_str, description)
            account.add_transaction(tx)
            print("✅ Expense added successfully!")

        elif choice == "3":
            account.show_all_transactions()

        elif choice == "4":
            print("💾 Exiting... Your data is saved in 'transactions.csv'.")
            break

        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()