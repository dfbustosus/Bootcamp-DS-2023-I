-- WHERE

SELECT * FROM  Customers 
WHERE  Country = “Mexico”;

SELECT * FROM  Products 
WHERE  Price = 18;

SELECT * FROM  Products 
WHERE  Price BETWEEN 50 AND 60

SELECT * FROM  Customers 
WHERE  City LIKE 's%' OR '%a'

--- AND, OR , NOT

SELECT * FROM  Customers 
WHERE  City = 'Berlin' OR City = 'Munchen'

SELECT * FROM  Customers 
WHERE  City = 'Berlin' AND City = 'Munchen'

SELECT * FROM  Customers 
WHERE  Country = 'Germany' OR Country = 'Spain'

SELECT * FROM  Customers 
WHERE NOT  Country = 'Germany'

SELECT * FROM  Customers 
WHERE Country = 'Germany' AND (City = 'Berlin' OR City = 'Munchen')

SELECT * FROM  Customers 
WHERE NOT Country = 'Germany' AND NOT Country = 'USA' 

-- SELECT TOP

SELECT * FROM  Customers 
LIMIT 3;

SELECT * FROM  Customers 
WHERE  Country ='Germany'
LIMIT 3

-- LIKE
SELECT * FROM  Customers 
WHERE CustomerName LIKE 'a%';

SELECT  * FROM  Customers 
WHERE CustomerName LIKE '%e';

SELECT  * FROM  Customers 
WHERE CustomerName LIKE '%or%';

SELECT  * FROM  Customers 
WHERE CustomerName LIKE '_r%';

-- ALIASING
SELECT CustomerID AS ID,  CustomerName AS Customer
FROM Customers;

SELECT CustomerName AS Customer,  ContactName AS [Contact Person]
FROM Customers;

SELECT  CustomerName, Address + ',  ' + PostalCode + '    ' + City +  ',  ' + Country AS Address FROM Customers

-- COMMENTS
-- SELECT * FROM Customers
SELECT * FROM Products;

SELECT * FROM Customers --  WHERE City = ‘Berlin’

/* Comentario largo de control de cambios para regulacion */ 
SELECT * FROM Customers 

/* SELECT Comentario largo de control de cambios para regulacion */ 
SELECT * FROM Customers 

-- CASE END 

SELECT OrderID, Quantity,
CASE 
  WHEN Quantity > 30 THEN 'Mayor30'
  WHEN Quantity = 30 THEN 'Igual30'
  ELSE 'Menor30'
END AS  TextoCantidad


SELECT CustomerName, City, Country
FROM  Customers
ORDER BY 
(CASE 
     WHEN City  IS NULL THEN Country
     ELSE City
END)

-- IN
SELECT * FROM Customers 
WHERE Country IN ('Germany','France','UK')

SELECT * FROM Customers 
WHERE Country NOT IN ('Germany','France','UK')

SELECT * FROM  Customers 
WHERE  Country IN 
(SELECT Country FROM Suppliers) 

-- BETWEEN
SELECT * FROM  Products 
WHERE  Price BETWEEN  10 AND 20;

SELECT * FROM  Products 
WHERE  Price NOT BETWEEN  10 AND 20;

SELECT * FROM  Products 
WHERE  Price BETWEEN  10 AND 20
AND CategoryID NOT IN (1,2,3) 

SELECT * FROM  Products 
WHERE ProductName BETWEEN  'Carnarvon Tigers' AND 'Mozzarella di Diobanni'
ORDER BY ProductName


-- ANY
SELECT ProductName 
FROM Products 
WHERE ProductID IN 
  (SELECT ProductID 
   FROM OrderDetails 
   WHERE Quantity > 99);

SELECT ProductName 
FROM  Products
WHERE ProductID IN  
  (SELECT ProductID 
   FROM OrderDetails
   WHERE Quantity >1000)

-- ALL (No existE)

-- JOINS
SELECT Customers.CustomerName, Orders.OrderID
FROM  Orders
INNER JOIN  Customers ON Orders.CustomerID= Customers.CustomerID 
ORDER BY Customers.CustomerName

SELECT Customers.CustomerName, Orders.OrderID
FROM  Customers
LEFT JOIN  Orders ON Customers.CustomerID= Orders.CustomerID 
ORDER BY Customers.CustomerName

SELECT Orders.OrderID, Employees.LastName, Employees.FirstName
FROM  Orders
RIGHT JOIN  Employees ON Orders.EmployeeID= Employees.EmployeeID 
ORDER BY Orders.OrderID

SELECT Customers.CustomerName, Orders.OrderID
FROM  Customers
INNER JOIN  Orders ON Customers.CustomerID= Orders.CustomerID 
ORDER BY Customers.CustomerName

- ORDER BY

SELECT COUNT (CustomerID) as CONTEO
FROM  Customers
GROUP BY Country 
ORDER BY CONTEO DESC

-- HAVING
SELECT COUNT (CustomerID), Country
FROM  Customers
GROUP BY Country 
HAVING COUNT  (CustomerID)>5

SELECT COUNT (CustomerID), Country
FROM  Customers
GROUP BY Country
HAVING COUNT (CustomerID) >5

-- MIN-MAX

SELECT MIN (Price)
AS SmallestPrice
FROM  Products

SELECT MAX (Price)
AS SmallestPrice
FROM  Products

-- COUNT, AVG, SUM

SELECT COUNT (Price)
AS SumPrice, COUNT (ProductID)
FROM  Products

SELECT AVG (Price)
AS SumPrice, COUNT (ProductID)
FROM  Products

-- Actividad
-- Parte I
-- o.*, c.*, s.* esto selecciona todas las columnas con los alias

SELECT o.*, c.*, s.*
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Shippers s ON o.ShipperID = s.ShipperID;

-- Parte II
SELECT s.ShipperName, COUNT(*) AS TotalOrders
FROM Orders o
JOIN Shippers s ON o.ShipperID = s.ShipperID
GROUP BY s.ShipperName;


