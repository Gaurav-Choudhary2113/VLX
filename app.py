import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///VLX.db")

#CACHE NONSENSE-----------------------------------
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#HOME PAGE-------------------------------------

@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html")

#LOGIN------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        rows = db.execute(
            "SELECT * FROM Users WHERE Username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hashed_pwd"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

        # Redirect user to home page
        return redirect("/userhome")
    else:
        return render_template("login.html")

#REGISTER-----------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        username = request.form.get("username")
        hashed_password = generate_password_hash(request.form.get("password"))
        email = request.form.get("email")

        try:
            registrant = db.execute(
                "INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)",
                username, hashed_password, email
            )
            
        except:
            return apology("Username exists", 400)

        session["user_id"] = registrant

        flash("Registered!")
        return redirect("/userhome")

    else:
        return render_template("register.html")
