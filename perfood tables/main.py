import pandas as pd
from convertdate import persian, gregorian

# Load the data from the Excel files
print("Loading data...")
rsfaresh_df = pd.read_excel('RSefaresh.xlsx')
rfakitm_df = pd.read_excel('Rfakitm.xlsx')
rfaktors_df = pd.read_excel('RFaktors.xlsx')

# Display the loaded data for verification
print("Data loaded successfully.")
print(rsfaresh_df.head())
print(rfakitm_df.head())
print(rfaktors_df.head())

# Function to convert Persian date to Gregorian date
def persian_to_gregorian(date_str):
    year, month, day = map(int, date_str.split('/'))
    return gregorian.from_jd(persian.to_jd(year, month, day))

# Convert 'Tarikh' to Gregorian dates
print("Converting Persian dates to Gregorian dates...")
rfaktors_df['GregorianDate'] = rfaktors_df['Tarikh'].apply(persian_to_gregorian)
rfaktors_df[['GYear', 'GMonth', 'GDay']] = pd.DataFrame(rfaktors_df['GregorianDate'].tolist(), index=rfaktors_df.index)

# Create a new 'Datetime' column with Gregorian dates and 'Saat'
rfaktors_df['Datetime'] = pd.to_datetime(rfaktors_df[['GYear', 'GMonth', 'GDay']].astype(str).agg('-'.join, axis=1) + ' ' + rfaktors_df['Saat'])

print("Dates converted successfully.")
print(rfaktors_df[['Tarikh', 'Saat', 'Datetime']].head())

# Merge the data
print("Merging data...")
merged_df = pd.merge(rfakitm_df, rfaktors_df, on='FID', suffixes=('_item', '_factor'))
merged_df = pd.merge(merged_df, rsfaresh_df, on='KID', suffixes=('', '_order'))

print("Data merged successfully.")
print(merged_df.columns)  # Check the columns to identify any renaming or conflicts
print(merged_df.head())

# Identify the correct column name for the price
print("Identifying price column...")
price_column = 'ghymat_item' if 'ghymat_item' in merged_df.columns else 'ghymat'
print(f"Using price column: {price_column}")

# Set the datetime as index
print("Setting datetime as index...")
merged_df.set_index('Datetime', inplace=True)

# Calculate weekday sales for each item
print("Calculating weekday sales for each item...")
merged_df['DayOfWeek'] = merged_df.index.day_name()
weekday_sales_per_item = merged_df.pivot_table(index='Esm', columns='DayOfWeek', values=price_column, aggfunc='sum', fill_value=0)
print("Weekday Sales Per Item:\n", weekday_sales_per_item.head())

# Function to divide a Persian month into three parts
def persian_month_parts(date_str):
    year, month, day = map(int, date_str.split('/'))
    if day <= 10:
        return 'Part 1'
    elif day <= 20:
        return 'Part 2'
    else:
        return 'Part 3'

print("Dividing Persian month into three parts...")
merged_df['MonthPart'] = merged_df['Tarikh'].apply(persian_month_parts)

# Calculate monthly three-part sales for each item
print("Calculating monthly three-part sales for each item...")
monthly_sales_parts_per_item = merged_df.pivot_table(index='Esm', columns='MonthPart', values=price_column, aggfunc='sum', fill_value=0)
print("Monthly Three-Part Sales Per Item:\n", monthly_sales_parts_per_item.head())

# Save the results to new Excel files
print("Saving results to Excel files...")
weekday_sales_per_item.to_excel('Weekday_Sales_Per_Item.xlsx')
monthly_sales_parts_per_item.to_excel('Monthly_Sales_Parts_Per_Item.xlsx')

print("Analysis completed and results saved.")
