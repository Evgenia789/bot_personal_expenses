create table category(
    id integer primary key AUTOINCREMENT,
    name nvarchar(255),
    limit_amount integer
);

create table bill(
    id integer primary key AUTOINCREMENT,
    name varchar(255),
    status varchar(255)
);

create table item(
    id integer primary key AUTOINCREMENT,
    amount integer,
    category_id integer,
    bill_id integer,
    date TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES category(id),
    FOREIGN KEY(bill_id) REFERENCES bil(id)
);


insert into category (id, name, limit_amount)
values
    (1, "Supermarkets", 500),
    (2, "Cafes and restaurants", 500),
    (3, "Transport", 500),
    (4, "Housing", 500),
    (5, "Clothes", 500),
    (6, "Household Goods", 500),
    (7, "Cat", 500),
    (8, "Medicine", 500),
    (9, "Entertainments", 500),
    (10, "Other", 500);
