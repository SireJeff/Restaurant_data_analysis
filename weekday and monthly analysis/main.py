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

# Calculate weekly sales per day
print("Calculating weekly sales per day...")
merged_df['DayOfWeek'] = merged_df.index.day_name()
weekly_sales_per_day = merged_df.groupby('DayOfWeek').sum()[price_column]
print("Weekly Sales Per Day:\n", weekly_sales_per_day)

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

# Ensure 'Tarikh' is part of the DataFrame
print("Calculating monthly sales in three parts based on Persian dates...")
monthly_sales_parts_persian = merged_df.groupby(['Tarikh', 'MonthPart']).sum()[price_column]
print("Monthly Sales in Three Parts (Persian):\n", monthly_sales_parts_persian)

# Save the results to new Excel files
print("Saving results to Excel files...")
weekly_sales_per_day.to_excel('Weekly_Sales_Per_Day.xlsx')
monthly_sales_parts_persian.to_excel('Monthly_Sales_Parts_Persian.xlsx')

print("Analysis completed and results saved.")

in this code for week and month based nalaysis i don't need to merge all the table, i just need it to bedone based on the Rfaktors modify it so that it gives me the per weekdays analysis and the per monthly 3 divison data only based on Rfaktors:
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

# Calculate weekly sales per day
print("Calculating weekly sales per day...")
merged_df['DayOfWeek'] = merged_df.index.day_name()
weekly_sales_per_day = merged_df.groupby('DayOfWeek').sum()[price_column]
print("Weekly Sales Per Day:\n", weekly_sales_per_day)

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

# Ensure 'Tarikh' is part of the DataFrame
print("Calculating monthly sales in three parts based on Persian dates...")
monthly_sales_parts_persian = merged_df.groupby(['Tarikh', 'MonthPart']).sum()[price_column]
print("Monthly Sales in Three Parts (Persian):\n", monthly_sales_parts_persian)

# Save the results to new Excel files
print("Saving results to Excel files...")
weekly_sales_per_day.to_excel('Weekly_Sales_Per_Day.xlsx')
monthly_sales_parts_persian.to_excel('Monthly_Sales_Parts_Persian.xlsx')

print("Analysis completed and results saved.")


