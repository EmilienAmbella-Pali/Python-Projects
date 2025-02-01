import datetime
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import hashlib
import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class PropertyManagementApp:
    # ...existing code...

    def create_tenants_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tenants")

        self.tenants_listbox = tk.Listbox(frame)
        self.tenants_listbox.pack()

        self.update_tenants_listbox()

        ttk.Button(frame, text="Add Tenant", command=self.add_tenant).pack()
        ttk.Button(frame, text="Edit Tenant", command=self.edit_selected_tenant).pack()
        ttk.Button(frame, text="Delete Tenant", command=self.delete_selected_tenant).pack()

    def update_tenants_listbox(self):
        self.tenants_listbox.delete(0, tk.END)
        for tenant in self.selected_property.tenant_rents:
            self.tenants_listbox.insert(tk.END, tenant)

    def edit_selected_tenant(self):
        selected_index = self.tenants_listbox.curselection()
        if selected_index:
            tenant_name = self.tenants_listbox.get(selected_index)
            self.edit_tenant(tenant_name)
        else:
            messagebox.showerror("Error", "Please select a tenant to edit.")

    def delete_selected_tenant(self):
        selected_index = self.tenants_listbox.curselection()
        if selected_index:
            tenant_name = self.tenants_listbox.get(selected_index)
            del self.selected_property.tenant_rents[tenant_name]
            self.update_tenants_listbox()
            messagebox.showinfo("Success", f"Tenant '{tenant_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Please select a tenant to delete.")

    def create_expenses_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Expenses")

        self.expenses_listbox = tk.Listbox(frame)
        self.expenses_listbox.pack()

        self.update_expenses_listbox()

        ttk.Button(frame, text="Add Expense", command=self.get_miscellaneous_expenses).pack()
        ttk.Button(frame, text="Edit Expense", command=self.edit_selected_expense).pack()
        ttk.Button(frame, text="Delete Expense", command=self.delete_selected_expense).pack()

    def update_expenses_listbox(self):
        self.expenses_listbox.delete(0, tk.END)
        for expense, amount in self.selected_property.monthly_expenses.items():
            self.expenses_listbox.insert(tk.END, f"{expense}: £{amount}")

    def edit_selected_expense(self):
        selected_index = self.expenses_listbox.curselection()
        if selected_index:
            expense_name = self.expenses_listbox.get(selected_index).split(":")[0]
            amount = simpledialog.askfloat("Edit Expense", f"Enter new amount for {expense_name}:")
            if amount is not None:
                self.selected_property.monthly_expenses[expense_name] = amount
                self.update_expenses_listbox()
                messagebox.showinfo("Success", f"Expense '{expense_name}' updated successfully.")
        else:
            messagebox.showerror("Error", "Please select an expense to edit.")

    def delete_selected_expense(self):
        selected_index = self.expenses_listbox.curselection()
        if selected_index:
            expense_name = self.expenses_listbox.get(selected_index).split(":")[0]
            del self.selected_property.monthly_expenses[expense_name]
            self.update_expenses_listbox()
            messagebox.showinfo("Success", f"Expense '{expense_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Please select an expense to delete.")

    def create_maintenance_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Maintenance")
        
        ttk.Button(frame, text="Report Issue", command=self.manage_maintenance).pack()

    def create_communication_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Communication")
        
        ttk.Button(frame, text="Send Message", command=self.manage_communication).pack()

    # ...existing code...
class Property:
    def __init__(self, name):
        self.name = name
        self.tenant_rents = {}
        self.monthly_expenses = {}
        self.maintenance_issues = []
        
    def add_tenant(self, tenant_name, rent):
        self.tenant_rents[tenant_name] = rent
        
    def add_expense(self, expense_name, amount):
        self.monthly_expenses[expense_name] = amount
    
    def add_maintenance_issue(self, issue):
        self.maintenance_issues.append(issue)

class PropertyManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Property Management")
        self.users = {}
        self.properties = {}
        self.selected_property = None
        self.load_users()
        self.load_properties()
        self.create_login_screen()

    def load_users(self):
        if not os.path.exists('users.csv'):
            with open('users.csv', 'w'):
                pass
        else:
            with open('users.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.users[row[0]] = row[1]

    def save_users(self):
        with open('users.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for username, password in self.users.items():
                writer.writerow([username, password])

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_properties(self):
        if not os.path.exists('properties.csv'):
            with open('properties.csv', 'w'):
                pass
        else:
            with open('properties.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    property_name = row[0]
                    self.properties[property_name] = Property(property_name)

    def save_properties(self):
        with open('properties.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for property_name in self.properties:
                writer.writerow([property_name])

    def create_login_screen(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(pady=20)

        ttk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack()

        ttk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        ttk.Button(self.login_frame, text="Login", command=self.authenticate).pack(pady=5)
        ttk.Button(self.login_frame, text="Register", command=self.register_user).pack()

    def authenticate(self):
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        
        if username in self.users and self.users[username] == password:
            self.logged_in_user = username
            self.login_frame.destroy()
            self.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register_user(self):
        username = simpledialog.askstring("Register", "Enter a new username:")
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        password = simpledialog.askstring("Register", "Enter a password:", show="*")
        self.users[username] = self.hash_password(password)
        self.save_users()
        messagebox.showinfo("Success", "Registration successful! You can now log in.")

    def create_main_interface(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        self.create_dashboard_tab()
        self.create_expenses_tab()
        self.create_tenants_tab()
        self.create_maintenance_tab()
        self.create_communication_tab()
        self.create_summary_tab()

    def create_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        ttk.Label(frame, text="Welcome to Property Management").pack()
        
        ttk.Button(frame, text="Add Property", command=self.add_property).pack()
        ttk.Label(frame, text="Properties:").pack()
        
        self.property_listbox = tk.Listbox(frame)
        self.property_listbox.pack()
        
        self.update_property_listbox()
        
        ttk.Button(frame, text="Select Property", command=self.select_property).pack()

    def create_expenses_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Expenses")
        
        ttk.Button(frame, text="Enter Misc Expenses", command=self.get_miscellaneous_expenses).pack()

    def create_tenants_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tenants")
        
        ttk.Button(frame, text="Add Tenant", command=self.add_tenant).pack()

    def create_maintenance_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Maintenance")
        
        ttk.Button(frame, text="Report Issue", command=self.manage_maintenance).pack()

    def create_communication_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Communication")
        
        ttk.Button(frame, text="Send Message", command=self.manage_communication).pack()

    def create_summary_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Summary")
        
        ttk.Button(frame, text="Annual Summary", command=self.show_annual_summary).pack()
        ttk.Button(frame, text="Monthly Summary", command=self.show_monthly_summary).pack()

    def add_property(self):
        new_property_name = simpledialog.askstring("Add Property", "Enter Property Name:")
        if new_property_name:
            self.properties[new_property_name] = Property(new_property_name)
            self.save_properties()
            self.update_property_listbox()
            messagebox.showinfo("Success", f"Property '{new_property_name}' added successfully.")

    def update_property_listbox(self):
        self.property_listbox.delete(0, tk.END)
        for property_name in self.properties:
            self.property_listbox.insert(tk.END, property_name)

    def select_property(self):
        selected_index = self.property_listbox.curselection()
        if selected_index:
            self.selected_property = self.properties[self.property_listbox.get(selected_index)]
            messagebox.showinfo("Property Selected", f"You have selected '{self.selected_property.name}'.")

    def get_miscellaneous_expenses(self):
        try:
            amount = simpledialog.askfloat("Miscellaneous Expenses", "Enter miscellaneous expenses:")
            if self.selected_property:
                expense_name = simpledialog.askstring("Expense Name", "Enter expense description:")
                self.selected_property.add_expense(expense_name, amount)
                messagebox.showinfo("Success", f"Expense '{expense_name}' of £{amount} recorded for property '{self.selected_property.name}'.")
            else:
                messagebox.showerror("Error", "Please select a property first.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    def add_tenant(self):
        if self.selected_property:
            tenant_name = simpledialog.askstring("Add Tenant", "Enter Tenant Name:")
            rent = simpledialog.askfloat("Tenant Rent", "Enter Tenant Rent (£):")
            if tenant_name and rent:
                self.selected_property.add_tenant(tenant_name, rent)
                messagebox.showinfo("Tenant Added", f"Tenant '{tenant_name}' with rent of £{rent} added to '{self.selected_property.name}'.")
        else:
            messagebox.showerror("Error", "Please select a property first.")

    def manage_maintenance(self):
        if self.selected_property:
            issue = simpledialog.askstring("Maintenance", "Enter Issue:")
            if issue:
                self.selected_property.add_maintenance_issue(issue)
                messagebox.showinfo("Recorded", f"Issue '{issue}' recorded for '{self.selected_property.name}'.")
        else:
            messagebox.showerror("Error", "Please select a property first.")

    def manage_communication(self):
        message = simpledialog.askstring("Communication", "Enter Message:")
        if message:
            messagebox.showinfo("Sent", "Message sent to tenants.")

    def show_annual_summary(self):
        if self.selected_property:
            annual_expenses = sum(self.selected_property.monthly_expenses.values())
            total_rent = sum(self.selected_property.tenant_rents.values()) * 12
            messagebox.showinfo("Annual Summary", f"Total Rent: £{total_rent}\nTotal Expenses: £{annual_expenses}")
        else:
            messagebox.showerror("Error", "Please select a property first.")

    def show_monthly_summary(self):
        if self.selected_property:
            monthly_expenses = sum(self.selected_property.monthly_expenses.values())
            total_rent = sum(self.selected_property.tenant_rents.values())
            messagebox.showinfo("Monthly Summary", f"Total Rent: £{total_rent}\nTotal Expenses: £{monthly_expenses}")
        else:
            messagebox.showerror("Error", "Please select a property first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PropertyManagementApp(root)
    root.mainloop()
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import hashlib
import csv
import os
import re

class Property:
    def __init__(self, name):
        self.name = name
        self.tenant_rents = {}
        self.monthly_expenses = {}

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.username = ""
        self.password = ""
        self.users = {}
        self.properties = {}
        self.selected_property = None

        self.load_users()

        self.login_label = tk.Label(root, text="Please enter username and password")
        self.login_label.pack()

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.authenticate)
        self.login_button.pack()

    def load_users(self):
        if not os.path.exists('users.csv'):
            with open('users.csv', 'w'):
                pass
        else:
            with open('users.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.users[row[0]] = row[1]

    def save_users(self):
        with open('users.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for username, password in self.users.items():
                writer.writerow([username, password])

    def authenticate(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        if self.username in self.users and self.check_password(self.password, self.users[self.username]):
            self.root.destroy()
            self.property_selection()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, input_password, stored_password):
        return self.hash_password(input_password) == stored_password

    def property_selection(self):
        self.property_window = tk.Tk()
        self.property_window.title("Select Property")

        property_label = tk.Label(self.property_window, text="Select Property:")
        property_label.pack()

        for property_name in self.properties:
            property_button = tk.Button(self.property_window, text=property_name, command=lambda name=property_name: self.select_property(name))
            property_button.pack()

        add_property_button = tk.Button(self.property_window, text="Add Property", command=self.add_property)
        add_property_button.pack()

        self.property_window.mainloop()

    def select_property(self, property_name):
        self.selected_property = self.properties[property_name]
        self.launch_app_for_property()

    def launch_app_for_property(self):
        property_window = tk.Toplevel()
        property_window.title("Property Management")
        app = PropertyManagementApp(property_window, self.selected_property, self.username)

    def add_property(self):
        new_property_name = simpledialog.askstring("Add Property", "Enter Property Name:")
        if new_property_name:
            self.properties[new_property_name] = Property(new_property_name)
            messagebox.showinfo("Property Added", f"Property '{new_property_name}' added successfully.")
            self.property_window.destroy()  # Close the property selection window
            self.property_selection()  # Reopen the property selection window with updated properties
        else:
            messagebox.showerror("Error", "Property name cannot be empty.")
            
            # Close the property selection window
            self.property_window.destroy()
            
            # Reopen the property selection window with updated properties
            self.property_selection()

    def save_properties(self):
        with open('properties.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for property_name, property_obj in self.properties.items():
                # Save property details: property name
                writer.writerow([property_name])

                # Save tenant details for the property
                for tenant, tenant_data in property_obj.tenant_rents.items():
                    writer.writerow([property_name, tenant, tenant_data['rent'], tenant_data['payment_day'], tenant_data['email'], tenant_data['phone']])


    def load_properties(self):
        if not os.path.exists('properties.csv'):
            return

        with open('properties.csv', mode='r') as file:
           reader = csv.reader(file)
           current_property = None
           for row in reader:
               if len(row) == 1:  # New property entry
                   current_property = row[0]
                   self.properties[current_property] = Property(current_property)
               elif len(row) == 6:  # Tenant details for the property
                  property_name, tenant, rent, payment_day, email, phone = row
                  if property_name in self.properties:
                      self.properties[property_name].tenant_rents[tenant] = {
                          'rent': int(rent),
                          'payment_day': int(payment_day),
                          'email': email,
                          'phone': phone
                      }

class PropertyManagementApp:
    def __init__(self, root, selected_property, username):
        self.root = root
        self.selected_property = selected_property
        self.username = username
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

        maintenance_button = tk.Button(self.root, text="Maintenance", command=self.manage_maintenance)
        maintenance_button.pack()

        communication_button = tk.Button(self.root, text="Communication", command=self.manage_communication)
        communication_button.pack()

        property_details_button = tk.Button(self.root, text="Property Details", command=self.view_property_details)
        property_details_button.pack()


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
           tenant_name_to_edit = simpledialog.askstring("Edit Tenant", "Enter the name of the tenant to edit:")
           if tenant_name_to_edit in self.tenant_rents:
               self.edit_tenant_details(tenant_name_to_edit)
           else:
               messagebox.showerror("Error", f"Tenant '{tenant_name_to_edit}' not found.")

        else:
           messagebox.showerror("Error", "Invalid selection")

    def edit_tenant_details(self, tenant_name):
        # Function to edit details of a specific tenant
        tenant_details = self.tenant_rents[tenant_name]

        label_texts = ["Monthly rent:", "Date of payment:", "Email address:", "Phone number:"]
        entries = {}
    
        for i, (key, text) in enumerate(zip(tenant_details, label_texts), start=1):
            label = tk.Label(self.edit_window, text=text)
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(self.edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(tk.END, str(tenant_details[key]))  # Fill the entry with existing data
            entries[key] = entry

        save_button = tk.Button(self.edit_window, text="Save Details", command=lambda: self.save_edited_tenant_details(tenant_name, entries))
        save_button.grid(row=len(label_texts) + 1, column=0, columnspan=2, pady=10)

    def save_edited_tenant_details(self, tenant_name, entries):
        edited_details = {}
        for key, entry in entries.items():
            if key == "rent" or key == "payment_day":
                value = int(entry.get()) if entry.get().isdigit() else 0
            else:
                value = entry.get()

            edited_details[key] = value

        # Update the tenant details with edited values
        self.tenant_rents[tenant_name] = edited_details
        messagebox.showinfo("Success", f"Details for '{tenant_name}' updated successfully.")
        self.edit_window.destroy()
        # Call function to update savings or perform other necessary actions
        self.update_savings()
        self.show_savings.set(f"Accumulated Capital up to month {self.current_month}: £{self.calculate_accumulated_savings()[0]}")    
            
        

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
        for i, (key, text) in enumerate(zip(label_texts, label_texts), start=1):
            entry = self.edit_window.grid_slaves(row=i, column=1)[0]
            if key == "Monthly rent:" or key == "Date of payment:":
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

    def manage_tenants(self):
        # Logic to manage tenants: Sample implementation to add a new tenant
        tenant_name = simpledialog.askstring("Tenant Details", "Enter Tenant Name:")
        if tenant_name:
            rent = simpledialog.askfloat("Tenant Details", f"Enter Monthly Rent for {tenant_name}:")
            payment_day = simpledialog.askinteger("Tenant Details", f"Enter Payment Day for {tenant_name} (1-31):")
            email = simpledialog.askstring("Tenant Details", f"Enter Email Address for {tenant_name}:")
            phone = simpledialog.askstring("Tenant Details", f"Enter Phone Number for {tenant_name}:")

            self.selected_property.tenant_rents[tenant_name] = {
                "rent": rent,
                "payment_day": payment_day,
                "email": email,
                "phone": phone
            }
            messagebox.showinfo("Tenant Added", f"Tenant '{tenant_name}' added successfully.")
        else:
            messagebox.showerror("Error", "Tenant name cannot be empty.")

    def manage_finances(self):
        # Logic to manage finances: Sample implementation to add monthly expenses
        expense_type = simpledialog.askstring("Monthly Expenses", "Enter Expense Type:")
        if expense_type:
            amount = simpledialog.askfloat("Monthly Expenses", f"Enter Amount for {expense_type}:")
            self.selected_property.monthly_expenses[expense_type] = -amount
            messagebox.showinfo("Expense Added", f"Expense '{expense_type}' added successfully.")
        else:
            messagebox.showerror("Error", "Expense type cannot be empty.")

    def manage_maintenance(self):
        # Logic to manage maintenance: Sample implementation to track maintenance issues
        issue = simpledialog.askstring("Maintenance", "Enter Maintenance Issue:")
        if issue:
            # Logic to handle the maintenance issue
            messagebox.showinfo("Maintenance Recorded", f"Maintenance issue '{issue}' recorded.")
        else:
            messagebox.showerror("Error", "Please enter a maintenance issue.")

    def manage_communication(self):
        # Logic to manage communication: Sample implementation to send notifications
        message = simpledialog.askstring("Communication", "Enter Message to Tenants:")
        if message:
            # Logic to send the message to tenants
            messagebox.showinfo("Message Sent", "Message sent to all tenants.")
        else:
            messagebox.showerror("Error", "Message cannot be empty.")

    def view_property_details(self):
        # Logic to view property details: Sample implementation to display property information
        details = f"Property Name: {self.selected_property.name}\n"
        details += "Tenant Rents:\n"
        for tenant, data in self.selected_property.tenant_rents.items():
            details += f"{tenant}: Rent £{data['rent']} due on {data['payment_day']}th\n"
        details += "Monthly Expenses:\n"
        for expense, amount in self.selected_property.monthly_expenses.items():
            details += f"{expense}: £{amount}\n"

        messagebox.showinfo("Property Details", details)

    # Implement other functionalities as needed for property management

    def change_property(self):
        self.root.destroy()
        root = tk.Tk()
        login = LoginWindow(root)
        root.mainloop()

def main():
    root = tk.Tk()
    login = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
