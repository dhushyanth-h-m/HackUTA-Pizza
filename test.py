# import os
# import random
# from datetime import datetime, timedelta
# from flask_mail import Mail, Message
# from werkzeug.security import generate_password_hash, check_password_hash
# import psycopg2
from flask import Flask, render_template, request, session, redirect, url_for, flash
# import smtplib
from pymongo.mongo_client import MongoClient
# import pymongo as Mongo
app = Flask(__name__)


# @app.route("/")
# def hello():
#     # return render_template('allergen.html')
#     return "Hello world!"


# uri = "mongodb+srv://hackuta:rpe5xx3YOUWLXFOc@cluster-01.65uvf4f.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://hackuta:rpe5xx3YOUWLXFOc@cluster-01.nzw7jiq.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client["left_over_food"]
users_collection = db["restaurant_info"]
# Send a ping to confirm a successful connection
#


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://hackuta:rpe5xx3YOUWLXFOc@cluster-01.nzw7jiq.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_shopping_list']


db = client["restaurant_db"]

# Access the collection for restaurant owners (create it if it doesn't exist)
owners_collection = db["restaurant_owners"]

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


def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        return True
    return False


@app.route('/')
def index():
    # Check if the user is authenticated
    if not authenticate_user("sample_user", "sample_password"):
        return redirect(url_for('login'))

    user_id = "sample_user"  # Replace with actual user ID
    store_info = get_store_info(user_id)

    if "error" in store_info:
        return "Unauthorized access"

    return render_template('store_info.html', store_info=store_info)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate_user(username, password):
            # Store the username in the session to mark the user as authenticated
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')


if __name__ == '__main__':
    dbname = get_database()
    collection_name = dbname["user_1_items"]
    app.run(debug=True)
