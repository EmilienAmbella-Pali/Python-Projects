import datetime
import tkinter as tk
from tkinter import simpledialog

# Define the rent for each tenant in a dictionary
tenant_rents = {
    "Tenant_1": 450,
    "Tenant_2": 450,
    "Tenant_3": 600,
    "Tenant_4": 1000,
    "Tenant_5": 400,
}

# Define a dictionary to store monthly expenses
monthly_expenses = {
    "gas": -150,
    "electricity": -200,
    "council_tax": -150,
    "wifi": -30,
    "miscellaneous": 0
}

# Create a dictionary to map payment months to tenant names
payment_schedule = {
    1: ["Tenant_3", "Tenant_5"],
    2: ["Tenant_2", "Tenant_4", "Tenant_1"]
}

# Function to get miscellaneous expenses from the user
def get_miscellaneous_expenses():
    amount = simpledialog.askfloat("Miscellaneous Expenses", "Enter miscellaneous expenses for the month:")
    monthly_expenses["miscellaneous"] = -amount
    update_savings()

# Function to create a new window with a larger text font
def create_summary_window(title, content, font_size):
    summary_window = tk.Toplevel(root)
    summary_window.title(title)
    label = tk.Label(summary_window, text=content, font=("Helvetica", font_size))
    label.pack()

# Initialize the GUI window
root = tk.Tk()
root.title("Property Management App")

# Create a button to input miscellaneous expenses
miscellaneous_expenses_button = tk.Button(root, text="Enter Miscellaneous Expenses", command=get_miscellaneous_expenses, width=30, height=2)
miscellaneous_expenses_button.pack()

# Get the current month
current_month = datetime.datetime.now().month

# Initialize variables for total income and expenses
total_income = 0
total_expenses = 0
savings_up_to_date = 0  # Define savings as a global variable

# Calculate the total income based on the current month and payment schedule
for payment_month, tenants in payment_schedule.items():
    if current_month >= payment_month:
        for tenant in tenants:
            total_income += tenant_rents.get(tenant, 0)

# Function to update the total expenses and savings
def update_savings():
    global savings_up_to_date  # Access the global savings variable
    total_expenses = sum(monthly_expenses.values())
    savings_up_to_date = total_income + total_expenses
    show_savings.set(f"Accumulated Capital up to month {current_month}: £{savings_up_to_date}")

# Calculate accumulated savings
accumulated_savings = 0
for month in range(1, current_month + 1):
    total_income_month = sum(tenant_rents.get(tenant, 0) for tenants in payment_schedule.values() for tenant in tenants)
    total_expenses_month = sum(monthly_expenses[expense] for expense in monthly_expenses)
    accumulated_savings += total_income_month + total_expenses_month

# Create a label to display savings
show_savings = tk.StringVar()
show_savings.set(f"Accumulated Capital up to month {current_month}: £{accumulated_savings}")
savings_label = tk.Label(root, textvariable=show_savings)
savings_label.pack()

# Function to display the monthly financial summary
def show_monthly_summary():
    monthly_expense_values = list(monthly_expenses.values())
    total_expenses = -sum(monthly_expense_values)
    monthly_income = total_income  # Calculate monthly income

    financial_summary = f"Monthly Financial Summary for Month {current_month}:\n\n"

    # Monthly Income
    financial_summary += "Monthly Income:\n"
    for tenant, rent in tenant_rents.items():
        financial_summary += f"{tenant}: £{rent}\n"
    financial_summary += f"Total Income: £{monthly_income}\n\n"

    # Expenses
    financial_summary += "Expenses:\n"
    for expense, amount in monthly_expenses.items():
        financial_summary += f"{expense}: £{amount}\n"
    financial_summary += f"Total Expenses: £{total_expenses}\n\n"

    financial_summary += f"Savings for month {current_month}: £{savings_up_to_date}"

    create_summary_window("Monthly Financial Summary", financial_summary, 14)  # 14 is the font size

# Create a button to display the monthly financial summary
show_summary_button = tk.Button(root, text="Show Monthly Financial Summary", command=show_monthly_summary, width=30, height=2)
show_summary_button.pack()

# Function to display the annual financial summary
def show_annual_summary():
    # Calculate accumulated savings and total expenses from January to the current month
    accumulated_savings = 0
    total_expenses_up_to_month = 0
    for month in range(1, current_month + 1):
        total_income_month = sum(tenant_rents.get(tenant, 0) for tenants in payment_schedule.values() for tenant in tenants)
        total_expenses_month = sum(monthly_expenses[expense] for expense in monthly_expenses)
        accumulated_savings += total_income_month + total_expenses_month
        total_expenses_up_to_month += total_expenses_month

    # Display the annual summary
    annual_summary = f"Accumulated Capital up to month {current_month}: £{accumulated_savings}\n"
    annual_summary += f"Total Expenses up to month {current_month}: £{total_expenses_up_to_month}"
    create_summary_window("Annual Financial Summary", annual_summary, 14)  # 14 is the font size

# Create a button to display the annual financial summary
show_annual_summary_button = tk.Button(root, text="Show Annual Financial Summary", command=show_annual_summary, width=30, height=2)
show_annual_summary_button.pack()

# Run the GUI application
root.mainloop()
