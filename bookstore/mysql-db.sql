DROP DATABASE IF EXISTS bookstore;
CREATE DATABASE bookstore;
USE bookstore;

CREATE TABLE user(
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Password VARCHAR(255),
    Name VARCHAR(255),
    Email VARCHAR(255),
    UserType ENUM('Admin', 'Customer')
);

CREATE TABLE book(
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Price DECIMAL(10,2),
    Stock INT,
    OutOfPrint BOOLEAN
);

CREATE TABLE `order`(
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    BookID INT,
    Quantity INT,
    FOREIGN KEY (UserID) REFERENCES user(UserID),
    FOREIGN KEY (BookID) REFERENCES book(BookID)
);

CREATE VIEW BookOrderSummary AS
SELECT b.BookID, b.Title, b.Author, COUNT(o.OrderID) AS TotalOrders
FROM book b
LEFT JOIN `order` o ON b.BookID = o.BookID
GROUP BY b.BookID;


-- Stored Procedure for total sales
DELIMITER //
CREATE PROCEDURE GetTotalSales(IN book_id INT)
BEGIN
SELECT
    SUM(Price * Quantity) as TotalCost
    FROM (
    SELECT o.BookID, o.Quantity, b.Price
    FROM `order` as o
    JOIN book as b on o.BookID = b.BookID
    WHERE o.BookID = book_id) as books;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateBookStock(IN book_id INT, quantity_sold INT)
BEGIN
    UPDATE book SET Stock = Stock - quantity_sold WHERE BookID = book_id;
END //
DELIMITER ;


INSERT INTO user (Password, Name, Email, UserType) VALUES ('scrypt:32768:8:1$W7hiZnepCwFlFuDg$6b7e4fede305e7fa0358f5fcf5a7014a62eca72632ed818ffd0e1aa4018c7f9724bd44d30dfcc9062f8d98fb20ad798b8d42261f96e0bbe924e21d76ab50a224', 'User1', 'user1@example.com', 'Customer');
INSERT INTO user (Password, Name, Email, UserType) VALUES ('scrypt:32768:8:1$BuPfJLF0nLkQACBN$aac622075eba4d1dd37fb22764b9712700b4ead62c98804bc10ff43514810b4be6a1bd03cd971d904385d112478b3f445548f0cca94bacc17061fbc44b0b2bca', 'User2', 'user2@example.com', 'Customer');
INSERT INTO user (Password, Name, Email, UserType) VALUES ('scrypt:32768:8:1$43yL3klwddXHBySa$f7d10ec2d23e25c2072926a9ae496277137363beac1a29318f4fd045d6582f2e45617abcfd2af101e0aab17676422387a8c6a286a89b68d939f5c0b4c64a75dc', 'User3', 'user3@example.com', 'Customer');
INSERT INTO user (Password, Name, Email, UserType) VALUES ('scrypt:32768:8:1$eMPOGt9BBD9TOT3P$e2cbec97ad1e7d163a52c747d49ec45ae15ac463b3a693ede7a4162c43cb681c96832e128cae9aa109ade300eee128079f8abaf2e89ba200affc0d4e5687111d', 'User4', 'user4@example.com', 'Customer');
INSERT INTO user (Password, Name, Email, UserType) VALUES ('scrypt:32768:8:1$GASJ50sn5WNHd0rO$f3649c6e5f89287346a48a68d3c87d505a75d73eac7b533ce05a997064220796f96f982a2baa5e6d4f190a3d37f9ff03dc7f5c87312083a051738afb1c214218', 'User5', 'user5@example.com', 'Customer');
INSERT INTO user (Password, Name, Email, UserType) VALUES ('scrypt:32768:8:1$cGBKP5dUb1ZLkOS7$eef3a7cb0600c0c3df4d47a5c985e2c68628b60564248b4113a88b0bb6631a6c0e7589e350212aaab329c7e9cd71081fce06e0f09128255c7226d6c0cff9cd8c', 'Admin', 'admin@example.com', 'Admin');

INSERT INTO book (Title, Author, Price, Stock, OutOfPrint) VALUES ('Machine Learning ', 'Christopher Bishop', 11, 6, false);
INSERT INTO book (Title, Author, Price, Stock, OutOfPrint) VALUES ('Introduction to Thermodynamics', 'Charles Kittel', 12, 7, false);
INSERT INTO book (Title, Author, Price, Stock, OutOfPrint) VALUES ('Algebraic Art ', 'Leonardo da Vinci', 13, 8, false);
INSERT INTO book (Title, Author, Price, Stock, OutOfPrint) VALUES ('Time Series Forecasting', 'Oliver Theobald', 14, 9, false);
INSERT INTO book (Title, Author, Price, Stock, OutOfPrint) VALUES ('Improvise or Die', 'Angus MacGuyver', 15, 10, false);

INSERT INTO `order` (UserID, BookID, Quantity) VALUES (2, 2, 2);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (3, 3, 3);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (4, 4, 1);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (5, 5, 2);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (1, 1, 3);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (2, 2, 1);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (3, 3, 2);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (4, 4, 3);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (5, 5, 1);
INSERT INTO `order` (UserID, BookID, Quantity) VALUES (1, 1, 2);