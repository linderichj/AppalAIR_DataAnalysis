import math
import pandas as pd


def calculate_dew_point(T, RH):
    """
    Calculate the dew point temperature given temperature and relative humidity.
    
    :param T: Temperature in Celsius
    :param RH: Relative Humidity in percentage (0-100%)
    :return: Dew point in Celsius
    """
    # Constants for the Magnus formula
    A = 17.27
    B = 237.7
    
    # Calculate the intermediate value alpha
    alpha = ((A * T) / (B + T)) + math.log(RH / 100.0)
    
    # Calculate the dew point using Magnus formula
    dew_point = (B * alpha) / (A - alpha)
    
    return dew_point

# # Example usage
# temperature = float(input("Enter the temperature in Celsius: "))
# relative_humidity = float(input("Enter the relative humidity in percentage: "))

# dew_point = calculate_dew_point(temperature, relative_humidity)
# print(f"The dew point is: {dew_point:.2f} °C")


def calculate_relative_humidity(T, T_dew):
    """
    Calculate relative humidity given the actual temperature and dew point temperature.
    
    :param T: Actual temperature in Celsius
    :param T_dew: Dew point temperature in Celsius
    :return: Relative humidity in percentage
    """
    # Constants for the Magnus formula
    A = 17.27
    B = 237.7
    
    # Magnus formula for relative humidity
    alpha_actual = (A * T) / (B + T)
    alpha_dew = (A * T_dew) / (B + T_dew)
    
    # Calculate RH from the dew point
    RH = 100 * math.exp(alpha_dew - alpha_actual)
    
    return RH

# Example usage
# actual_temperature = float(input("Enter the actual temperature in Celsius: "))
# dew_point_temperature = float(input("Enter the dew point temperature in Celsius: "))

# relative_humidity = calculate_relative_humidity(actual_temperature, dew_point_temperature)
# print(f"The relative humidity is: {relative_humidity:.2f}%")


def calcInsideTdew(dataset, outputFileInside, outputFileOutlet, label):
    # Combine dataset path with filenames for inside and outlet
    file_path_inside = dataset + outputFileInside
    file_path_outlet = dataset + outputFileOutlet
    
    # Read the CSV files for both inside and outlet data
    df_inside = pd.read_csv(file_path_inside)
    df_outlet = pd.read_csv(file_path_outlet)

    # Assuming the files are in the format: Timestamp, Temperature, RelativeHumidity, DewPoint
    # Use the DewPoint from outlet and Temperature from inside for calculation
    df_inside[label] = df_inside.apply(
    lambda row: calculate_relative_humidity(row['Temperature'], df_outlet.loc[df_outlet['Timestamp'] == row['Timestamp'], 'DewPoint'].values[0])
    if pd.notnull(row['Temperature']) and len(df_outlet.loc[df_outlet['Timestamp'] == row['Timestamp'], 'DewPoint'].values) > 0
    else None, axis=1
    )

    # Save the updated inside data with the new 'RH_dewpointBased' column
    df_inside.to_csv(file_path_inside, index=False)

    print(f"File {file_path_inside} updated with RH_dewpointBased column.")

# calcInsideTdew('DataSet2/', )