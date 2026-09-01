import json
import os
from datetime import datetime
import hashlib
import getpass
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "expenses.json"
USER_FILE = "users.json"
BUDGET_FILE = "budgets.json"

#--------------------------users.json(Starting)------------------------------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    try:
        with open(USER_FILE, "r") as file:                
            return json.load(file)
    except json.JSONDecodeError:
        return {}
    
def save_users(users_data):
    with open(USER_FILE, "w") as file:
        json.dump(users_data, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user():
    users = load_users()

    print("---Register New Account---")
    username = input("Choose a Username: ")

    if username in users:
        print("Username already exists.")
        return

    password = getpass.getpass("Choose a Password: ")

    users[username] = {"password_hash":hash_password(password)}
    save_users(users)
    print("Account registered and saved successfully!")

def get_and_verify_user():
    users = load_users()

    if not users:
        print("No accounts found.Let's create one first!")
        register_user()
        users = load_users()

    print("---Secure Login Required---")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    if username not in users:
        print("\nAccess Denied: User not found.")
        return False

    stored_hash = users[username]["password_hash"]
    current_attempt_hash = hash_password(password)

    if current_attempt_hash == stored_hash :
        print("\nAccess Granted: Welcome to your Expense Tracker\n")
        return True
    else:
        print("\nAccess Denied: Incorrect password")
        return False
#---------------------------users.json(Ending)-------------------------------

#--------------------------expenses.json(Starting)------------------------------
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
            
    category = input("Enter category (e.g., Food, Travel, Books): ").strip().capitalize()
    
    while True:
        try:
            amount = float(input("Enter amount (€ or ₹): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    description = input("Enter description (optional): ").strip()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
 
    expenses = load_expenses()
    expenses.append({
        "id": len(expenses) + 1,
        "date": date_str,
        "category": category,
        "amount": amount,
        "description": description
    })
    save_expenses(expenses)
    print("Expense added successfully!\n")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    print("\n--- All Expenses ---")
    print(f"{'ID':<4} | {'Date':<16} | {'Category':<12} | {'Amount':<8} | {'Description'}")
    print("-" * 60)
    for item in expenses:
        print(f"{item['id']:<4} | {item['date']:<16} | {item['category']:<12} | {item['amount']:<8.2f} | {item['description']}")
    print("-" * 60 + "\n")

def view_summary():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    total_spent = sum(item["amount"] for item in expenses)
    category_totals = {}
    for item in expenses:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + item["amount"]

    print("\n--- Expense Summary ---")
    print(f"Total Expenditure: {total_spent:.2f}")
    print("Category Breakdown:")
    for cat, total in category_totals.items():
        percentage = (total / total_spent) * 100
        print(f"  • {cat}: {total:.2f} ({percentage:.1f}%)")
    print("-" * 25 + "\n")

def searchExpense():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    target_category = input("Enter the category you want to search: ").strip().capitalize()
    category_exists = [item for item in expenses if item["category"] == target_category]

    if not category_exists:
        print(f"\nNo expenses found by category : '{target_category}'.\n")
        return

    print("\n--- Expense Found ---")
    print(f"{'ID':<4} | {'Date':<16} | {'Category':<12} | {'Amount':<8} | {'Description'}")
    print("-" * 60)
    for item in category_exists:
        print(f"{item['id']:<4} | {item['date']:<16} | {item['category']:<12} | {item['amount']:<8.2f} | {item['description']}")
    print("-" * 60 + "\n")

def remove_expense():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return
    
    target_category = input("Enter the category you want to remove(e.g., Food): ").strip().capitalize()

    category_exists = any(item["category"] == target_category for item in expenses)

    if not category_exists:
        print(f"\nNo expenses found under the category '{target_category}'.\n")
        return

    updated_expense = [item for item in expenses if item["category"] != target_category]

    save_expenses(updated_expense)
    print(f"\n All expenses under '{target_category}' has been removed successfully!\n")

def visual_expenses():
    expenses = pd.read_json("expenses.json")

    expense = load_expenses()
    if not expense:
        print("\nNo expenses recorded yet.\n")
        return
    

    print("Pie chart for Overall Expenses\n")
    overall_expenses = expenses.groupby("category")["amount"].sum()
    plt.pie(overall_expenses, labels=overall_expenses.index, autopct="%1.1f%%")
    plt.title("For all Expenses")
    plt.show()

    print("Pie chart for Monthly Expenses\n")
    current_month = datetime.now().strftime("%Y-%m")
    monthly_expenses = expenses[expenses['date'].dt.strftime("%Y-%m") == current_month] 

    if not monthly_expenses.empty:
        monthly_totals = monthly_expenses.groupby("category")["amount"].sum()
        plt.pie(monthly_totals, labels=monthly_totals.index, autopct="%1.1f%%")
        plt.title(f"Expenses for {current_month}")
        plt.show()
    else:
        print("No expenses of current month recorded yet.\n")

    print("Bar chart for Yearly Expenses\n")
    current_year = datetime.now().strftime("%Y")
    yearly_expenses = expenses[expenses['date'].dt.strftime("%Y") == current_year]

    if not yearly_expenses.empty:
        yearly_totals = yearly_expenses.groupby(yearly_expenses['date'].dt.strftime("%B"))['amount'].sum()
        month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        yearly_totals = yearly_totals.reindex(month_order).dropna()

        plt.bar(yearly_totals.index, yearly_totals.values, color='skyblue', edgecolor='black')
        plt.xlabel("Months")
        plt.ylabel("Expenses")
        plt.title(f"Monthly Breakdown for {current_year}")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()
    else:
        print("No expenses of current year recorded yet.\n")
    

def expenses_calculator():
    expenses = load_expenses()

    #Overall Expenses 
    total_expenses = sum(item["amount"] for item in expenses)
    print(f"\nTotal expenses upto today: {total_expenses}")

    #Monthly Expenses
    current_month = datetime.now().strftime("%Y-%m")
    monthly_expenses = sum(item["amount"] for item in expenses  if item["date"].startswith(current_month)) 
    print(f"Total Monthly Expenses: {monthly_expenses}")

    #Yearly Expenses
    current_year = datetime.now().strftime("%Y")
    yearly_expenses = sum(item["amount"] for item in expenses if item["date"].startswith(current_year))
    print(f"Total Yearly Expenses: {yearly_expenses}\n")
#---------------------------expenses.json(Ending)-------------------------------

#--------------------------budgets.json(Starting)------------------------------
def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return []
    try:
        with open(BUDGET_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_budgets(budgets):
    with open(BUDGET_FILE, "w") as file:
        json.dump(budgets, file, indent=4)

def add_monthly_budget():

    budgets = load_budgets()

    current_month = datetime.now().strftime("%Y-%m")

    for budget in budgets:
        if budget.get("date", "").startswith(current_month) :
            print(f"Error: A Budget for {current_month} already exists. You cannot add another one.")
            print("Instead, you can update budget in 'Update Budget' section.\n")
            return

    print("\nNote: You can neither add another budget for same month twice nor can remove the budget.\n")
    while True:
        try:
            amount = float(input("Enter amount to add for budget of current month(€ or ₹): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    description = input("Enter description (optional): ").strip()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
 
    budgets.append({
        "id": len(budgets) + 1,
        "date": date_str,
        "amount": amount,
        "description": description
    })
    save_budgets(budgets)
    print("Budget added successfully!\n")


def add_yearly_budget():
    budgets = load_budgets()

    current_year = datetime.now().strftime("%Y")

    for budget in budgets:
        if budget.get("year", "").startswith(current_year):
            print(f"Error: A Budget for {current_year} already exists. You cannot add another one.")
            print("Instead, you can update budget in 'Update Budget' section.")
            return

    print("Note: You can neither add another budget for same year twice nor can remove the budget.")
    while True:
        try:
            amount = float(input("Enter amount to add for budget of current year(€ or ₹): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    description = input("Enter description (optional): ").strip()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
 
    budgets.append({
        "id": len(budgets) + 1,
        "date": date_str,
        "amount": amount,
        "description": description
    })
    save_budgets(budgets)
    print("Budget added successfully!\n")
#---------------------------budgets.json(Ending)-------------------------------

def main():

    if get_and_verify_user():

        while True:
            print("=== Personal Expense Tracker CLI ===")
            print("1. Expense Account")
            print("2. Savings Account")
            print("3. Exit")

            choice = input("Select an option(1, 2 or 3): ").strip()

            if choice == "1":
                while True:
                    print("---Expense Account---")
                    print("1. Add Expense")
                    print("2. View All Expenses")
                    print("3. View Summary by Category")
                    print("4. Search Expense by Category")
                    print("5. Remove Expense")
                    print("6. View Visual Reports")
                    print("7. Calculate Monthly/Yearly and Overall Expenses")
                    print("8. Main Menu")
        
                    choice = input("Select an option (1-8): ").strip()
                    if choice == "1":
                        add_expense()
                    elif choice == "2":
                        view_expenses()
                    elif choice == "3":
                        view_summary()
                    elif choice == "4":
                        searchExpense()
                    elif choice == "5":
                        remove_expense()
                    elif choice == "6":
                        visual_expenses()
                    elif choice =="7":
                        expenses_calculator()
                    elif choice == "8":
                        print("Back to Main Menu...\n")
                        break
                    else:
                        print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, 7 or 8.\n")

            elif choice == "2":
                while True: 
                    print("---Savings Account---")
                    print("1. Add Monthly Budget")
                    print("2. Add Yearly Budget")
                    print("3. View All Budgets")
                    print("4. Search Budget by Month")
                    print("5. Update Budget")
                    print("6. View Visual Reports")
                    print("7. Calculate Savings and Projections")
                    print("8. Main Menu")
        
                    choice = input("Select an option (1-8): ").strip()
                    if choice == "1":
                        add_monthly_budget()
                    elif choice == "2":
                        add_yearly_budget()
                    elif choice == "3":
                        print("Back to Main Manu...\n")
                        break
                    else:
                        print("Invalid choice. Please select 1, 2 , or 3.\n")

            elif choice == "3":
                print("Exiting program. Goodbye!\n")
                break;

            else:
                print("Invalid choice. Please enter 1, 2 or 3.")
        
if __name__ == "__main__":
    main()