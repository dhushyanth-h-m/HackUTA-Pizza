import smtplib
from flask import Flask, render_template, request, session, redirect, url_for, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import random
import os


# Define the database connection details
DB_NAME = 'foodsustainability'
DB_USER = 'postgres'
DB_PASS = '200117'
DB_HOST = 'localhost'
DB_PORT = '5432'


app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.secret_key = 'mysecretkey'

# @app.route("/")
# def hello():
#     # return render_template('allergen.html')
#     return "Hello world!"

# Define the SQL statement for authenticating a user
AUTHENTICATE_USER = """
    SELECT * FROM user_info  
    WHERE username = %s AND password = %s;
"""


@app.route('/')
def login():
    return render_template('login_new.html')


def connect_db():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        print('Connected to database')
    except psycopg2.Error as e:
        print('Error connecting to database:', e)
    return conn


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        phone_number = request.form['phone_number']

        # Check if the username already exists
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT id FROM user_info WHERE username = %s', (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('signup'))

        # Insert the user data into the database
        hashed_password = generate_password_hash(password, method='sha256')
        cur.execute(
            'INSERT INTO user_info (username, password, email, first_name, last_name, date_of_birth, address, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (username, hashed_password, email, first_name,
             last_name, date_of_birth, address, phone_number)
        )
        conn.commit()

        # Set the session data and redirect to the dashboard
        session['username'] = username
        flash('Your account has been created!')
        return redirect(url_for('login'))

    else:
        return render_template('signup_new.html')


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_info WHERE username = %s', (username,))
        user = cur.fetchone()

        if not user:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        # Check if the password is correct
        if not check_password_hash(user[2], password):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        # Set the session data and redirect to the dashboard
        session['username'] = username
        session['user_id'] = user[0]
        return redirect(url_for('dashboard'))

    else:
        return render_template('login_new.html')


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # Get the user's information from the database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_info WHERE id = %s',
                    (session['user_id'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('index.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/map')
def map():
    return render_template('map.html')


# def get_database():

#     # Provide the mongodb atlas url to connect python to mongodb using pymongo
#     CONNECTION_STRING = "mongodb+srv://hackuta:rpe5xx3YOUWLXFOc@cluster-01.nzw7jiq.mongodb.net/?retryWrites=true&w=majority"

#     # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
#     client = MongoClient(CONNECTION_STRING)

#     try:
#         client.admin.command('ping')
#         print("Pinged your deployment. You successfully connected to MongoDB!")
#     except Exception as e:
#         print(e)

#     # Create the database for our example (we will use the same database throughout the tutorial
#     return client['user_shopping_list']


# db = client["restaurant_db"]

# # Access the collection for restaurant owners (create it if it doesn't exist)
# owners_collection = db["restaurant_owners"]

# # Sample data for a restaurant owner
# restaurant_owner_data = {
#     "username": "restaurant_owner1",
#     "password": "secure_password",
#     "email": "owner1@example.com",
#     "phone_number": "+1234567890",
#     "address": "123 Main St, City, Country",
#     "payment_details": {
#         "card_type": "Visa",
#         "card_number": "************1234",
#         "expiration_date": "12/25",
#         "cvv": "123",
#     }
# }

# # Insert the restaurant owner data into the collection
# result = owners_collection.insert_one(restaurant_owner_data)

# # Check if the insertion was successful
# if result.inserted_id:
#     print("Restaurant owner data added successfully.")
# else:
#     print("Failed to add restaurant owner data.")

# # Close the MongoDB client
# client.close()


@app.route('/add_food_item', methods=['GET', 'POST'])
def add_food_item():
    # Check if the user is authenticated
    if not 'username' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Process the submitted form data and add the food item to MongoDB Atlas
        # (Implement this logic here)

        # Redirect to the store information page after adding the item
        return redirect(url_for('index'))

    return render_template('add_food_item.html')


def get_store_info(user_id):
    # Simulated data for a store
    store_data = {
        "user_id": user_id,
        "store_name": "Sample Store",
        "products": []
    }

    # Query MongoDB Atlas to get the store's food items
    store_items = your_mongodb_query_here  # Replace with your MongoDB query

    # Populate the 'products' list with the retrieved food items
    for item in store_items:
        product_info = {
            "product_name": item["product_name"],
            "quantity": item["quantity"],
            "time_till_last": item["time_till_last"],
            "remaining_food": item["remaining_food"],
            "food_after_hours": item["food_after_hours"],
            "price": item["price"],
            "discounted_price": item["discounted_price"],
            "webpage_link": item["webpage_link"],
        }
        store_data["products"].append(product_info)

    return store_data

# Dummy user authentication function (replace with your authentication logic)


@app.route('/logout')
def logout():
    # Clear the user's ID from the session
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    # dbname = get_database()
    # collection_name = dbname["user_1_items"]
    app.run(debug=True)
