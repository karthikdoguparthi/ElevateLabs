# %% [markdown]
# # Retail Business Performace & Profitability Analysis

# %% [markdown]
# # Project Summary

# %% [markdown]
# My main objective was to analyze transactional retail data in order to uncover profit-draining categories, optimize inventory turnover, and understand seasonal product behavior. To achieve this, I connected my dataset from MySQL into Python using Pandas and SQLAlchemy, then built queries and visualizations to extract meaningful insights.
# 
# The first area I focused on was customer payment behavior. By grouping transactions by payment method, I quickly saw which modes of payment were most popular. Visualizing this with bar charts, both overall and city wise, revealed interesting regional variations. I could clearly see a trend where digital methods were gaining traction compared to traditional cash payments. Understanding this shift is crucial for deciding where to invest in smoother payment integrations.
# 
# I examined product sales by store type. By aggregating counts and building grouped bar charts, I identified which products performed strongly in which types of stores. This showed me that product store fit is real: some categories thrive in supermarkets, while others do better in specialty or online stores. I also highlighted the single top product for each store type, which immediately pointed to anchor products driving revenue.
# 
# Looking at yearly and seasonal sales, I noticed a stable revenue pattern from 2020 to 2023 across all seasons, with a dip appearing in 2024. Seasonal breakdowns helped me see which times of year generated the most revenue and which ones lagged. This kind of insight is important for adjusting inventory planning and targeting promotions at the right time.
# 
# City wise analysis was another key component. Ranking cities by transaction volume showed that a few cities dominate total sales, while others lag far behind. When I layered on promotions, I could see that some regions responded very well, while others hardly moved. That suggests a need for more tailored, region-specific promotional strategies.
# 
# Finally, I looked at customer value distribution by identifying the top buyers. It was striking to see that a small group of customers contributed a large portion of revenue. This reinforced the importance of customer loyalty and retention programs for sustaining long-term profitability.

# %% [markdown]
# # Dataset Loading

# %%
# Libraries

import numpy as np
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings 
warnings.filterwarnings("ignore")


# %%
# Dataset 
dataset = pd.read_csv('Retail_Transactions_Dataset.csv')

# %% [markdown]
# # Dataset Information

# %%
# Libraries

import numpy as np
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Dataset 
dataset = pd.read_csv('Retail_Transactions_Dataset.csv')

# %%
# Display the first few rows of the dataset
print(dataset.head())

# %%
# Display basic information about the dataset
print(dataset.info())

# %%
# Display summary statistics of the dataset
print(dataset.describe(include='all').transpose())

# %%
# Check for missing values in the dataset
print(dataset.isnull().sum())

# %% [markdown]
# # Connection 

# %%
# DB connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port=3306,
    password="admin",
    database="Retail"
 )


engine = create_engine("mysql+mysqlconnector://root:admin@127.0.0.1:3306/Retail")

# Helper
def run_query(query):
    return pd.read_sql(query, conn)

# %% [markdown]
# # Visualizations

# %% [markdown]
# ### Payment Method Distribution
# This chart shows how many transactions were completed using each payment method.  
# It helps us identify the most preferred payment modes by customers.

# %%
df = run_query("""
SELECT Payment_Method, COUNT(Payment_Method) AS payment_count
FROM retail_dataset
GROUP BY Payment_Method
ORDER BY payment_count DESC;
""")

plt.figure(figsize=(8,5))
sns.barplot(x="Payment_Method", y="payment_count", data=df, palette="Set2")
plt.title("Payment Method Distribution")
plt.show()

# %% [markdown]
# ### Payment Methods by City
# This grouped bar chart compares the usage of different payment methods across cities.  
# It highlights regional variations in customer payment preferences.

# %%
df = run_query("""
SELECT City, Payment_Method, COUNT(Payment_Method) AS Payment_Count
FROM retail_dataset
GROUP BY Payment_Method, City
ORDER BY City, Payment_Count DESC;
""")

plt.figure(figsize=(12,6))
sns.barplot(x="City", y="Payment_Count", hue="Payment_Method", data=df, palette="Set2")
plt.title("Payment Methods by City")
plt.xticks(rotation=45)
plt.show()

# %% [markdown]
# ### Top Product by Store Type
# This bar chart highlights the single most sold product within each store type.  
# It reveals which products are the top drivers of sales depending on the store category.

# %%
df = run_query("""
SELECT Store_Type, Product, Total_Sold FROM (
    SELECT Store_Type, Product, SUM(Total_Items) AS Total_Sold,
           ROW_NUMBER() OVER (PARTITION BY Store_Type ORDER BY SUM(Total_Items) DESC) AS rn
    FROM retail_dataset
    GROUP BY Store_Type, Product
) ranked
WHERE rn = 1;
""")
plt.figure(figsize=(8,5))
sns.barplot(x="Total_Sold", y="Store_Type", hue="Product", data=df, dodge=False)
plt.title("Top Product by Store Type")
plt.show()

# %% [markdown]
# ### Yearly Sales (Items vs. Cost)
# This line chart shows the trend of items sold and total revenue over time, year by year.  
# It helps us understand sales growth, seasonal dips, or upward/downward trends.

