from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample data (in a real app, use a database)
users = {
    'admin': 'password123',
    'student': 'student123'
}

attendance_records = []

# Home/Login Page
@app.route("/")
def index():
    return render_template("index.html")

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# Dashboard Page
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=session['user'])

# Mark Attendance
@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        record = {
            'user': session['user'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'status': request.form.get('status')
        }
        attendance_records.append(record)
        return redirect(url_for('attendance'))
    
    return render_template('attendance.html', records=attendance_records)

# View Records
@app.route("/records")
def records():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_records = [r for r in attendance_records if r['user'] == session['user']]
    return render_template('records.html', records=user_records)

# Logout
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
