DROP TABLE IF EXISTS book;
create table book (
    id INTEGER primary key AUTOINCREMENT,
    title VARCHAR(250),
    author VARCHAR(250),
    price INT
);