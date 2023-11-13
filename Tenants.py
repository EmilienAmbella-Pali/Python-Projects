import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# Define the rent for each tenant in a dictionary
tenant_rents = {
    "Tenant_1": {"rent": 450, "payment_day": 24},
    "Tenant_2": {"rent": 450, "payment_day": 15},
    "Tenant_3": {"rent": 600, "payment_day": 5},
    "Tenant_4": {"rent": 1000, "payment_day": 15},
    "Tenant_5": {"rent": 400, "payment_day": 15},
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

def calculate_accumulated_savings():
    accumulated_savings = 0
    total_expenses_up_to_month = 0
    for month in range(1, current_month + 1):
        total_income_month = sum(tenant_rents[tenant]["rent"] for tenants in payment_schedule.values() for tenant in tenants)
        total_expenses_month = sum(monthly_expenses[expense] for expense in monthly_expenses)
        accumulated_savings += total_income_month + total_expenses_month
        total_expenses_up_to_month += total_expenses_month
    return accumulated_savings, total_expenses_up_to_month

# Function to get miscellaneous expenses from the user
def get_miscellaneous_expenses():
    try:
        amount = simpledialog.askfloat("Miscellaneous Expenses", "Enter miscellaneous expenses for the month:")
        monthly_expenses["miscellaneous"] = -amount
        update_savings()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for miscellaneous expenses.")

# Function to create a new window with a larger text font
def create_summary_window(title, content, font_size):
    summary_window = tk.Toplevel(root)
    summary_window.title(title)
    label = tk.Label(summary_window, text=content, font=("Helvetica", font_size))
    label.pack()

# Function to add tenants
def add_tenants():
    tenant_name = simpledialog.askstring("Add Tenant", "Enter the name of the new tenant:")
    if tenant_name:
        rent = simpledialog.askinteger("Add Tenant", f"Enter the monthly rent for {tenant_name}:")
        if rent is not None:
            payment_day = simpledialog.askinteger("Add Tenant", f"Enter the payment day for {tenant_name} (1-31):")
            if 1 <= payment_day <= 31:
                tenant_rents[tenant_name] = {"rent": rent, "payment_day": payment_day}
                update_savings()

# Function to edit or remove tenants
def edit_tenants():
    tenant_name = simpledialog.askstring("Edit Tenant", "Enter the name of the tenant to edit:")
    if tenant_name in tenant_rents:
        action = simpledialog.askstring("Edit Tenant", f"Select action for {tenant_name}:\n\n"
                                                         "1. Edit Tenant\n"
                                                         "2. Delete Tenant\n")
        if action == "1":
            new_rent = simpledialog.askinteger("Edit Tenant", f"Enter the new monthly rent for {tenant_name}:",
                                               initialvalue=tenant_rents[tenant_name]["rent"])
            if new_rent is not None:
                new_payment_day = simpledialog.askinteger("Edit Tenant", f"Enter the new payment day for {tenant_name} (1-31):",
                                                          initialvalue=tenant_rents[tenant_name]["payment_day"])
                if 1 <= new_payment_day <= 31:
                    tenant_rents[tenant_name]["rent"] = new_rent
                    tenant_rents[tenant_name]["payment_day"] = new_payment_day
                    update_savings()
        elif action == "2":
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {tenant_name}?")
            if confirm:
                del tenant_rents[tenant_name]
                update_savings()
    else:
        messagebox.showerror("Error", f"Tenant '{tenant_name}' not found.")

# Function to update the total expenses and savings
def update_savings():
    total_expenses = sum(monthly_expenses.values())
    global savings_up_to_date  # Access the global savings variable
    savings_up_to_date = total_income + total_expenses
    show_savings.set(f"Accumulated Capital up to month {current_month}: £{savings_up_to_date}")

# Function to display the annual financial summary
def show_annual_summary():
    accumulated_savings, total_expenses_up_to_month = calculate_accumulated_savings()

    # Display the annual summary
    annual_summary = f"Accumulated Capital up to month {current_month}: £{accumulated_savings}\n"
    annual_summary += f"Total Expenses up to month {current_month}: £{total_expenses_up_to_month}"
    create_summary_window("Annual Financial Summary", annual_summary, 14)  # 14 is the font size

# Function to display the monthly financial summary
def show_monthly_summary():
    financial_summary = f"Monthly Financial Summary for Month {current_month}:\n\n"

    # Monthly Income
    financial_summary += "Monthly Income:\n"
    total_monthly_income = 0
    for tenant, data in tenant_rents.items():
        financial_summary += f"{tenant}: £{data['rent']} (Due on {data['payment_day']}th)\n"
        total_monthly_income += data["rent"]

    financial_summary += f"Total Income: £{total_monthly_income}\n\n"

    # Expenses
    financial_summary += "Expenses:\n"
    for expense, amount in monthly_expenses.items():
        financial_summary += f"{expense}: £{amount}\n"
    total_expenses_month = -sum(monthly_expenses.values())
    financial_summary += f"Total Expenses: £{total_expenses_month}\n\n"

    financial_summary += f"Savings for month {current_month}: £{savings_up_to_date}"

    create_summary_window("Monthly Financial Summary", financial_summary, 14)  # 14 is the font size

# Initialize the GUI window
root = tk.Tk()
root.title("Property Management App")

# Create a button to input miscellaneous expenses
miscellaneous_expenses_button = tk.Button(root, text="Enter Miscellaneous Expenses", command=get_miscellaneous_expenses, width=30, height=2)
miscellaneous_expenses_button.pack()

# Create a button to display the annual financial summary
show_annual_summary_button = tk.Button(root, text="Show Annual Financial Summary", command=show_annual_summary, width=30, height=2)
show_annual_summary_button.pack()

# Create a button to add tenants (placed below the annual summary button)
add_tenants_button = tk.Button(root, text="Add Tenants", command=add_tenants, width=30, height=2)
add_tenants_button.pack()

# Create a button to edit or remove tenants (placed below the add tenants button)
edit_tenants_button = tk.Button(root, text="Edit Tenants", command=edit_tenants, width=30, height=2)
edit_tenants_button.pack()

# Create a button to display the monthly financial summary
show_summary_button = tk.Button(root, text="Show Monthly Financial Summary", command=show_monthly_summary, width=30, height=2)
show_summary_button.pack()

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
            total_income += tenant_rents[tenant]["rent"]

# Calculate accumulated savings
accumulated_savings, _ = calculate_accumulated_savings()

# Create a label to display savings
show_savings = tk.StringVar()
show_savings.set(f"Accumulated Capital up to month {current_month}: £{accumulated_savings}")
savings_label = tk.Label(root, textvariable=show_savings)
savings_label.pack()

# Run the GUI application
root.mainloop()
