import pandas as pd


def dataPreProcessOutlet(dataset, input_file_name, output_file_name):
    
    input_file_path = dataset + input_file_name
    output_file_path = dataset + output_file_name

    df = pd.read_csv(input_file_path, delimiter=',', skiprows=1)  # Skip the first row for the header

    # Convert the 'DateTimeUTC' column to datetime format
    df['DateTimeUTC'] = pd.to_datetime(df['DateTimeUTC'], format='%Y-%m-%d %H:%M:00')

    # Filter out the relevant columns
    output_df = df[['DateTimeUTC', 'T_V12', 'U_V12']].copy()  # Use .copy() to avoid the warning

    # Calculate dew point using T_V12 for temperature and U_V12 for relative humidity
    output_df.loc[:, 'DewPoint'] = output_df.apply(
        lambda row: row['T_V12'] - (100 - row['U_V12']) / 5 if row['U_V12'] is not None and row['U_V12'] > 0 else None, axis=1
    )

    # Rename columns to match your desired output format
    output_df.columns = ['DateTimeUTC', 'T_V12', 'U_V12', 'DewPoint']

    output_df = output_df.round({'T_V12': 2, 'U_V12': 2, 'DewPoint': 2})

    # Rename columns directly
    output_df.columns = ['Timestamp', 'Temperature', 'RelativeHumidity', 'DewPoint']

    # Save the new dataset to a CSV file
    output_df.to_csv(output_file_path, index=False)

    print("Data has been extracted and saved to:", output_file_path)


# # Load the dataset
# dataset = 'DataSet2/'                   # Dataset 
# input_file_name = 'app_20241004.csv'    # Replace with the path to your input file
# output_file_name = 'reducedOutlet2.csv'


# dataPreProcessOutlet(dataset, input_file_name, output_file_name)  
