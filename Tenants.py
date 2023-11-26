import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

class PropertyManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Property Management App")
        self.tenant_rents = {
            "Tenant_1": {"rent": 450, "payment_day": 24},
            "Tenant_2": {"rent": 450, "payment_day": 15},
            "Tenant_3": {"rent": 600, "payment_day": 5},
            "Tenant_4": {"rent": 1000, "payment_day": 15},
            "Tenant_5": {"rent": 400, "payment_day": 15},
        }
        self.monthly_expenses = {
            "gas": -150,
            "electricity": -200,
            "council_tax": -150,
            "wifi": -30,
            "miscellaneous": 0
        }
        self.payment_schedule = {
            1: ["Tenant_3", "Tenant_5"],
            2: ["Tenant_2", "Tenant_4", "Tenant_1"]
        }

        self.current_month = datetime.datetime.now().month
        self.total_income = 0
        self.total_expenses = 0
        self.savings_up_to_date = 0

        self.create_buttons()

    def create_buttons(self):
        miscellaneous_expenses_button = tk.Button(self.root, text="Enter Miscellaneous Expenses", command=self.get_miscellaneous_expenses, width=30, height=2)
        miscellaneous_expenses_button.pack()

        show_annual_summary_button = tk.Button(self.root, text="Show Annual Financial Summary", command=self.show_annual_summary, width=30, height=2)
        show_annual_summary_button.pack()

        create_edit_tenants_button = tk.Button(self.root, text="Create/Edit Tenants", command=self.create_edit_tenants, width=30, height=2)
        create_edit_tenants_button.pack()

        show_summary_button = tk.Button(self.root, text="Show Monthly Financial Summary", command=self.show_monthly_summary, width=30, height=2)
        show_summary_button.pack()

        self.show_savings = tk.StringVar()
        self.show_savings.set(f"Accumulated Capital up to month {self.current_month}: £{self.calculate_accumulated_savings()[0]}")
        savings_label = tk.Label(self.root, textvariable=self.show_savings)
        savings_label.pack()

    def calculate_accumulated_savings(self):
        accumulated_savings = 0
        total_expenses_up_to_month = 0
        for month in range(1, self.current_month + 1):
            total_income_month = sum(self.tenant_rents[tenant]["rent"] for tenants in self.payment_schedule.values() for tenant in tenants)
            total_expenses_month = sum(self.monthly_expenses[expense] for expense in self.monthly_expenses)
            accumulated_savings += total_income_month + total_expenses_month
            total_expenses_up_to_month += total_expenses_month
        return accumulated_savings, total_expenses_up_to_month

    def get_miscellaneous_expenses(self):
        try:
            amount = simpledialog.askfloat("Miscellaneous Expenses", "Enter miscellaneous expenses for the month:")
            self.monthly_expenses["miscellaneous"] = -amount
            self.update_savings()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for miscellaneous expenses.")

    def create_edit_tenants(self):
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Tenant Details")

        action = simpledialog.askstring("Tenants", "Select an action: \n1. Add New Tenant\n2. Edit Existing Tenant")

        if action == "1":
            # Code to add a new tenant
            tenant_name = simpledialog.askstring("Add Tenant", "Enter name of new tenant:")
            tenant_rent = simpledialog.askinteger("Add Tenant", "Enter monthly rent:")
            payment_day = simpledialog.askinteger("Add Tenant", "Enter payment day (1-31):")

            self.tenant_rents[tenant_name] = {"rent": tenant_rent, "payment_day": payment_day}

        elif action == "2":
            # Code to edit an existing tenant
            tenant_name = simpledialog.askstring("Edit Tenant", "Enter name of tenant to edit:")

            if tenant_name in self.tenant_rents:
                new_rent = simpledialog.askinteger("Edit Rent", f"Enter new rent for {tenant_name}:", initialvalue=self.tenant_rents[tenant_name]["rent"])
                new_payment_day = simpledialog.askinteger("Edit Payment Day", f"Enter new payment day for {tenant_name}:", initialvalue=self.tenant_rents[tenant_name]["payment_day"])

                self.tenant_rents[tenant_name]["rent"] = new_rent
                self.tenant_rents[tenant_name]["payment_day"] = new_payment_day

        else:
            messagebox.showerror("Error", "Invalid selection")

        self.show_savings.set(f"Accumulated Capital up to month {self.current_month}: £{self.calculate_accumulated_savings()[0]}")

    def update_savings(self):
        total_expenses = sum(self.monthly_expenses.values())
        self.savings_up_to_date = self.total_income + total_expenses
        self.show_savings.set(f"Accumulated Capital up to month {self.current_month}: £{self.savings_up_to_date}")

    def show_annual_summary(self):
        accumulated_savings, total_expenses_up_to_month = self.calculate_accumulated_savings()
        annual_summary = f"Accumulated Capital up to month {self.current_month}: £{accumulated_savings}\n"
        annual_summary += f"Total Expenses up to month {self.current_month}: £{total_expenses_up_to_month}"
        self.create_summary_window("Annual Financial Summary", annual_summary, 14)

    def show_monthly_summary(self):
        financial_summary = f"Monthly Financial Summary for Month {self.current_month}:\n\n"
        financial_summary += "Monthly Income:\n"
        total_monthly_income = 0
        for tenant, data in self.tenant_rents.items():
            financial_summary += f"{tenant}: £{data['rent']} (Due on {data['payment_day']}th)\n"
            total_monthly_income += data["rent"]

        financial_summary += f"Total Income: £{total_monthly_income}\n\n"
        financial_summary += "Expenses:\n"
        for expense, amount in self.monthly_expenses.items():
            financial_summary += f"{expense}: £{amount}\n"
        total_expenses_month = -sum(self.monthly_expenses.values())
        financial_summary += f"Total Expenses: £{total_expenses_month}\n\n"
        financial_summary += f"Savings for month {self.current_month}: £{self.savings_up_to_date}"

        self.create_summary_window("Monthly Financial Summary", financial_summary, 14)

    def create_summary_window(self, title, content, font_size):
        summary_window = tk.Toplevel(self.root)
        summary_window.title(title)
        label = tk.Label(summary_window, text=content, font=("Helvetica", font_size))
        label.pack()

def main():
    root = tk.Tk()
    app = PropertyManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
