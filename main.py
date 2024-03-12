# Flask imports
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_DO_NOT_SHARE"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Login submission
        username = request.form["username"]
        password = request.form["password"]
        # Authentication (later)
        if username == "admin" and password == "pass":
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
        # Add user to database (later)
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/home")
def home():
    # Check if user is logged in
    if "username" in session:
        return render_template("home.html", username=session["username"])
    else:
        return redirect(url_for("index", error="You are not logged in"))


@app.route("/logout")
def logout():
    # Remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
