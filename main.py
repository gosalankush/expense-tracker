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
    

    print("- Displaying Pie chart for Overall Expenses -\n")
    overall_expenses = expenses.groupby("category")["amount"].sum()
    plt.pie(overall_expenses, labels=overall_expenses.index, autopct="%1.1f%%")
    plt.title("For all Expenses")
    plt.show()

    print("- Displaying Pie chart for Monthly Expenses -\n")
    current_month = datetime.now().strftime("%Y-%m")
    monthly_expenses = expenses[expenses['date'].dt.strftime("%Y-%m") == current_month] 

    if not monthly_expenses.empty:
        monthly_totals = monthly_expenses.groupby("category")["amount"].sum()
        plt.pie(monthly_totals, labels=monthly_totals.index, autopct="%1.1f%%")
        plt.title(f"Expenses for {current_month}")
        plt.show()
    else:
        print("No expenses of current month recorded yet.\n")

    print("- Displaying Bar chart for Yearly Expenses -\n")
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

def expenses_csv():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    df = pd.DataFrame(expenses)

    filename = f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    df.to_csv(filename, index=False)
    print(f"\nExpenses successfully exported to '{filename}'!\n")
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

    current_month = datetime.now().strftime("%m")

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
    date_str = datetime.now().strftime("%m-%d %H:%M")
 
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

