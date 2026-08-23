import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

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
    print("Expense added successfully!")

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
    print(f"\n All expenses under '{target_category}' has been removed successfully!")

def main():
    while True:
        print("=== Personal Expense Tracker CLI ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Summary by Category")
        print("4. View Expense by Category")
        print("5. Remove Expense")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ").strip()
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
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, 5 or 6.\n")

if __name__ == "__main__":
    main()