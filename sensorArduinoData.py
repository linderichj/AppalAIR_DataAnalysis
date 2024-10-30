import pandas as pd
from datetime import datetime, timedelta
import math

# Calibration parameters (slope, intercept)
slope = 0.99384  # Example value for slope
intercept = 0.736  # Example value for intercept

# Time correction factor 
TIME_CORRECTION = 1.00000


## Functions

# Function to calculate calibrated RH values
def calibrate_rh(rh_measured, slope, intercept, quadratic_term=0):
     # Extendable to quadratic calibration if needed
    calibrated_value = intercept + rh_measured * slope + quadratic_term * (rh_measured ** 2)
    return round(calibrated_value, 2)  # Round to 2 decimal places

# Function to convert time (hh:mm:ss) to decimal day format
def time_to_decimal_day(time_str, day):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    day_fraction = total_seconds / 86400  # 86400 seconds in a day
    return round(day + day_fraction, 8)  # Rounded to 6 decimals for precision

# Function to convert decimal day to time format
def decimal_day_to_time(decimal_day):
    # Extract the day fraction
    day_fraction = decimal_day - int(decimal_day)
    
    # Calculate total seconds from the day fraction
    total_seconds = day_fraction * 86400  # 86400 seconds in a day
    
    # Convert total seconds to hours, minutes, and seconds
    day = int(decimal_day)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    return day, hours, minutes, seconds

# Function to add startTime + read in time
def add_time_with_array(time_array1, start_time):
    # Extract the day, hour, minute, second from the array
    day = time_array1[0]
    hour, minute, second = time_array1[1], time_array1[2], time_array1[3] 

    # Create a timedelta object for the day and time
    day_delta = timedelta(days=day)
    time_delta = timedelta(hours=hour, minutes=minute, seconds=second)
    
    # Add day and time deltas to the start_time
    final_time = start_time + day_delta + time_delta
    return final_time

# Initialize an empty two-dimensional array
time_array = []

# Function to add a new time entry
def add_time_entry(year, month, day, hour, minute, second):
    time_array.append([year, month, day, hour, minute, second])


# Function to extract start time from the filename
def extract_start_time(filename):
    # Remove the 'UTC_LogRhExhaust.csv' part and extract the date and time part
    datetime_str = filename.split('_')[0] + filename.split('_')[1][:6]
    
    # Parse the extracted string into a datetime object
    start_time = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')
    return start_time

def dataPreProcessSensor(dataset, input_file_name, output_file_name): 

    # Extract start time from the filename
    start_time = extract_start_time(input_file_name)
    # print("Start Time:", start_time)

    input_file_path = dataset + input_file_name
    output_file_path = dataset + output_file_name

    df = pd.read_csv(input_file_path)


    # Specify headers (Time, RH_measured, Temperature) since the file lacks them
    headers = ["Time", "RH_measured", "Temperature", "T_dewpoint"]
    df = pd.read_csv(input_file_path, names=headers)

    # Initialize the day counter starting from 0
    day_counter = 0
    decimal_times = []

    # Convert 'Time' column to string (if not already)
    df['Time'] = df['Time'].astype(str)

    # Loop through the 'Time' column to increment the day when '00:00:00' is encountered
    for time in df['Time']:
        if time == '00:00:00':
            day_counter += 1
        decimal_times.append(time_to_decimal_day(time, day_counter))

    # Add the 'Decimal_Day' column to the DataFrame
    df['Decimal_Day'] = decimal_times

    # Calculate corrected time
    corr_decimal_times = []

    decimal_time_start = df['Decimal_Day'].iloc[0]
    decimal_time_stop = df['Decimal_Day'].iloc[-1]

    for decimal_times in df['Decimal_Day']: 
        corr_decimal_times.append((decimal_times - decimal_time_start) / TIME_CORRECTION + decimal_time_start)
        [d, h, m, s] = decimal_day_to_time((decimal_times - decimal_time_start) / TIME_CORRECTION + decimal_time_start)
        time_array.append([d, h, m, s])

    # Add the 'Corr_Decimal_Day' column to the DataFrame
    df['Corr_Decimal_Day'] = corr_decimal_times
    df['dhms'] = time_array

    timeStemp = []


    for time_array1 in time_array:
        # Call the function to add start_time and day counter to the time
        timeStempValue = add_time_with_array(time_array1, start_time)
        timeStemp.append(timeStempValue)
    df['timeStemp'] = timeStemp


    # Apply the calibration function to add the 'RH_calibrated' column
    df['RH_calibrated'] = df['RH_measured'].apply(lambda x: calibrate_rh(x, slope, intercept))

    # Store the DataFrame to a new CSV file with headers
    try:
        tempFilePath = dataset + 'temp/' + 'calibrated_rh_data.csv'  # Replace with desired output path
        df.to_csv(tempFilePath, index=False)
    except:
        print('No temp folder')
    else: 
        tempFilePath = dataset + 'calibrated_rh_data.csv'  # Replace with desired output path
        df.to_csv(tempFilePath, index=False)


    # Initialize an empty list to store the 'Minute' values
    minute_list = []

    # Loop through each 'timeStemp' and calculate 'total_min' for each row
    for ts in df['timeStemp']:  # Make sure 'timeStemp' is a column in df
        dT = ts - start_time
        total_min = int(dT.total_seconds() / 60)  # Calculate minutes since start_time
        minute_list.append(total_min)  # Append each total_min to the list

    # Assign the calculated minutes list to the 'Minute' column in the DataFrame
    df['Minute'] = minute_list

    # Group by the 'Minute' column and calculate the mean for relevant columns
    df_grouped = df.groupby('Minute').agg({
        'timeStemp': 'mean',                # Average of corrected decimal days
        'Temperature': 'mean',              # Average of temperature measurements
        'RH_calibrated': 'mean',            # Averaging RH_calibrated 
        'T_dewpoint': 'mean'                # Average dewpoint temperature
    }).reset_index()

    # Round the aggregated values to the desired number of decimal places (e.g., 2 decimal places)
    df_grouped = df_grouped.round({'Temperature': 2, 'RH_calibrated': 2, 'T_dewpoint': 2})

    # Set seconds and microseconds to 0 in the 'timeStemp' column (fully remove microseconds)
    df_grouped['timeStemp'] = df_grouped['timeStemp'].apply(lambda x: x.replace(second=0, microsecond=0))

    # Convert to string format without microseconds and then back to datetime
    df_grouped['timeStemp'] = pd.to_datetime(df_grouped['timeStemp'].dt.strftime('%Y-%m-%d %H:%M:%S'))

    # Remove the first column (if it's the index or any unwanted column)
    df_grouped.drop(df_grouped.columns[0], axis=1, inplace=True)  # Use this line to drop the first column

    #  Rename columns directly
    df_grouped.columns = ['Timestamp', 'Temperature', 'RelativeHumidity', 'DewPoint']

    # Save the reduced dataset to a new CSV file
    df_grouped.to_csv(output_file_path, index=False)

    print("Data has been processed and saved to:", output_file_path)



# # Modify to read in the file from a CSV
# dataset = 'DataSet2/'
# input_file_name = '20241004_160009UTC_WN_Inlet.csv'  # Replace with your file path
# outputFileSensor = 'reducedSensor.csv'

# dataPreProcessSensor(dataset, input_file_name, outputFileSensor)