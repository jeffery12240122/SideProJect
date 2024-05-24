import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta

class ReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Reservation System")
        self.root.geometry("500x500")

        self.reservations = self.load_reservations()

        self.name_label = tk.Label(root, text="Name")
        self.name_label.pack(pady=10)

        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        self.date_label = tk.Label(root, text="Date")
        self.date_label.pack(pady=10)

        self.date_combobox = ttk.Combobox(root, values=self.generate_dates())
        self.date_combobox.pack(pady=5)

        self.time_label = tk.Label(root, text="Time")
        self.time_label.pack(pady=10)

        self.time_combobox = ttk.Combobox(root, values=self.generate_times())
        self.time_combobox.pack(pady=5)

        self.create_button = tk.Button(root, text="Preserve", command=self.create_reservation)
        self.create_button.pack(pady=10)

        self.view_button = tk.Button(root, text="View all preserve", command=self.open_view_window)
        self.view_button.pack(pady=10)

    def generate_dates(self):
        today = datetime.today()
        return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    def generate_times(self):
        return [f"{hour:02d}:00" for hour in range(24)]

    def load_reservations(self):
        try:
            with open("reservations.txt", "r") as file:
                reservations = {}
                for line in file:
                    datetime_str, name = line.strip().split(",")
                    reservations[datetime_str] = name
                return reservations
        except FileNotFoundError:
            return {}

    def create_reservation(self):
        name = self.name_entry.get()
        date = self.date_combobox.get()
        time = self.time_combobox.get()
        datetime_str = f"{date} {time}"

        if not name or not date or not time:
            messagebox.showwarning("Input Error", "Please provide name, date, and time.")
            return

        if datetime_str in self.reservations:
            messagebox.showwarning("Reservation Error", f"Time slot {datetime_str} is already booked.")
        else:
            self.reservations[datetime_str] = name
            messagebox.showinfo("Success", f"Reservation made for {name} at {datetime_str}.")

        self.save_reservations()

    def open_view_window(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Reservations")
        view_window.geometry("600x400")

        tree = ttk.Treeview(view_window, columns=("Name", "Date", "Time"))
        tree.heading("#0", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.column("#0", width = 60)
        tree.column("Name", width = 210)
        tree.column("Date", width = 150)
        tree.column("Time", width = 80)
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
        with open("reservations.txt", "w") as file:
            for datetime_str, name in self.reservations.items():
                file.write(f"{datetime_str},{name}\n")

    def delete_reservation(self, datetime_str):
        if messagebox.askyesno("Delete Confirmation", f"Do you want to delete the reservation at {datetime_str}?"):
            if datetime_str in self.reservations:
                del self.reservations[datetime_str]
                messagebox.showinfo("Success", f"Reservation at {datetime_str} has been deleted.")
                self.save_reservations()
            else:
                messagebox.showwarning("Deletion Error", f"No reservation found at {datetime_str}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationSystem(root)
    root.mainloop()
