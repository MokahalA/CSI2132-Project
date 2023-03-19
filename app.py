from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__, static_url_path='', )
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
            return redirect(url_for('loginCustomerPage', username=username))
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

def get_hotels():
    chain = request.args.get('chain')
    # Connect to the database
    conn = sqlite3.connect('ehotels_database.db')
    c = conn.cursor()
    # Construct a query to retrieve hotels for the selected chain from the database
    query = "SELECT * FROM hotels WHERE chainName = ?"
    c.execute(query, (chain,))
    hotels = c.fetchall()
    # Convert the query result to a list of dictionaries
    hotels = [dict(hotel) for hotel in hotels]
    # Close the database connection
    c.close()
    conn.close()
    # Return the list of hotels as a JSON object
    return jsonify({'hotels': hotels})
  

def get_hotel_chains():
    conn = sqlite3.connect('ehotels_database.db')
    c = conn.cursor()
    c.execute('SELECT chainName FROM HotelChain WHERE chainName IS NOT NULL;')
    rows = c.fetchall()
    c.close()
    conn.close()
    return rows


#Route for the customer page (when they are logged in)
@app.route('/loginCustomerPage', methods=['GET', 'POST'])
def loginCustomerPage():
    return render_template('customerPage.html', chains=get_hotel_chains())



def bookAndrent():
    return render_template('rentandbook.html')


if __name__ == '__main__':
    app.run(debug=True)