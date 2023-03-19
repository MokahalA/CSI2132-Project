from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'


# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

#Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the inputs from the HTML
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('ehotels_database.db')
        c = conn.cursor()

        #SQL Select to see if the user credentials match a row in the database
        c.execute('SELECT * FROM Customer WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()

        if user:
            session['username'] = user[1]
            global loggedUserName
            loggedUserName = username
            conn.close()
            return render_template('customerPage.html', username = username)
        else:
            conn.close()
            return 'Invalid username or password'
        
    return render_template('login.html')


#Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the inputs from the HTML
        ssnValue = request.form['SSN']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        street = request.form['street']
        city = request.form['city']
        province = request.form['province']
        zip = request.form['zip']
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('ehotels_database.db')
        c = conn.cursor()

        # SQL insertion statement to create a Customer row
        c.execute('INSERT INTO Customer (SSN, first_name, last_name, street, city, province, zip, username, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (ssnValue, first_name, last_name, street, city, province, zip, username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')


#Route for the customer page (when they are logged in)
@app.route('/loginCustomerPage', methods=['GET', 'POST'])
def loginCustomerPage():
    return render_template('customerPage.html')



if __name__ == '__main__':
    app.run(debug=True)