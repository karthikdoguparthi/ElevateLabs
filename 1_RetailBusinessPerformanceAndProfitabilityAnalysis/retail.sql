use Retail;


select count(Transaction_ID) from retail_dataset;

select * from retail_dataset limit 3;

# Checking duplicate records
SELECT *
FROM retail_dataset r
JOIN (
    SELECT Transaction_ID, COUNT(*) AS count
    FROM retail_dataset
    GROUP BY Transaction_ID
    HAVING COUNT(*) > 1
) d
ON r.Transaction_ID = d.Transaction_ID;

#Check any null values
SELECT 
    SUM(CASE WHEN Transaction_ID IS NULL THEN 1 ELSE 0 END) AS Transaction_ID_nulls,
    SUM(CASE WHEN Date IS NULL THEN 1 ELSE 0 END) AS Date_nulls,
    SUM(CASE WHEN Customer_Name IS NULL THEN 1 ELSE 0 END) AS Customer_Name_nulls,
    SUM(CASE WHEN Product IS NULL THEN 1 ELSE 0 END) AS Product_nulls,
    SUM(CASE WHEN Total_Items IS NULL THEN 1 ELSE 0 END) AS Total_Items_nulls,
    SUM(CASE WHEN Total_Cost IS NULL THEN 1 ELSE 0 END) AS Total_Cost_nulls,
    SUM(CASE WHEN Payment_Method IS NULL THEN 1 ELSE 0 END) AS Payment_Method_nulls,
    SUM(CASE WHEN City IS NULL THEN 1 ELSE 0 END) AS City_nulls,
    SUM(CASE WHEN Store_Type IS NULL THEN 1 ELSE 0 END) AS Store_Type_nulls,
    SUM(CASE WHEN Discount_Applied IS NULL THEN 1 ELSE 0 END) AS Discount_Applied_nulls,
    SUM(CASE WHEN Customer_Category IS NULL THEN 1 ELSE 0 END) AS Customer_Category_nulls,
    SUM(CASE WHEN Season IS NULL THEN 1 ELSE 0 END) AS Season_nulls,
    SUM(CASE WHEN Promotion IS NULL THEN 1 ELSE 0 END) AS Promotion_nulls
FROM retail_dataset;


# Splitting date column to date and time columns
ALTER TABLE retail_dataset 
ADD COLUMN Order_Date DATE,
ADD COLUMN Order_Time TIME;

UPDATE retail_dataset
SET 
    Order_Date = DATE(STR_TO_DATE(Date, '%Y-%m-%d %H:%i:%s')),
    Order_Time = TIME(STR_TO_DATE(Date, '%Y-%m-%d %H:%i:%s'));

# Payment count
select Payment_Method, count(Payment_Method) as payment_count
from retail_dataset 
group by Payment_Method
order by payment_count desc;

# Payment count in each city
select City, Payment_Method, count(Payment_Method) as Payment_Count
from retail_dataset 
group by Payment_Method, city
order by City, Payment_Count desc ;

# Product count sold in different store
select Product, Store_Type, count(*) as CNT
from retail_dataset
group by Product,Store_Type
order by CNT desc;

# Most sold product at type of store
SELECT Store_Type, Product, Total_Sold
FROM (
    SELECT 
        Store_Type,
        Product,
        SUM(Total_Items) AS Total_Sold,
        ROW_NUMBER() OVER (PARTITION BY Store_Type ORDER BY SUM(Total_Items) DESC) AS rn
    FROM retail_dataset
    GROUP BY Store_Type, Product
    order by Total_Sold desc
) ranked
WHERE rn = 1;

# Least sold product combination at type of store
SELECT Store_Type, Product, Total_Sold
FROM (
    SELECT 
        Store_Type,
        Product,
        SUM(Total_Items) AS Total_Sold,
        ROW_NUMBER() OVER (PARTITION BY Store_Type ORDER BY SUM(Total_Items)) AS rn
    FROM retail_dataset
    GROUP BY Store_Type, Product
    order by Total_Sold desc
) ranked
WHERE rn = 1;

# Yearly sales
select year(Order_Date) as Order_Year, sum(Total_Items) as Item_sales,
	round(sum(Total_Cost),2) as Item_cost 
from retail_dataset
group by Order_Year
order by Order_Year;

# Seasonwise sales
select year(Order_Date) as Order_Year, Season,
	round(sum(Total_Cost),2) as Item_cost 
from retail_dataset
group by Order_Year, Season
order by Order_Year;

# Yearly payment method
select year(Order_Date) as Order_Year, Payment_Method, count(*) as Payment_count
from retail_dataset
group by Order_year, Payment_Method
order by Order_year, Payment_count desc;

#Citywise sales
Select City, count(*) as Sales
from retail_dataset
group by City
order by Sales desc;

# Top buyers
Select Customer_Name, round(sum(Total_Cost),2) as Sales
from retail_dataset
group by Customer_Name
order by Sales desc
limit 10;

# Storewise sales
Select Store_Type, count(*) as Sales
from retail_dataset
group by Store_Type
order by Sales desc;

# Promotion sales per city
Select City, Promotion, round(sum(Total_Cost),2) as Promotion_sales
from retail_dataset
group by City, Promotion
order by City,Promotion_sales;

#Product wise sales per city
select City, Product, round(sum(Total_Cost),2) as Sales
from retail_dataset
group by City, Product
order by City, Sales desc;


