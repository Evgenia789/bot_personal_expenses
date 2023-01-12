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
    amount float,
    category_id integer,
    bill_id integer,
    date TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES category(id),
    FOREIGN KEY(bill_id) REFERENCES bil(id)
);


insert into category (id, name, limit_amount)
values
    (1, "Supermarkets", 350),
    (2, "Cafes and restaurants", 150),
    (3, "Transport", 50),
    (4, "Housing", 900),
    (5, "Clothes", 100),
    (6, "Household Goods", 100),
    (7, "Cat", 50),
    (8, "Medicine", 100),
    (9, "Entertainments", 50),
    (10, "Other", 100);
