import os

from flask import Flask, render_template ,session, request
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
    sql_command = "SELECT title, name FROM books INNER JOIN authors on books.author_id = authors.id"
    books = db.execute(sql_command)
    return render_template("index.html", books=books)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/books/<string:title>")
def book_info(title):
    sql_command = f"SELECT title, name , year from books INNER JOIN authors on books.author_id = authors.id AND books.title='{title}'"
    book = db.execute(sql_command).fetchone()
    return render_template("book.html", book=book)

# Search for individual book
@app.route("/search", methods=["GET"])
def search():
    if request.method == 'GET':
        item =  request.args.get("input-book-search")
        #
        print (item)
        #
        # search a book
        sql_command_isbn = f"SELECT title, name FROM books INNER JOIN authors on books.author_id = authors.id AND books.isbn = '{item}'"
        sql_command_title = f"SELECT title, name FROM books INNER JOIN authors on books.author_id = authors.id AND books.title LIKE '%{item}%'"
        sql_command_author = f"Select title, name from books INNER JOIN authors on books.author_id = authors.id AND authors.name LIKE '%{item}%'"

        if db.execute(sql_command_title).rowcount == 0 and db.execute(sql_command_isbn).rowcount == 0 and db.execute(sql_command_author) == 0:
            return render_template("error.html", message="No book found")
        else:
            books = []
            if(db.execute(sql_command_title).rowcount > 0):
                books = books + list(db.execute(sql_command_title))
            if(db.execute(sql_command_isbn).rowcount > 0):
                books = books + list(db.execute(sql_command_isbn))
            if(db.execute(sql_command_author).rowcount > 0):
                books = books + list(db.execute(sql_command_author))
            print(books)
            return render_template("index.html", books=books)
    else:
        return render_template("error.html", message="Not correct message")
