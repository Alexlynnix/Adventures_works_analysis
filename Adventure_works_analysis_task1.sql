--- CREATING AND IMPORTING THE TABLES 

CREATE TABLE "AdventureWorks_Sales_2015" (
	"OrderDate"	TEXT,
	"StockDate"	TEXT,
	"OrderNumber"	TEXT,
	"ProductKey"	INTEGER,
	"CustomerKey"	INTEGER,
	"TerritoryKey"	INTEGER,
	"OrderLineItem"	INTEGER,
	"OrderQuantity"	INTEGER
);

--- creating the facts table for sales using the three sales tables

CREATE TABLE FactSales (
 "OrderDate" TEXT,
 "StockDate" TEXT,
 "OrderNumber" TEXT,
 "ProductKey" INTEGER,
 "CustomerKey" INTEGER,
 "TerritoryKey" INTEGER,
 "OrderLineItem" INTEGER,
 "OrderQuantity" INTEGER,
 PRIMARY KEY (OrderNumber, OrderLineItem)
);

---merging and inserting the three sales tables into the newly created factsales table.

INSERT INTO FactSales(OrderDate,StockDate, OrderNumber, ProductKey, CustomerKey, TerritoryKey, OrderLineItem, OrderQuantity)
SELECT OrderDate,StockDate, OrderNumber, ProductKey, CustomerKey, TerritoryKey, OrderLineItem, OrderQuantity
FROM AdventureWorks_Sales_2015;

INSERT INTO FactSales(OrderDate,StockDate, OrderNumber, ProductKey, CustomerKey, TerritoryKey, OrderLineItem, OrderQuantity)
SELECT OrderDate,StockDate, OrderNumber, ProductKey, CustomerKey, TerritoryKey, OrderLineItem, OrderQuantity
FROM AdventureWorks_Sales_2016;

INSERT INTO FactSales(OrderDate,StockDate, OrderNumber, ProductKey, CustomerKey, TerritoryKey, OrderLineItem, OrderQuantity)
SELECT OrderDate,StockDate, OrderNumber, ProductKey, CustomerKey, TerritoryKey, OrderLineItem, OrderQuantity
FROM AdventureWorks_Sales_2017;

---renaming the returns table to a fact returns TABLE

ALTER TABLE AdventureWorks_Returns RENAME TO FactReturns;

-- renaming and other tables to become a dimension table for easier interaction

ALTER TABLE AdventureWorks_Customers RENAME TO DimCustomer;
ALTER TABLE AdventureWorks_Product_Categories RENAME TO DimProductCategories;
ALTER TABLE AdventureWorks_Product_Subcategories RENAME TO DimProduct_Subcategories;
ALTER TABLE AdventureWorks_Products RENAME TO DimProducts;
ALTER TABLE AdventureWorks_Territories RENAME TO DimTerritories;

--- creating the dimension calender table. the AdventureWorks_Calendar has only date where the month and year is written together in one column, but with the new dimension calender table, the month and year will be plitted into different columns.
CREATE TABLE DimCalendars(
 "OrderDate" TEXT,
 "Year" TEXT,
 "Month" TEXT,
 PRIMARY KEY (OrderDate)
 );
 
 ---splitting and inserting the AdventureWorks_Calendar into the newly created DimCalendars
 INSERT INTO DimCalendars(OrderDate, Year, Month)
 SELECT Date,
 CAST(substr(Date,-4) as INTEGER) as Year, 
 CAST(substr(Date, 1, 2) as INTEGER) as Month
FROM AdventureWorks_Calendar;

---creating a new FactReturn table that has a unique field/column, introducing the returnindex column into the table.

CREATE TABLE "FactReturn" (
	"ReturnIndex"   INTEGER PRIMARY KEY AUTOINCREMENT,
	"ReturnDate"	TEXT,
	"TerritoryKey"	INTEGER,
	"ProductKey"	INTEGER,
	"ReturnQuantity"	INTEGER
);

--- inserting the FactReturns table into the newly created table with returnindex column.

INSERT INTO FactReturn(ReturnDate, TerritoryKey, ProductKey, ReturnQuantity)
SELECT ReturnDate, TerritoryKey, ProductKey, ReturnQuantity
FROM FactReturns;