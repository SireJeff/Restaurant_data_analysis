import pandas as pd
from convertdate import persian, gregorian

# Load the data from the Excel files
print("Loading data...")
rfaktors_df = pd.read_excel('RFaktors.xlsx')

# Display the loaded data for verification
print("Data loaded successfully.")
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

# Set the datetime as index
print("Setting datetime as index...")
rfaktors_df.set_index('Datetime', inplace=True)

# Identify the correct column name for the price
print("Identifying price column...")
price_column = 'Ghymatkoly'  # Example column name based on your output

# Calculate weekly sales per day
print("Calculating weekly sales per day...")
rfaktors_df['DayOfWeek'] = rfaktors_df.index.day_name()
weekly_sales_per_day = rfaktors_df.groupby('DayOfWeek').sum()[price_column]
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

# Calculate monthly sales in three parts based on Persian dates
print("Calculating monthly sales in three parts based on Persian dates...")
rfaktors_df['MonthPart'] = rfaktors_df['Tarikh'].apply(persian_month_parts)
monthly_sales_parts_persian = rfaktors_df.groupby(['Tarikh', 'MonthPart']).sum()[price_column]
print("Monthly Sales in Three Parts (Persian):\n", monthly_sales_parts_persian)

# Save the results to new Excel files
print("Saving results to Excel files...")
weekly_sales_per_day.to_excel('Weekly_Sales_Per_Day.xlsx')
monthly_sales_parts_persian.to_excel('Monthly_Sales_Parts_Persian.xlsx')

print("Analysis completed and results saved.")
