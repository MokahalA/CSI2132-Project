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
        if request.form['loginBtn'] == 'LoginCustomer':
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
        
        elif request.form['loginBtn'] == 'LoginEmployee':
            # TODO: Need to implement username & password validation for employee here, 
            # might need to hard-code some values in the Employee table when we do SQL insertions.
            
            # Get the inputs from the HTML
            username = request.form['username']
            password = request.form['password']

            conn = sqlite3.connect('ehotels_database.db')
            c = conn.cursor()

            #SQL Select to see if the user credentials match a row in the database
            c.execute('SELECT * FROM Employee WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()

            if user:
                session['username'] = user[1]
                loggedUserName = username
                conn.close()
                return redirect(url_for('loginEmployeePage', username=username))
            else:
                conn.close()
                return 'Invalid username or password'
        
        else:
            return render_template('login.html')
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

  
# Function for obtaining a list of all the HotelChains stored in the database.
def get_hotel_chains():
    conn = sqlite3.connect('ehotels_database.db')
    c = conn.cursor()
    c.execute('SELECT chainName FROM HotelChain WHERE chainName IS NOT NULL;')
    rows = c.fetchall()
    c.close()
    conn.close()
    return rows

# Function for obtaining a list of Hotels associated with an input HotelChain.
def get_hotels(chainName):
    conn = sqlite3.connect('ehotels_database.db')
    c = conn.cursor()
    c.execute('SELECT Hotels.locationName, Hotels.hotelID FROM HotelChain INNER JOIN Hotels ON HotelChain.chainName = Hotels.chainName WHERE Hotels.chainName = ?', 
              (chainName,))
    rows = c.fetchall()
    c.close()
    conn.close()
    return rows

# Function for obtaining a list of Rooms associated with input criteria
def get_rooms(hotelID, numRooms, minPrice, maxPrice, hasWifi, hasJacuzzi, viewType):

    print(hotelID, numRooms, minPrice, maxPrice, hasWifi, hasJacuzzi, viewType)

    if(hasWifi == None):
        hasWifi = 0
    if(hasJacuzzi == None):
        hasJacuzzi = 0

     # Connect to the database
    conn = sqlite3.connect('ehotels_database.db')
    cur = conn.cursor()

    # Execute the SQL query
    sql_query = '''SELECT roomID, hotelID, price, hasWifi, hasJaccuzi, roomCapacity, viewType, extendable
    FROM Rooms
    WHERE hotelID = ?
    AND price BETWEEN ? AND ?
    AND hasWifi = ?
    AND hasJaccuzi = ?
    AND viewType = ?
    AND roomCapacity >= ?'''

    cur.execute(sql_query, (hotelID, minPrice, maxPrice, hasWifi, hasJacuzzi, viewType, numRooms))
    # Fetch the results
    rows = cur.fetchall()

    conn.close()
    return rows

#Route for the customer page (when they are logged in)
@app.route('/loginCustomerPage', methods=['GET', 'POST'])
def loginCustomerPage():
    if request.method == 'GET' and ('hotel-chain-filter' or 'hotel-filter' or 'num-rooms-filter' or 'min-price' or 'max-price' or 'hasWifi-filter' or 'hasJacuzzi-filter' or 'viewType-filter') in request.args:
        # get the value of the 'hotel-chain-filer' parameter
        chainName = request.args.get('hotel-chain-filter')

        # create a new 'chains' list where the previously selected hotel chain is at the front of the list.
        newChains = list(filter(lambda c: c != (chainName,), get_hotel_chains()))
        newChains.insert(0, (chainName,))

        # Obtain all other filter attributes
        hotelID = request.args.get('hotel-filter')
        numRooms = request.args.get('num-rooms-filter')
        minPrice = request.args.get('min-price')
        maxPrice = request.args.get('max-price')
        hasWifi = request.args.get('hasWifi-filter')
        hasJacuzzi = request.args.get('hasJacuzzi-filter')
        viewType = request.args.get('viewType-filter')

        print(get_rooms(hotelID, numRooms, minPrice, maxPrice, hasWifi, hasJacuzzi, viewType))

        # Render new UI with the selected hotel chain and the associated hotels
        return render_template('customerPage.html', chains = newChains, hotels = get_hotels(chainName), results = get_rooms(hotelID, numRooms, minPrice, maxPrice, hasWifi, hasJacuzzi, viewType))
    return render_template('customerPage.html', chains=get_hotel_chains(), hotels = get_hotels("Accor S.A."), results = get_rooms(1, 1, 10, 400, 1, 0, 'Sea view'))


#Route for the employee page (when they are logged in)
@app.route('/loginEmployeePage', methods=['GET', 'POST'])
def loginEmployeePage():
    return render_template('employeePage.html')


def bookAndrent():
    return render_template('rentandbook.html')


if __name__ == '__main__':
    app.run(debug=True)