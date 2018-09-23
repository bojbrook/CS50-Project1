import os

from flask import Flask, render_template ,session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    books = db.execute("select * from books")
    return render_template("index.html", books=books)

@app.route("/books")
def books():
    sql_command = "SELECT title, name FROM books INNER JOIN authors on books.author_id = authors.id"
    books = db.execute(sql_command)
    return render_template("index.html", books=books)

@app.route("/search/<string:item>")
def search(item):
    sql_command = f"SELECT title, name FROM books INNER JOIN authors on books.author_id = authors.id AND books.isbn='{item}'"
    if db.execute(sql_command).rowcount == 0:
        return render_template("error.html", message="No book found")
    else:
        books = db.execute(sql_command)
        return render_template("index.html", books=books)
