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

# Set the datetime as index
rfaktors_df.set_index('Datetime', inplace=True)

# Merge the data based on FID from rfakitm and rfaktors
print("Merging data...")
merged_df = pd.merge(rfakitm_df, rfaktors_df.reset_index(), on='FID', suffixes=('_item', '_factor'))

# Then merge with rsfaresh_df based on KID
merged_df = pd.merge(merged_df, rsfaresh_df, on='KID', suffixes=('', '_order'))

print("Data merged successfully.")
print(merged_df.columns)  # Check the columns to identify any renaming or conflicts
print(merged_df.head())

# Identify the correct column name for the price
print("Identifying price column...")
price_column = 'ghymat_item' if 'ghymat_item' in merged_df.columns else 'ghymat'
print(f"Using price column: {price_column}")

# Add columns for day of the week and categorize sales as before or after 6pm
print("Categorizing sales by day of week and time of day...")
merged_df['DayOfWeek'] = merged_df['Datetime'].dt.day_name()
merged_df['TimeOfDay'] = ['Before 6pm' if hour < 18 else 'After 6pm' for hour in merged_df['Datetime'].dt.hour]

# Group by item, day of week, and time of day, then sum the prices
print("Calculating total prices for each item by day of week and time of day...")
total_price_per_item_day_time = merged_df.groupby(['Esm', 'DayOfWeek', 'TimeOfDay'])[price_column].sum().unstack().fillna(0)

print("Total price per item by day of week and time of day:\n", total_price_per_item_day_time)

# Save the results to a new Excel file
print("Saving results to Excel files...")
total_price_per_item_day_time.to_excel('Total_Price_Per_Item_Day_Time.xlsx')

print("Analysis completed and results saved.")
