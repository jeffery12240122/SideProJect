import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
import re
import os

class ReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Reservation System")
        self.root.geometry("500x500")

        self.users = self.load_users()
        self.current_user = None
        self.reservations = {}

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Register", command=self.show_register_screen)
        self.register_button.pack(pady=10)

    def show_register_screen(self):
        self.clear_screen()

        self.new_username_label = tk.Label(self.root, text="New Username")
        self.new_username_label.pack(pady=10)

        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)

        self.new_password_label = tk.Label(self.root, text="New Password")
        self.new_password_label.pack(pady=10)

        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back to Login", command=self.show_login_screen)
        self.back_button.pack(pady=10)

    def show_reservation_screen(self):
        self.clear_screen()

        self.name_label = tk.Label(self.root, text="Name")
        self.name_label.pack(pady=10)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        self.date_label = tk.Label(self.root, text="Date")
        self.date_label.pack(pady=10)

        self.date_combobox = ttk.Combobox(self.root, values=self.generate_dates())
        self.date_combobox.pack(pady=5)
        self.date_combobox.bind("<<ComboboxSelected>>", self.update_time_combobox)

        self.time_label = tk.Label(self.root, text="Time")
        self.time_label.pack(pady=10)

        self.time_combobox = ttk.Combobox(self.root)
        self.time_combobox.pack(pady=5)

        self.create_button = tk.Button(self.root, text="Preserve", command=self.create_reservation)
        self.create_button.pack(pady=10)

        self.view_button = tk.Button(self.root, text="View all preserve", command=self.open_view_window)
        self.view_button.pack(pady=10)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

        self.update_time_combobox()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_dates(self):
        today = datetime.today()
        return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    def generate_times(self, selected_date=None):
        all_times = [f"{hour:02d}:00" for hour in range(24)]
        if selected_date:
            reserved_times = [
                datetime_str.split()[1] for datetime_str in self.reservations
                if datetime_str.startswith(selected_date)
            ]
            available_times = [time for time in all_times if time not in reserved_times]
            return available_times
        return all_times

    def update_time_combobox(self, event=None):
        selected_date = self.date_combobox.get()
        available_times = self.generate_times(selected_date)
        self.time_combobox['values'] = available_times
        if available_times:
            self.time_combobox.current(0)

    def load_reservations(self):
        if self.current_user:
            try:
                with open(f"{self.current_user}_reservations.txt", "r") as file:
                    reservations = {}
                    for line in file:
                        datetime_str, name = line.strip().split(",")
                        reservations[datetime_str] = name
                    return reservations
            except FileNotFoundError:
                return {}
        return {}

    def load_users(self):
        try:
            with open("users.txt", "r") as file:
                users = {}
                for line in file:
                    username, password = line.strip().split(",")
                    users[username] = password
                return users
        except FileNotFoundError:
            return {}

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.reservations = self.load_reservations()
            messagebox.showinfo("Login Success", "Welcome!")
            self.show_reservation_screen()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password.")

    def register(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if not self.validate_username(new_username):
            messagebox.showwarning("Input Error", "Username must be alphanumeric and at least 3 characters long.")
            return

        if not self.validate_password(new_password):
            messagebox.showwarning("Input Error", "Password must be at least 6 characters long.")
            return

        if new_username in self.users:
            messagebox.showwarning("Registration Failed", "Username already exists.")
        else:
            self.users[new_username] = new_password
            self.save_users()
            os.makedirs(new_username, exist_ok=True)
            messagebox.showinfo("Registration Success", "You have successfully registered!")
            self.show_login_screen()

    def validate_username(self, username):
        return bool(re.match("^[A-Za-z0-9]{3,}$", username))

    def validate_password(self, password):
        return len(password) >= 6

    def logout(self):
        self.current_user = None
        self.reservations = {}
        self.show_login_screen()

    def create_reservation(self):
        name = self.name_entry.get()
        date = self.date_combobox.get()
        time = self.time_combobox.get()
        datetime_str = f"{date} {time}"

        # Validate inputs
        if not self.validate_name(name):
            messagebox.showwarning("Input Error", "Please provide a valid name (only letters and spaces are allowed).")
            return
        if not date or not time:
            messagebox.showwarning("Input Error", "Please select a date and time.")
            return

        if datetime_str in self.reservations:
            messagebox.showwarning("Reservation Error", f"Time slot {datetime_str} is already booked.")
        else:
            self.reservations[datetime_str] = name
            messagebox.showinfo("Success", f"Reservation made for {name} at {datetime_str}.")
            self.save_reservations()
            self.update_time_combobox()

    def validate_name(self, name):
        return bool(re.match("^[A-Za-z ]+$", name))

    def open_view_window(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Reservations")
        view_window.geometry("600x400")

        tree = ttk.Treeview(view_window, columns=("Name", "Date", "Time"))
        tree.heading("#0", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.column("#0", width=60)
        tree.column("Name", width=210)
        tree.column("Date", width=150)
        tree.column("Time", width=80)
        tree.pack(expand=True, fill="both")

        sorted_reservations = sorted(self.reservations.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M"))
        for index, (datetime_str, name) in enumerate(sorted_reservations, start=1):
            date, time = datetime_str.split()
            tree.insert("", "end", text=str(index), values=(name, date, time))

        def delete_selected():
            selected_item = tree.selection()
            if selected_item:
                item_id = tree.item(selected_item)["text"]
                datetime_str = sorted_reservations[int(item_id) - 1][0]
                self.delete_reservation(datetime_str)
                view_window.destroy()

        delete_button = tk.Button(view_window, text="Delete Selected", command=delete_selected)
        delete_button.pack(pady=10)

    def save_reservations(self):
        if self.current_user:
            with open(f"{self.current_user}_reservations.txt", "w") as file:
                for datetime_str, name in self.reservations.items():
                    file.write(f"{datetime_str},{name}\n")

    def save_users(self):
        with open("users.txt", "w") as file:
            for username, password in self.users.items():
                file.write(f"{username},{password}\n")

    def delete_reservation(self, datetime_str):
        if messagebox.askyesno("Delete Confirmation", f"Do you want to delete the reservation at {datetime_str}?"):
            if datetime_str in self.reservations:
                del self.reservations[datetime_str]
                messagebox.showinfo("Success", f"Reservation at {datetime_str} has been deleted.")
                self.save_reservations()
                self.update_time_combobox()
            else:
                messagebox.showwarning("Deletion Error", f"No reservation found at {datetime_str}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationSystem(root)
    root.mainloop()
