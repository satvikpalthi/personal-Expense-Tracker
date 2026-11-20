import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    """Load saved expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read expenses.json. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save all expenses to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    print("\n--- Add Expense ---")
    date_text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()

    if not date_text:
        date_text = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            return

    category = input("Category (Food, Travel, Shopping, Bills, Other): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()
    amount = get_amount("Amount (₹): ")

    expense = {
        "date": date_text,
        "category": category.title(),
        "description": description,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")


def view_expenses(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'No.':<5}{'Date':<13}{'Category':<15}{'Amount (₹)':>12}  Description")
    print("-" * 70)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<5}{expense['date']:<13}{expense['category']:<15}"
            f"{expense['amount']:>12.2f}  {expense['description']}"
        )

    total = sum(item["amount"] for item in expenses)
    print("-" * 70)
    print(f"Total expenses: ₹{total:.2f}")


def show_total(expenses):
    total = sum(item["amount"] for item in expenses)
    print(f"\nTotal expenses: ₹{total:.2f}")


def search_by_category(expenses):
    category = input("\nEnter category to search: ").strip().casefold()
    matches = [
        item for item in expenses
        if item["category"].casefold() == category
    ]

    if not matches:
        print("No expenses found in that category.")
        return

    print(f"\nExpenses in {category.title()}:")
    for item in matches:
        print(
            f"{item['date']} | ₹{item['amount']:.2f} | "
            f"{item['description']}"
        )

    total = sum(item["amount"] for item in matches)
    print(f"Category total: ₹{total:.2f}")


def monthly_summary(expenses):
    month = input("\nEnter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM, for example 2026-11.")
        return

    matches = [item for item in expenses if item["date"].startswith(month)]
    total = sum(item["amount"] for item in matches)

    print(f"\n--- Summary for {month} ---")
    print(f"Number of expenses: {len(matches)}")
    print(f"Total spending: ₹{total:.2f}")

    if matches:
        category_totals = {}
        for item in matches:
            category = item["category"]
            category_totals[category] = (
                category_totals.get(category, 0) + item["amount"]
            )

        print("Spending by category:")
        for category, amount in sorted(category_totals.items()):
            print(f"- {category}: ₹{amount:.2f}")


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return

    try:
        number = int(input("\nEnter the expense number to delete: "))
        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return
    except ValueError:
        print("Please enter a valid whole number.")
        return

    removed = expenses.pop(number - 1)
    save_expenses(expenses)
    print(f"Deleted expense: {removed['category']} - ₹{removed['amount']:.2f}")


def main():
    expenses = load_expenses()

    while True:
        print("\n========== PERSONAL EXPENSE TRACKER ==========")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Show total expenses")
        print("4. Search by category")
        print("5. Monthly summary")
        print("6. Delete an expense")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            search_by_category(expenses)
        elif choice == "5":
            monthly_summary(expenses)
        elif choice == "6":
            delete_expense(expenses)
        elif choice == "7":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
