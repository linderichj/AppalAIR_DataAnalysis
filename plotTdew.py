from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def plotTdew(dataset, outputFileOutlet, outputFileInside, outputFileSensor, plotFileName):
    # Load the RelativeHumidity datasets
    df_outlet = pd.read_csv(dataset + outputFileOutlet)  # Outlet NOAA dataset
    df_wet_neph = pd.read_csv(dataset + outputFileInside)  # Wet Neph NOAA dataset
    df_sensor = pd.read_csv(dataset + outputFileSensor)  # Sensor dataset

    # Ensure the Timestamp columns are in datetime format
    df_outlet['Timestamp'] = pd.to_datetime(df_outlet['Timestamp'])
    df_wet_neph['Timestamp'] = pd.to_datetime(df_wet_neph['Timestamp'])
    df_sensor['Timestamp'] = pd.to_datetime(df_sensor['Timestamp'])

    # Identify the common time range
    start_time = max(df_outlet['Timestamp'].min(), df_wet_neph['Timestamp'].min(), df_sensor['Timestamp'].min())
    end_time = datetime.strptime('2024-10-05 01:00:00', '%Y-%m-%d %H:%M:%S')  # min(df_outlet['Timestamp'].max(), df_wet_neph['Timestamp'].max(), df_sensor['Timestamp'].max())

    # Filter for the common time range in each DataFrame
    common_outlet = df_outlet[(df_outlet['Timestamp'] >= start_time) & (df_outlet['Timestamp'] <= end_time)]
    common_wet_neph = df_wet_neph[(df_wet_neph['Timestamp'] >= start_time) & (df_wet_neph['Timestamp'] <= end_time)]
    common_sensor = df_sensor[(df_sensor['Timestamp'] >= start_time) & (df_sensor['Timestamp'] <= end_time)]

    # Plot the dewpoint temperatures for the common area 
    plt.figure(figsize=(12, 6))

    # Plot Outlet NOAA dewpoint
    plt.plot(common_outlet['Timestamp'], common_outlet['DewPoint'], label='NOAA Outlet Dewpoint', color='blue')

    # Plot Wet Neph NOAA dewpoint
    plt.plot(common_wet_neph['Timestamp'], common_wet_neph['DewPoint'], label='NOAA Wet Neph Dewpoint', color='orange')

    # Plot Sensor dewpoint
    plt.plot(common_sensor['Timestamp'], common_sensor['DewPoint'], label='Inlet Sensor Dewpoint', color='green')

    # Formatting the plot
    plt.title('Dewpoint Temperature Comparison (Common Area)')
    plt.xlabel('Timestamp')
    plt.ylabel('Dewpoint Temperature (°C)')
    plt.xticks(rotation=45)

    # Set the x-axis limits to the common time range
    plt.xlim(start_time, end_time)

    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(dataset + plotFileName)
    plt.show()
