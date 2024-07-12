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

# Merge the data based on FID from rfakitm and rfaktors
print("Merging data...")
merged_df = pd.merge(rfakitm_df, rfaktors_df, on='FID', suffixes=('_item', '_factor'))

# Then merge with rsfaresh_df based on KID
merged_df = pd.merge(merged_df, rsfaresh_df, on='KID', suffixes=('', '_order'))

print("Data merged successfully.")
print(merged_df.columns)  # Check the columns to identify any renaming or conflicts
print(merged_df.head())

# Save the merged data to a new Excel file
print("Saving merged data to Excel file...")
merged_df.to_excel('Merged_Rfaktors_Rfakitm.xlsx', index=False)

print("Merged data saved successfully.")
