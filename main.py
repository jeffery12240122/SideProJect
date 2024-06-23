from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'qwertyuiop78962147896mnbvcx'
# A list to store reservations
reservations = []

@app.route('/')
def index():
    return render_template('index.html', reservations=reservations)

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']
    people = request.form['people']

    reservation = {
        'name': name,
        'email': email,
        'date': date,
        'time': time,
        'people': people
    }

    reservations.append(reservation)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=False)
