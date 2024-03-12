# Flask imports
from flask import Flask, request, render_template, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_DO_NOT_SHARE"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Login submission
        username = request.form["username"]
        password = request.form["password"]
        user = database.get_user(username)
        # Authentication
        if user and user["password"] == password:
            session["username"] = username
            print("Logged in as " + username)
            return redirect(url_for("home"))
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
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/home")
def home():
    # Check if user is logged in
    if "username" in session:
        food = database.get_products()
        print("FOOD" + str(food))
        return render_template("home.html", username=session["username"], foods=food)
    else:
        return redirect(url_for("index", error="You are not logged in"))


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


@app.route("/logout")
def logout():
    # Remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
