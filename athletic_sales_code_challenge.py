import pandas as pd

# Combine and Clean the Data
# Load the data
sales_2020 = pd.read_csv("athletic_sales_2020.csv")
sales_2021 = pd.read_csv("athletic_sales_2021.csv")

# Check column consistency
assert list(sales_2020.columns) == list(sales_2021.columns), "Columns do not match!"

# Combine the DataFrames
combined_sales = pd.concat([sales_2020, sales_2021], ignore_index=True)

# Convert "invoice_date" to datetime
combined_sales['invoice_date'] = pd.to_datetime(combined_sales['invoice_date'])

# Ensure the data type is changed
assert combined_sales['invoice_date'].dtype == 'datetime64[ns]', "invoice_date is not datetime!"

# Determine which Region Sold the Most Products
products_sold = combined_sales.groupby(['region', 'state', 'city'])['units_sold'].sum().reset_index()
products_sold = products_sold.rename(columns={'units_sold': 'Total_Products_Sold'}).sort_values(
    by='Total_Products_Sold', ascending=False).head(5)

# Determine which Region had the Most Sales
sales_by_region = combined_sales.groupby(['region', 'state', 'city'])['total_sales'].sum().reset_index()
sales_by_region = sales_by_region.rename(columns={'total_sales': 'Total_Sales'}).sort_values(
    by='Total_Sales', ascending=False).head(5)

# Determine which Retailer had the Most Sales
sales_by_retailer = combined_sales.groupby(['retailer', 'region', 'state', 'city'])['total_sales'].sum().reset_index()
sales_by_retailer = sales_by_retailer.rename(columns={'total_sales': 'Total_Sales'}).sort_values(
    by='Total_Sales', ascending=False).head(5)

# Determine which Retailer Sold the Most Women's Athletic Footwear
womans_footwear_sales = combined_sales[combined_sales['product'] == "Women's Athletic Footwear"]
sales_by_retailer_women = womans_footwear_sales.groupby(['retailer', 'region', 'state', 'city'])['units_sold'].sum().reset_index()
sales_by_retailer_women = sales_by_retailer_women.rename(columns={'units_sold': 'womans_Footwear_Units_Sold'}).sort_values(
    by='womans_Footwear_Units_Sold', ascending=False).head(5)

# Determine the Day with the Most Women's Athletic Footwear Sales
daily_sales_women = womans_footwear_sales.groupby('invoice_date')['total_sales'].sum().reset_index()
daily_sales_women = daily_sales_women.rename(columns={'total_sales': 'Daily_Sales'}).sort_values(
    by='Daily_Sales', ascending=False).head(10)

# Determine the Week with the Most Women's Athletic Footwear Sales
weekly_sales_women = womans_footwear_sales.resample('W', on='invoice_date')['total_sales'].sum().reset_index()
weekly_sales_women = weekly_sales_women.rename(columns={'total_sales': 'Weekly_Sales'}).sort_values(
    by='Weekly_Sales', ascending=False).head(10)

# Display Results
print("Top 5 Regions that Sold the Most Products:")
print(products_sold)

print("\nTop 5 Regions with the Most Sales:")
print(sales_by_region)

print("\nTop 5 Retailers with the Most Sales:")
print(sales_by_retailer)

print("\nTop 5 Retailers that Sold the Most Women's Athletic Footwear:")
print(sales_by_retailer_women)

print("\nTop 10 Days with the Most Women's Athletic Footwear Sales:")
print(daily_sales_women)

print("\nTop 10 Weeks with the Most Women's Athletic Footwear Sales:")
print(weekly_sales_women)