def update_monthly_budget():
    budgets = load_budgets()

    current_month = datetime.now().strftime("%m-%d")

    for budget in budgets:
        if budget.get("date", "").startswith(current_month):
            while True:
                    try:
                        upd_amount = float(input("Enter amount for New Budget of Current Month(€ or ₹): "))
                        if upd_amount <= 0:
                            print("Amount must be greater than zero.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            budget["amount"] = upd_amount
            save_budgets(budgets)
            print(f"Budget of {current_month} has successfully updated.\n")
            return

    print(f"No budget for {current_month} exists. You can add one in 'Add Budget' section.\n")


def update_yearly_budget():

    budgets = load_budgets()

    current_year = datetime.now().strftime("%Y")

    for budget in budgets:
        if budget.get("year", "").startswith(current_year):
            while True:
                    try:
                        upd_amount = float(input("Enter amount for New Budget of Current Year(€ or ₹): "))
                        if upd_amount <= 0:
                            print("Amount must be greater than zero.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            budget["amount"] = upd_amount
            save_budgets(budgets)
            print(f"Budget of {current_year} has successfully updated.\n")
            return

    print(f"No budget for {current_year} exists. You can add one in 'Add Budget' section.\n")

def view_budgets():
    budgets = load_budgets()
    if not budgets:
        print("\nNo budgets recorded yet.\n")
        return

    current_month = datetime.now().strftime("%m-%d")
    current_year = datetime.now().strftime("%Y")

    print("\n--- All Budgets ---")

    for item in budgets:
        if item.get("date", "").startswith(current_month):
            print("- Monthly Budgets -")
            print(f"{'ID':<4} | {'Date':<16} | {'Amount':<8} | {'Description'}")
            print("-" * 60)
            print(f"{item['id']:<4} | {item['date']:<16} | {item['amount']:<8.2f} | {item['description']}")

    for item in budgets:
        if item.get("year", "").startswith(current_year):
            print("- Yearly Budgets -")
            print(f"{'ID':<4} | {'Date':<16} | {'Amount':<8} | {'Description'}")
            print("-" * 60)
            print(f"{item['id']:<4} | {item['date']:<16} | {item['amount']:<8.2f} | {item['description']}")
    print("-" * 60 + "\n")

def savings_calculator():

    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return 

    budgets = load_budgets()
    if not budgets:
        print("\nNo budgets recorded yet.\n")
        return

    #Overall Expenses 
    total_expenses = sum(item["amount"] for item in expenses)
    total_budgets = sum(item["amount"] for item in budgets)
    total_savings = total_budgets - total_expenses
    if total_expenses > total_budgets:
        print("Overall, you got no savings.")
        print("Try to do less expenses!\n")
    else:
        print(f"\nTotal expenses upto Today: {total_expenses}")
        print(f"Total Savings upto Today: {total_savings}\n")

    #Monthly Expenses
    current_month = datetime.now().strftime("%m-%d")
    current_month_expenses = datetime.now().strftime("%Y-%m")
    monthly_expenses = sum(item["amount"] for item in expenses  if item["date"].startswith(current_month_expenses))
    monthly_budgets = sum(item["amount"] for item in budgets if item["date"].startswith(current_month))
    monthly_savings = monthly_budgets - monthly_expenses

    if not monthly_budgets:
        print("You didn't set budget for this month yet.\n")
    else:
        if monthly_expenses > monthly_budgets:
            print("You got no savings this month.\n")
        else: 
            print(f"Total Monthly Expenses: {monthly_expenses}")
            print(f"Total Monthly Savings: {monthly_savings}\n")

    #Yearly Expenses
    current_year = datetime.now().strftime("%Y")
    yearly_expenses = sum(item["amount"] for item in expenses if item["date"].startswith(current_year))
    yearly_budgets = sum(item["amount"] for item in budgets if item["date"].startswith(current_year))
    yearly_savings = yearly_budgets - yearly_expenses

    if not yearly_budgets:
        print("You didn't set budget for this year yet.\n")
    else:
        if yearly_expenses > yearly_budgets:
            print("You got no savings this year.\n")
        else: 
            print(f"Total Yearly Expenses: {yearly_expenses}")
            print(f"Total Yearly Savings: {yearly_savings}\n")

    choice = input("Do you want to run a Projection?(Y/y for Yes!) ").strip().capitalize()

    p_total_mexpenses = 0.0
    for item in expenses:
        p_monthly_expenses = item["amount"]
        p_total_mexpenses += p_monthly_expenses

    p_total_mbudgets = 0.0
    for item in budgets:
        p_monthly_budgets = item["amount"]
        p_total_mbudgets += p_monthly_budgets

    if p_total_mexpenses > p_total_mbudgets:
        print("Error: You have either missed to set any monthly budget (If yes, then remove expenses of that month.)")
        print("Or you need to lower your expenses for calculating this!\n")
        return

    total_psavings = p_total_mbudgets - p_total_mexpenses
        
    if choice =="Y":
        target = float(input("Enter your target amount: "))
        complete = target/total_psavings
        print(f"You will reach your target in {complete:.1F} months.")
        print("Keep Going!\n")

def visual_budgets():
    expenses = load_expenses()
    budgets = load_budgets()

    if not expenses and not budgets:
        print("\nNo budgets or expenses recorded yet to display visuals.\n")
        return

    expenses_df = pd.DataFrame(expenses)
    budgets_df = pd.DataFrame(budgets)

    current_month_str = datetime.now().strftime("%m") 
    current_year_str = datetime.now().strftime("%Y")   

    total_m_expense = 0.0
    if not expenses_df.empty and 'date' in expenses_df.columns:
        m_exp = expenses_df[expenses_df['date'].str.startswith(f"{current_year_str}-{current_month_str}")]
        total_m_expense = m_exp['amount'].sum() if not m_exp.empty else 0.0

    total_m_budget = 0.0
    if not budgets_df.empty and 'date' in budgets_df.columns:
        m_bud = budgets_df[budgets_df['date'].str.startswith(f"{current_month_str}-")]
        total_m_budget = m_bud['amount'].sum() if not m_bud.empty else 0.0

    total_m_savings = total_m_budget - total_m_expense

    print("\n- Displaying Current Month Visual Report -")
    categories = ['Total Budget', 'Total Expenses', 'Savings']
    values = [total_m_budget, total_m_expense, total_m_savings]
    colors = ['#4CAF50', '#F44336', '#2196F3' if total_m_savings >= 0 else '#FF9800']

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, values, color=colors, edgecolor='black', width=0.5)

    for bar in bars:
        yval = bar.get_height()
        va_pos = 'bottom' if yval >= 0 else 'top'
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', ha='center', va=va_pos)

    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.ylabel("Amount (€ / ₹)")
    plt.title(f"Monthly Savings Breakdown (Month {current_month_str})")
    plt.tight_layout()
    plt.show()

    print("\n- Displaying Yearly Month-by-Month Savings Report -")
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_expenses = [0.0] * 12
    monthly_budgets = [0.0] * 12

    if not expenses_df.empty and 'date' in expenses_df.columns:
        expenses_df['date_dt'] = pd.to_datetime(expenses_df['date'], errors='coerce')
        year_exp = expenses_df[expenses_df['date_dt'].dt.strftime("%Y") == current_year_str]
        for _, row in year_exp.iterrows():
            if pd.notnull(row['date_dt']):
                m_idx = row['date_dt'].month - 1
                monthly_expenses[m_idx] += row['amount']

    if not budgets_df.empty and 'date' in budgets_df.columns:
        for _, row in budgets_df.iterrows():
            date_str = str(row['date'])
            try:
                m_num = int(date_str.split('-')[0])
                if 1 <= m_num <= 12:
                    monthly_budgets[m_num - 1] += row['amount']
            except (ValueError, IndexError):
                continue

    yearly_savings = [b - e for b, e in zip(monthly_budgets, monthly_expenses)]

    plt.figure(figsize=(10, 5))
    bar_colors = ['#4CAF50' if s >= 0 else '#F44336' for s in yearly_savings]
    yearly_bars = plt.bar(months, yearly_savings, color=bar_colors, edgecolor='black', width=0.6)

    for bar in yearly_bars:
        yval = bar.get_height()
        if yval != 0:
            va_pos = 'bottom' if yval >= 0 else 'top'
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.0f}', ha='center', va=va_pos, fontsize=8)

    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.xlabel("Months")
    plt.ylabel("Savings (€ / ₹)")
    plt.title(f"Month-by-Month Savings Breakdown ({current_year_str})")
    plt.tight_layout()
    plt.show()