# %%
df = run_query("""
SELECT YEAR(Order_Date) AS Order_Year, SUM(Total_Items) AS Item_sales,
       ROUND(SUM(Total_Cost),2) AS Item_cost
FROM retail_dataset
GROUP BY Order_Year
ORDER BY Order_Year;
""")
plt.figure(figsize=(8,5))
sns.lineplot(x="Order_Year", y="Item_sales", data=df, marker="o", label="Items Sold")
sns.lineplot(x="Order_Year", y="Item_cost", data=df, marker="s", label="Total Cost")
plt.title("Yearly Sales")
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
plt.legend()
plt.show()

# %% [markdown]
# ### Season-wise Sales per Year
# This grouped bar chart breaks down total sales by season for each year.  
# It shows which seasons contribute the most to yearly sales and seasonal shopping patterns.

# %%
df = run_query("""
SELECT YEAR(Order_Date) AS Order_Year, Season, ROUND(SUM(Total_Cost),2) AS Item_cost
FROM retail_dataset
GROUP BY Order_Year, Season
ORDER BY Order_Year;
""")
plt.figure(figsize=(10,6))
sns.barplot(x="Order_Year", y="Item_cost", hue="Season", data=df)
plt.title("Season-wise Sales per Year")
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
plt.show()

# %% [markdown]
# ### Yearly Payment Method Trends
# This multi-line chart tracks the number of transactions by payment method over time.  
# It reveals shifts in customer payment behavior (e.g., rising card usage, declining cash).

# %%
df = run_query("""
SELECT YEAR(Order_Date) AS Order_Year, Payment_Method, COUNT(*) AS Payment_count
FROM retail_dataset
GROUP BY Order_Year, Payment_Method
ORDER BY Order_Year, Payment_count DESC;
""")
plt.figure(figsize=(10,6))
sns.lineplot(x="Order_Year", y="Payment_count", hue="Payment_Method", data=df, marker="o")
plt.title("Yearly Payment Method Trends")
plt.show()

# %% [markdown]
# ### Citywise Sales
# This horizontal bar chart shows which cities generate the most transactions.  
# It helps identify high-performing cities and regions that need growth strategies.

# %%
df = run_query("""
SELECT City, COUNT(*) AS Sales
FROM retail_dataset
GROUP BY City
ORDER BY Sales DESC;
""")
plt.figure(figsize=(10,6))
sns.barplot(x="Sales", y="City", data=df, palette="coolwarm")
plt.title("Citywise Sales")
plt.show()

# %% [markdown]
# ### Top 10 Buyers
# This bar chart shows the top 10 customers ranked by total spending.  
# It highlights the most valuable customers driving profitability.

# %%
df = run_query("""
SELECT Customer_Name, ROUND(SUM(Total_Cost),2) AS Sales
FROM retail_dataset
GROUP BY Customer_Name
ORDER BY Sales DESC
LIMIT 10;
""")
plt.figure(figsize=(10,6))
sns.barplot(x="Sales", y="Customer_Name", data=df, palette="mako")
plt.title("Top 10 Buyers")
plt.show()

# %% [markdown]
# ### Promotion Sales per City
# This stacked bar chart shows how promotions contribute to sales in different cities.  
# It allows us to evaluate the effectiveness of promotions in boosting revenue by location.

# %%
df = run_query("""
SELECT City, Promotion, ROUND(SUM(Total_Cost),2) AS Promotion_sales
FROM retail_dataset
GROUP BY City, Promotion
ORDER BY City, Promotion_sales;
""")
plt.figure(figsize=(12,6))
sns.barplot(x="City", y="Promotion_sales", hue="Promotion", data=df)
plt.title("Promotion Sales per City")
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
plt.xticks(rotation=45)
plt.show()

# %%
conn.close()

# %% [markdown]
# # Conclusion

# %% [markdown]
# 1.	Customer Payment Behavior
# 
# Bar charts of payment methods show that a few payment options dominate across most cities, but the mix does shift regionally. Tracking these trends year over year highlights a gradual move away from cash towards digital methods, which suggests where to invest in payment integrations.
# 
# 2.	Store Performance and Product Mix
# 
# Comparing product counts across store types makes it clear that certain products anchor sales in specific store formats. For example, large store types push bulk or high value products, while smaller outlets lean on fast-moving essentials. This helps identify which SKUs are profit drivers per channel.
# 
# 3.	Seasonality and Yearly Trends
# 
# Seasonal analysis shows consistent peaks in spending across all seasons from 2020 to 2023, with a noticeable dip in 2024. Yearly sales trends confirm a stable base but also reveal signs of slowdown. Inventory and promotional strategies should be adjusted to counterbalance those seasonal gaps.
# 
# 4.	Geographic and Promotional Impact
# 
# City wise sales rankings point out a handful of cities contributing the majority of revenue. Promotions do boost sales, but their effectiveness varies by region some cities respond strongly, others hardly move. This suggests the need for location targeted promotions rather than blanket campaigns.
# 
# 5.	Customer Value Distribution
# 
# The top buyers chart shows a small set of customers contribute a disproportionate share of revenue. This concentration highlights the importance of loyalty programs and retention strategies for high-value customers.
# 


