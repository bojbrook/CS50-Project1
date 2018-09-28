import os

from flask import Flask, render_template ,session, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from passlib.hash import sha256_crypt

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
@app.route("/index")
def index():
    if not session.get('logged_in'):
      return render_template('login.html')
    sql_command = "SELECT title, name FROM books INNER JOIN authors on books.author_id = authors.id"
    books = db.execute(sql_command)
    return render_template("index.html", books=books)

@app.route("/sign-up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form.get("inputName")
    userName = request.form.get("inputUserName")
    password = sha256_crypt.encrypt(request.form.get("inputPassword"))

    print(f"Name: {name} Username: {userName} Hash: {password}")
    sql_check_user_command = f"SELECT * FROM users WHERE username='{userName}'"
    print (password)
    
    if(db.execute(sql_check_user_command).rowcount > 0):
        return "Username is in use"

    insert_user_sql_command = "INSERT INTO users (name, username, password) VALUES (:name,:userName,:password)"
    db.execute(insert_user_sql_command,{"name": name, "userName": userName, "password": password})
    db.commit()

    return redirect(url_for('sign_up'))
    # return redirect(url_for('index'))
@app.route("/login", methods=["POST"])
def login():
    if request.form['InputPassword'] == 'password' and request.form['InputUsername'] == 'bojbrook':
       session['logged_in'] = True
    else:
        print("Wrong input")
    return redirect(url_for('index'))


@app.route("/books/<string:title>")
def book_info(title):
    get_book_sql_command = f"SELECT title, name , year FROM books INNER JOIN authors on books.author_id = authors.id AND books.title='{title}'"
    get_review_sql_command = f"SELECT username, title, review FROM ((user_reviews \
	                            INNER JOIN books ON user_reviews.book_id = books.id AND books.title='{title}') \
	                            INNER JOIN users ON user_reviews.user_id = users.id) "
                                
    book = db.execute(get_book_sql_command).fetchone()
    reviews = db.execute(get_review_sql_command)
    return render_template("book.html", book=book, reviews=reviews)

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
