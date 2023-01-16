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


insert into bill (id, name, status)
values
    (1, "IIS Alfa RUB", "active"),
    (2, "Alfa RUB", "active"),
    (3, "Deposit Alfa RUB", "active"),
    (4, "A Tinkof RUB", "active"),
    (5, "J Tinkof RUB", "active"),
    (6, "J Tinkof IIS RUB", "active"),
    (7, "Binance USD", "active"),
    (8, "TrustWallet old USD", "active"),
    (9, "TrustWallet new USD", "active"),
    (10, "Credit Vitya USD", "active"),
    (11, "Cash USD", "active"),
    (12, "Cash RSD", "active"),
    (13, "Cash EUR", "active"),
    (14, "J Bank of Georgia USD", "active");
-- insert into bill (id, name, status)
-- values
--     (1, "Alfa RUB", "active"),
--     (2, "Tinkof RUB", "active");