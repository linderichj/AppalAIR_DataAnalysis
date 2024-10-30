from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def plotRh(dataset, outputFileOutlet, outputFileInside, outputFileSensor, plotFileName):
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

    # Plot the RelativeHumidity temperatures for the common area
    plt.figure(figsize=(12, 6))

    # Plot Outlet NOAA RelativeHumidity
    plt.plot(common_outlet['Timestamp'], common_outlet['RelativeHumidity'], label='NOAA Outlet RH', color='blue')

    # Plot Wet Neph NOAA RelativeHumidity
    plt.plot(common_wet_neph['Timestamp'], common_wet_neph['RelativeHumidity'], label='NOAA Wet Neph RH', color='orange')
    plt.plot(common_wet_neph['Timestamp'], common_wet_neph['RH_dewpointOutlet'], label='Inside dewpointbased outlet RH', color='red')
    plt.plot(common_wet_neph['Timestamp'], common_wet_neph['RH_dewpointInlet'], label='Inside dewpointbased inlet RH', color='purple')

    # Plot Sensor RelativeHumidity
    plt.plot(common_sensor['Timestamp'], common_sensor['RelativeHumidity'], label='Inlet Sensor RH', color='green')

    # Formatting the plot
    plt.title('RelativeHumidity Comparison')
    plt.xlabel('Timestamp')
    plt.ylabel('RelativeHumidity (%)')
    plt.xticks(rotation=45)

    # Set the x-axis limits to the common time range
    plt.xlim(start_time, end_time)

    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(dataset + plotFileName)
    plt.show()
