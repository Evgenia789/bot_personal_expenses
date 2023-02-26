create table category(
    id integer primary key AUTOINCREMENT,
    name nvarchar(255),
    limit_amount integer,
    status varchar(255)
);

create table bill(
    id integer primary key AUTOINCREMENT,
    name varchar(255),
    amount float,
    status varchar(255)
);

create table item(
    id integer primary key AUTOINCREMENT,
    amount float,
    category_id integer,
    bill_id integer,
    date TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES category(id),
    FOREIGN KEY(bill_id) REFERENCES bil(id)
);

create table income(
    id integer primary key AUTOINCREMENT,
    amount float,
    bill_id integer,
    date TIMESTAMP,
    FOREIGN KEY(bill_id) REFERENCES bil(id)
);


insert into category (id, name, limit_amount, status)
values
    (1, "Supermarkets", 350, "active"),
    (2, "Cafes and restaurants", 150, "active"),
    (3, "Transport", 50, "active"),
    (4, "Housing", 900, "active"),
    (5, "Clothes", 100, "active"),
    (6, "Household Goods", 100, "active"),
    (7, "Cat", 50, "active"),
    (8, "Medicine", 100, "active"),
    (9, "Entertainments", 50, "active"),
    (10, "Other", 100, "active");


insert into bill (id, name, amount, status)
values
    (1, "Alfa RUB", 1000, "active"),
    (2, "Tinkof RUB", 2000, "active");