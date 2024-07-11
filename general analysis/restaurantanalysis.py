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
merged_df = pd.merge(rfakitm_df, rfaktors_df, on='FID')
merged_df = pd.merge(merged_df, rsfaresh_df, on='KID')

print("Data merged successfully.")
print(merged_df.columns)  # Check the columns to identify any renaming or conflicts
print(merged_df.head())

# Identify the correct column name for the price
print("Identifying price column...")
price_column = 'ghymat_x' if 'ghymat_x' in merged_df.columns else 'ghymat_y'
print(f"Using price column: {price_column}")

# Set the datetime as index
print("Setting datetime as index...")
merged_df.set_index('Datetime', inplace=True)

# Calculate sales on a weekly, monthly, and seasonal basis
print("Calculating weekly sales...")
weekly_sales = merged_df.resample('W').sum()[price_column]

print("Calculating monthly sales...")
monthly_sales = merged_df.resample('M').sum()[price_column]

print("Calculating seasonal sales...")
seasonal_sales = merged_df.resample('Q').sum()[price_column]

# Print the results
print("Weekly Sales:\n", weekly_sales)
print("\nMonthly Sales:\n", monthly_sales)
print("\nSeasonal Sales:\n", seasonal_sales)

# Save the results to new Excel files
print("Saving results to Excel files...")
weekly_sales.to_excel('Weekly_Sales.xlsx')
monthly_sales.to_excel('Monthly_Sales.xlsx')
seasonal_sales.to_excel('Seasonal_Sales.xlsx')

print("Analysis completed and results saved.")
