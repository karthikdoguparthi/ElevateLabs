CREATE TABLE ecommerce_data (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INTEGER,
    InvoiceDate DATE,
    UnitPrice FLOAT,
    CustomerID INTEGER,
    Country VARCHAR(30)
);

--0 Dataset
select * from ecommerce_data limit 3;

--1 Select distinct customerID
Select Count(distinct customerid) from ecommerce_data;

--2 Select top 10 Orders by date
Select invoicedate, count(*) as DailyOrders 
from ecommerce_data
group by invoicedate
limit 10;

--3 Select top 5 customers ordered ignoring null category
Select CustomerID, count(*) as TotalQuantity
from ecommerce_data
group by CustomerID
order by totalquantity desc
offset 1
limit 5;


--4 Information about top 10 countries that ordered highest
Select country, count(*) as CountryOrders
from ecommerce_data
group by country
order by CountryOrders desc
limit 10;

--5 Information about top 10 invoice dates and invoice numbers 
Select invoicedate, invoiceno, count(*) as InvoiceOrders
from ecommerce_data
group by invoicedate, invoiceno
order by invoiceorders desc
limit 10;

--6 Information about top 10 unique descriptions and regular descriptions for invoice numbers
select invoiceno, count(distinct description) as unique_description_count, 
count(description) as Description_count
from ecommerce_data
group by invoiceno
order by unique_description_count desc
limit 10;

--7 Information about top 10 ordered items
select stockcode, count(*) as stockcount
from ecommerce_data
group by stockcode
order by stockcount desc
limit 10;

--8 Top 10 stockcode from country
select country, stockcode, count(*) as country_stock_orders
from ecommerce_data
group by country, stockcode
order by country_stock_orders desc
limit 10;

--9 Top 3 StockCodes per Country by count of appearance
SELECT Country, StockCode, stock_count
FROM (
    SELECT 
        Country,
        StockCode,
        COUNT(*) AS stock_count,
        ROW_NUMBER() OVER (PARTITION BY Country ORDER BY COUNT(*) DESC) AS rn
    FROM ecommerce_data
    GROUP BY Country, StockCode
	ORDER BY country DESC, stock_count DESC
) sub
WHERE rn <= 3
OFFSET 3;

--10 Top 3 StockPrices per Country by count of appearance
SELECT Country, StockCode, stock_price
FROM (
    SELECT 
        Country,
        StockCode,
        COUNT(unitprice) AS stock_price,
        ROW_NUMBER() OVER (PARTITION BY Country ORDER BY COUNT(*) DESC) AS rn
    FROM ecommerce_data
    GROUP BY Country, StockCode
	ORDER BY country DESC, stock_price DESC
) sub
WHERE rn <= 3
OFFSET 3;

