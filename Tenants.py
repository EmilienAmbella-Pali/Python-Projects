import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import re  # Import regular expression module

class PropertyManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Property Management App")
        self.tenant_rents = {
            "Tenant_1": {"rent": 450, "payment_day": 24, "email": "", "phone": ""},
            "Tenant_2": {"rent": 450, "payment_day": 15, "email": "", "phone": ""},
            "Tenant_3": {"rent": 600, "payment_day": 5, "email": "", "phone": ""},
            "Tenant_4": {"rent": 1000, "payment_day": 15, "email": "", "phone": ""},
            "Tenant_5": {"rent": 400, "payment_day": 15, "email": "", "phone": ""},
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
            label_texts = ["Tenant name:", "Monthly rent:", "Date of payment:", "Email address:", "Phone number:"]
            for i, text in enumerate(label_texts, start=1):
                label = tk.Label(self.edit_window, text=text)
                label.grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(self.edit_window)
                entry.grid(row=i, column=1, padx=5, pady=5)

            save_button = tk.Button(self.edit_window, text="Save Details", command=self.save_tenant_details)
            save_button.grid(row=6, column=0, columnspan=2, pady=10)

        elif action == "2":
            self.create_table()

        else:
            messagebox.showerror("Error", "Invalid selection")

    def create_table(self):
        label_texts = ["Tenant name:", "Monthly rent:", "Date of payment:", "Email address:", "Phone number:"]
        for i, text in enumerate(label_texts, start=1):
            label = tk.Label(self.edit_window, text=text)
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(self.edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)

        save_button = tk.Button(self.edit_window, text="Save Details", command=self.save_tenant_details)
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_tenant_details(self):
        new_tenant_details = {}
        label_texts = ["Tenant name:", "Monthly rent:", "Date of payment:", "Email address:", "Phone number:"]
        for i, (key, text) in enumerate(zip(new_tenant_details, label_texts), start=1):
            entry = self.edit_window.grid_slaves(row=i, column=1)[0]
            if key == "rent" or key == "payment_day":
                value = int(entry.get()) if entry.get().isdigit() else 0
            else:
                value = entry.get()
                if key == "Email address:" and value:
                    if not re.match(r"[a-zA-Z0-9_.+-]+@gmail\.com", value):
                        messagebox.showerror("Error", "Please enter a valid Gmail address.")
                        return
            new_tenant_details[key] = value

        tenant_name = new_tenant_details.get("Tenant name:")
        if tenant_name and tenant_name not in self.tenant_rents:
            self.tenant_rents[tenant_name] = new_tenant_details
        else:
            messagebox.showerror("Error", "Tenant name already exists or is invalid.")

        self.edit_window.destroy()
        self.update_savings()
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
