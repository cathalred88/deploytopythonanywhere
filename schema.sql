DROP IF EXISTS book;
create table book (
    id INT AUTOINCREMENT primary key,
    title VARCHAR(250),
    author VARCHAR(250),
    price INT
);