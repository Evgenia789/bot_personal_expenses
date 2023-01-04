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


insert into bill (id, name, status)
values
    (1, "IIS Alfa RUB", "active"),
    (2, "Alfa RUB", "active"),
    (3, "Alfa USD", "active"),
    (4, "Deposit Alfa RUB", "active"),
    (5, "Credit mir Alfa RUB", "active"),
    (6, "Credit MC Alfa RUB", "active"),
    (7, "A Tinkof RUB", "active"),
    (8, "A Tinkof credit RUB", "active"),
    (9, "J Tinkof USD", "active"),
    (10, "J Tinkof RUB", "active"),
    (11, "J Tinkof IIS RUB", "active"),
    (12, "Salary mir RUB", "active"),
    (13, "Binance USD", "active"),
    (14, "TrustWallet old USD", "active"),
    (15, "TrustWallet new USD", "active"),
    (16, "Qiwi RUB", "active"),
    (17, "Credit Vitya USD", "active"),
    (18, "Credit Vitya RUB", "active"),
    (19, "Cash RUB", "active"),
    (20, "Cash USD", "active"),
    (21, "Cash LAR", "active"),
    (22, "J Bank of Georgia USD", "active"),
    (23, "J Bank of Georgia LAR", "active");
