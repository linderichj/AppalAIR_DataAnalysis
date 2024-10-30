import pandas as pd

def dataPreProcessInside(dataset, input_file_name, outputFileInside): 

    input_file_path = dataset + input_file_name
    output_file_path = dataset + outputFileInside

    df = pd.read_csv(input_file_path, delimiter=',', skiprows=1)  # Skip the first row for the header

    # Convert the 'DateTimeUTC' column to datetime format
    df['DateTimeUTC'] = pd.to_datetime(df['DateTimeUTC'], format='%Y-%m-%d %H:%M:00')

    # Filter out the relevant columns
    output_df = df[['DateTimeUTC', 'T_S12', 'U_S12']].copy()  # Use .copy() to avoid the warning

    # Calculate dew point using T_S12 for temperature and U_S12 for relative humidity
    output_df.loc[:, 'DewPoint'] = output_df.apply(
        lambda row: row['T_S12'] - (100 - row['U_S12']) / 5 if row['U_S12'] is not None and row['U_S12'] > 0 else None, axis=1
    )

    # Rename columns to match your desired output format
    output_df.columns = ['DateTimeUTC', 'T_S12', 'U_S12', 'DewPoint']

    output_df = output_df.round({'T_S12': 2, 'U_S12': 2, 'DewPoint': 2})

    # Rename columns directly
    output_df.columns = ['Timestamp', 'Temperature', 'RelativeHumidity', 'DewPoint']

    # Save the new dataset to a CSV file
    output_df.to_csv(output_file_path, index=False)

    print("Data has been extracted and saved to:", output_file_path)


# Load the dataset
# dataset = 'DataSet2/'                   # Dataset 
# input_file_name = 'app_20241004.csv'  # Replace with the path to your input file
# output_file_name = 'reducedInside2.csv'

# dataPreProcessInside(dataset, input_file_name, output_file_name) 
