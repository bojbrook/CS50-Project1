CREATE TABLE authors (
  id SERIAL PRIMARY KEY,
  name VARCHAR UNIQUE NOT NULL
);


CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR UNIQUE NOT NULL,
  title VARCHAR NOT NULL,
  author_id INTEGER REFERENCES authors,
  year INTEGER
);


CREATE TABLE 	users (
	id SERIAL PRIMARY KEY,
	name VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	PASSWORD VARCHAR NOT NULL
);


CREATE TABLE user_reviews(
	id SERIAL PRIMARY KEY,
	book_id INTEGER REFERENCES books,
	user_id INTEGER REFERENCES users,
	review VARCHAR
);


select username, title, review from ((user_reviews 
	INNER JOIN books ON user_reviews.book_id = books.id) 
	INNER JOIN users ON user_reviews.user_id = users.id);