import sqlite3
from flask import Flask, g, jsonify, request

app = Flask(__name__)
DATABASE = "database.db"

# Food table
# id | name | price | rating
food_name = [
    "Pizza",
    "Burger",
    "Pasta",
    "Fries",
    "Salad",
    "Sandwich",
    "Sushi",
    "Ramen",
    "Taco",
    "Burrito",
]
food_price = [10.0, 8.0, 12.0, 6.0, 7.0, 9.0, 15.0, 13.0, 5.0, 7.0]
food_rating = [4.5, 4.0, 4.8, 4.0, 4.2, 4.6, 4.9, 4.7, 4.0, 4.2]


def get_db():
    # Connect to the database if it exists, otherwise create a new one
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    # Create the database
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        # Create users table
        cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
        )
        # Create food table
        cursor.execute(
            "CREATE TABLE food (id INTEGER PRIMARY KEY, name TEXT, price REAL, rating REAL)"
        )
        # Insert food data
        for enum, name in enumerate(food_name):
            cursor.execute(
                "INSERT INTO food (name, price, rating) VALUES (?, ?, ?)",
                (name, food_price[enum], food_rating[enum]),
            )
        # Commit the changes
        conn.commit()


def get_user(username):
    # Get user from database return jsonify(user)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "username": user[1], "password": user[2]}
    return None


def add_user(username, password):
    # Add user to database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )
    conn.commit()
    conn.close()
    return True


def get_products():
    # Get products from database return jsonify(products)
    conn = get_db()
    print('in get_products()')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food")
    products = cursor.fetchall()
    if products:
        for enum, product in enumerate(products):
            products[enum] = {
                "id": product[0],
                "name": product[1],
                "price": product[2],
                "rating": product[3],
            }
        return products
    conn.close()
    return None

def get_productss(item):
    # Get specific products from database return jsonify(products)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food WHERE name=?", (item,))
    products = cursor.fetchall()
    if products:
        for enum, product in enumerate(products):
            products[enum] = {
                "id": product[0],
                "name": product[1],
                "price": product[2],
                "rating": product[3],
            }
        return products
    conn.close()
    return None


def get_db_data():
    # View the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM food")
    food = cursor.fetchall()
    if users:
        for enum, user in enumerate(users):
            users[enum] = {"id": user[0], "username": user[1], "password": user[2]}
    if food:
        for enum, product in enumerate(food):
            food[enum] = {
                "id": product[0],
                "name": product[1],
                "price": product[2],
                "rating": product[3],
            }
    data = {"users": users, "food": food}
    conn.close()
    return data


def get_user_data():
    # View the database
    user=request.args.get('user')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username=?",(user,))
    users = cursor.fetchall()
    if users:
        for enum, user in enumerate(users):
            users[enum] = {"id": user[0], "username": user[1], "password": user[2]}
    conn.close()
    return users

def generate_food():
    # Generate food data
    conn = get_db()
    cursor = conn.cursor()
    for enum, name in enumerate(food_name):
        cursor.execute(
            "INSERT INTO food (name, price, rating) VALUES (?, ?, ?)",
            (name, food_price[enum], food_rating[enum]),
        )
    conn.commit()
    conn.close()

def update_profile(id,uname,pwd):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("update users set username=?,password=? where id=?",(uname,pwd,id,))
    conn.commit()
    conn.close()

def delete_profile(id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("delete from users where id=?",(id,))
    conn.commit()
    conn.close()

def delete_all():
    # Delete all data from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM food")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")
