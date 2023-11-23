from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__,static_url_path='/static')


# Database connection configuration
db_config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "igcobra123",
    "host": "localhost",
    "port": "5432"
}

# Function to create a database connection
def create_db_connection():
    return psycopg2.connect(**db_config)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for student registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sms (name,email,password) VALUES (%s, %s, %s)", (name,email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# Define a route for student login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sms WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return redirect(url_for('dashboard'))
        else:
            return "Login failed."
    return render_template('loginn.html')

# Define a route for the student dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/prices')
def prices():
    return "welcome tp prices"


@app.route('/profile')
def profile():
    return render_template('profile.html')




# Define a route to log out
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
