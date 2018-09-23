import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if(db.execute("SELECT * from authors WHERE name = (:name)",{"name": author}).fetchone() is None):
            db.execute("INSERT INTO authors (name) VALUES (:author)",{"author": author})
        else:
            year = int(year)
            author_id = db.execute("SELECT id from authors WHERE name = (:name)",{"name": author}).fetchone().id

            db.execute("INSERT INTO books (isbn,title,author_id,year) VALUES (:isbn, :title, :author_id, :year)",
            {"isbn": isbn, "title": title, "author_id": author_id, "year":year})

    db.commit()
    print ('finished')
    # for isbn, title, author, year in reader:
    #     db.execute("INSERT INTO books (isbn, title, year) VALUES (:origin, :destination, :duration)",
    #                 {"origin": origin, "destination": destination, "duration": duration})
    #     print (f"isbn: {isbn} title: {title} author: {author} year: {year}")


if __name__ == "__main__":
    main()
