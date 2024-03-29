# Flask imports
from flask import Flask, request, render_template, redirect, url_for, session
import database, json

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_DO_NOT_SHARE"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Login submission
        username = request.form["username"]
        password = request.form["password"]
        print("got req")
        user = database.get_user(username)
        print("data retrived : " + str(user))
        # Authentication
        if user and user["password"] == password:
            session["username"] = username
            print("Logged in as " + username)
            return redirect(url_for("hometemp"))
        else:
            return render_template("index.html", error="Invalid username or password")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Register submission
        username = request.form["username"]
        password = request.form["password"]
        # Add user to database
        if database.add_user(username, password):
            return redirect(url_for("index"))
        else:
            return render_template("register.html", error="Username already exists")
    return render_template("register.html")


@app.route("/home")
def home():
    # Check if user is logged in
    if "username" in session:
        food = database.get_products()
        print("FOOD" + str(food))
        return render_template("home.html", username=session["username"], foods=food)
    else:
        return render_template("index.html", error="You are not logged in")


@app.route("/hometemp", methods=["GET", "POST"])
def hometemp():
    # Check if user is logged in
    item = request.args.get("item")
    if "username" in session:
        if item is not None and item != "":
            food = database.get_productss(item)
            print("item is " + item)
        else:
            food = database.get_products()
        print("FOOD" + str(food))
        return render_template("fashion.html", username=session["username"], foods=food)
    else:
        return render_template("index.html", error="You are not logged in")


# TODO - Add account page, display user details, update password, delete account
@app.route("/my_profile")
def my_profile():
    if "username" not in session:
        return render_template("index.html", error="You are not logged in")
    data = database.get_user_data()
    print(data)
    return render_template("my_profile.html", users=data)


@app.route("/update_profile")
def update_profile():
    if "username" not in session:
        return render_template("index.html", error="You are not logged in")
    data = database.update_profile(
        request.args.get("id"),
        request.args.get("username"),
        request.args.get("password"),
    )
    return redirect(url_for("logout"))


@app.route("/delete_profile")
def delete_profile():
    if "username" not in session:
        return render_template("index.html", error="You are not logged in")
    data = database.delete_profile(request.args.get("id"))
    return redirect(url_for("logout"))


# TODO add food page, display food details, add food, delete food


@app.route("/database")
def database_view():
    # Display the database contents
    data = database.get_db_data()
    usersData = data["users"]
    foodData = data["food"]
    print(data)
    if not data:
        return "No data in database"
    return render_template("database.html", users=usersData, foods=foodData)


@app.route("/food/<int:food_id>")
def food_view(food_id):
    # Display the food details
    food_json = database.get_food(food_id)
    if not food_json:
        return "Food not found"
    food_data = json.loads(food_json)
    return render_template("food.html", food=food_data)


@app.route("/generate_food", methods=["POST"])
def init_db():
    database.generate_food()
    return redirect(url_for("database_view"))


@app.route("/delete_all", methods=["POST"])
def delete_all():
    database.delete_all()
    return redirect(url_for("database_view"))


@app.route("/logout")
def logout():
    # Remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=8888)
