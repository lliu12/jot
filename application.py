# Lucy Liu
# CS50 Final Project: Jot

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import time
import string

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///jot.db")

# Allow user to enter a new journal entry
@app.route("/", methods=["GET", "POST"])
@login_required
def jot():
    usertags = db.execute("SELECT * FROM tags WHERE userid = :id", id=session["user_id"])
    if request.method == "POST":
        if not request.form.get("entry"):
            return apology("must enter an entry", 403)
        entry = (request.form.get("entry"))
        tag1 = (request.form.get("tag1"))
        tag2 = (request.form.get("tag2"))
        tag3 = (request.form.get("tag3"))
        # Check that all necessary forms are filled out
        db.execute("INSERT INTO entries (userid, entry, tag1, tag2, tag3) VALUES(:id, :entry, :tag1, :tag2, :tag3)",
                   id=session["user_id"], entry=entry, tag1=tag1, tag2=tag2, tag3=tag3)
        return render_template("jot.html", utags = usertags)
    else:
        return render_template("jot.html", utags = usertags)

# View all entries for this user
@app.route("/entries")
@login_required
def entries():
    entries = db.execute("SELECT * FROM entries WHERE userid = :id", id=session["user_id"])
    return render_template("entries.html", entries=entries)


# View user's tags and add a new tag if desired
@app.route("/tags", methods=["GET", "POST"])
@login_required
def tags():
    if request.method == "POST":
        tag = request.form.get("tag")
        tagentries = db.execute("SELECT * FROM entries WHERE (userid = :id) AND (tag1 = :tag OR tag2 = :tag OR tag3= :tag)", id=session["user_id"], tag=tag)
        if (len(tagentries) == 0):
            return render_template("nothingfound.html")
        else:
            return render_template("tag.html", tag=tag, entries=tagentries)
    else:
        tags = db.execute("SELECT * FROM tags WHERE userid = :id", id=session["user_id"])
        return render_template("tags.html", tags=tags)

# Add new tag to database for this user
@app.route("/newtag", methods=["POST"])
@login_required
def newtag():
    if request.method == "POST":
        t = request.form.get("newtag")
        print(t)
        db.execute("INSERT INTO tags (userid, tag) VALUES(:id, :tag)", id=session["user_id"], tag=t)
        tags = db.execute("SELECT * FROM tags WHERE userid = :id", id=session["user_id"])
        return render_template("tags.html", tags=tags)

# Log in
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Register for a new account
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not (not db.execute("SELECT * FROM users WHERE username = :un", un=request.form.get("username"))):
            return apology("username is unavailable")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("password confirmation does not match", 400)
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password confirmation does not match", 400)

        # Insert new user into database
        session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES(:un, :hash)", un=request.form.get(
            "username"), hash=generate_password_hash(request.form.get("password")))

        # Add default tags to database for user
        defaulttags = ["Gratitude", "Memory", "Notes", "Bucketlist"]
        for tag in defaulttags:
            db.execute("INSERT INTO tags (userid, tag) VALUES(:id, :tag)", id=session["user_id"], tag=tag)
        return redirect("/")

    else:
        return render_template("registration.html")

# Log out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Check if username is available
@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    if len(username) >= 1:
        if not db.execute("SELECT * FROM users WHERE username = :un", un=username):
            return jsonify(True)
    return jsonify(False)

# Return apology page
def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