def budgets_csv():
    budgets = load_budgets()
    if not budgets:
        print("\nNo budgets recorded yet.")
        return

    df = pd.DataFrame(budgets)

    filename = f"budgets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    df.to_csv(filename, index=False)
    print(f"\nBudgets successfully exported to '{filename}'!\n")
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
                    print("8. Export Expenses to CSV file")
                    print("9. Main Menu")
        
                    choice = input("Select an option (1-9): ").strip()
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
                        expenses_csv()
                    elif choice == "9":
                        print("Back to Main Menu...\n")
                        break
                    else:
                        print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, 7, 8 or 9.\n")

            elif choice == "2":
                while True: 
                    print("---Savings Account---")
                    print("1. Add Monthly Budget")
                    print("2. Add Yearly Budget")
                    print("3. Update Monthly Budget")
                    print("4. Update Yearly Budget")
                    print("5. View All Budgets")
                    print("6. View Visual Reports")
                    print("7. Calculate Savings and Projections")
                    print("8. Export Budgets to CSV file")
                    print("9. Main Menu")
        
                    choice = input("Select an option (1-9): ").strip()
                    if choice == "1":
                        add_monthly_budget()
                    elif choice == "2":
                        add_yearly_budget()
                    elif choice == "3":
                        update_monthly_budget()
                    elif choice == "4":
                        update_yearly_budget()
                    elif choice == "5":
                        view_budgets()
                    elif choice == "6":
                        visual_budgets()
                    elif choice == "7":
                        savings_calculator()
                    elif choice == "8":
                        budgets_csv()
                    elif choice == "9":
                        print("Back to Main Menu...\n")
                        break
                    else:
                        print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, 7, 8 or 9.\n")

            elif choice == "3":
                print("Exiting Program ... Goodbye!\n")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2 or 3.\n")
        
if __name__ == "__main__":
    main()