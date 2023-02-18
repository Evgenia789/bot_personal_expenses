create table category(
    id integer primary key AUTOINCREMENT,
    name nvarchar(255),
    limit_amount integer
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


-- insert into bill (id, name, amount, status)
-- values
--     (1, "Alfa RUB", 1000, "active"),
--     (2, "Tinkof RUB", 2000, "active");

insert into bill (id, name, amount, status)
values
    (1, "IIS Alfa RUB", 1000, "active"),
    (2, "Alfa RUB", 1000, "acive"),
    (3, "Deposit Alfa RUB", 1000, "acive"),
    (4, "A Tinkof RUB", 1000, "acive"),
    (5, "J Tinkof RUB", 1000, "acive"),
    (6, "J Tinkof IIS RUB", 1000, "acive"),
    (7, "Binance USD", 1000, "acive"),
    (8, "TrustWallet old USD", 1000, "acive"),
    (9, "TrustWallet new USD", 1000, "acive"),
    (10, "Credit Vitya USD", 1000, "acive"),
    (11, "Cash USD", 1000, "acive"),
    (12, "Cash RSD", 1000, "acive"),
    (13, "Cash EUR", 1000, "acive"),
    (14, "J Bank of Georgia USD", 1000, "active");