import sqlite3

conn = sqlite3.connect('stock_reminder.db')
c = conn.cursor()

c.execute("SELECT * FROM reminders")
rows = c.fetchall()
for row in rows:
    print(row)

conn.close()