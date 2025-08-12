select * from online_sales_dataset;

alter table online_sales_dataset add column TotalPrice double;
alter table online_sales_dataset add column Revenue double;

update online_sales_dataset set TotalPrice = UnitPrice * Quantity;
update online_sales_dataset set Revenue = TotalPrice - (Discount*UnitPrice);

#describing data
describe online_sales_dataset;

#1 Total Revenue after Discounts per Category
Select category, ROUND(SUM(revenue), 2) as Total_Revenue
From online_sales_dataset
Group by category
order by Total_Revenue desc;

#2 Total Revenue after Discounts per Country
Select Country, ROUND(SUM(revenue), 2) as Total_Revenue
From online_sales_dataset
Group by Country
order by Total_Revenue desc;

#3 Total orders from country by category
select Country, Category,
	sum(Quantity) as Total_orders
from online_sales_dataset
group by Country, Category
order by Total_orders desc;


#4 Monthly revenue arranged in Desc order
SELECT
	country,
    extract(year from InvoiceDate) as order_year,
    extract(month from InvoiceDate) as order_month,
    round(sum(revenue), 2) as monthly_revenue
from online_sales_dataset
group by country, order_year, order_month
order by order_year desc, order_month desc, monthly_revenue desc;

#5 Yearly revenue of country in desc order
SELECT
    country,
    extract(year from InvoiceDate) as order_year,
    round(sum(revenue), 2) as monthly_revenue
from online_sales_dataset
group by country, order_year
order by country desc, order_year desc;


#6 Total revenue of distinct items by category
select 
	category,
    Description,
    round(sum(revenue), 2) as Total_revenue
from online_sales_dataset
group by category, Description
order by Total_revenue desc;

#7 Top 3 revenue generated items
Select 
	category,
    description,
    round(sum(revenue), 2) as Total_Revenue
from online_sales_dataset
group by category, Description
order by Total_revenue desc
limit 3;

#8 Top 5 revenue generated customers
select 
	cast(cast(CustomerID as unsigned) AS char) AS CustomerID,
    round(sum(revenue), 2) as Total_Revenue
from online_sales_dataset
group by CustomerID
order by Total_Revenue desc
limit 5
offset 1;

#9 Top 10 payment method counts by customer
select 
	cast(cast(CustomerID as unsigned) AS char) AS CustomerID
    , PaymentMethod
    ,count(*) as Payment_count
from online_sales_dataset
group by CustomerID,PaymentMethod
order by Payment_count desc
limit 10
offset 3;

#10 Top revenue genrated country per year
SELECT country, order_year, total_revenue
FROM (
    SELECT
        country,
        EXTRACT(YEAR FROM InvoiceDate) AS order_year,
        ROUND(sum(revenue), 2) AS total_revenue,
        RANK() OVER (PARTITION BY EXTRACT(YEAR FROM total_revenue)
                     ORDER BY sum(revenue) DESC) AS rnk
    FROM online_sales_dataset
    GROUP BY country, order_year
) t
WHERE rnk = 1
ORDER BY order_year desc;