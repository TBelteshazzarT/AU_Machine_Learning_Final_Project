"""
Best attempt on copying the results of the paper,
"Machine learning models for predicting geomagnetic
storms across five solar cycles using Dst index and heliospheric varaibles"
Daniel Boyd
"""

import pandas as pd
from datetime import datetime, timedelta
import os
from OmniDataService import get_omni_data as get

def load_data(name='data.csv', years=(0,2025)):
    """Loads the indicated dataset. If it can't be found it generates it new."""
    if os.path.exists(name):
        # Load base dataset
        print(f"The file '{name}' exists. Loading DataFrame...")
        data = pd.read_csv(name)
        return data
    else:
        # Generate the data set used in the paper
        print(f"The file '{name}' does not exist. Generating DataFrame and saving csv...")
        data = create_dataset(name=name, years=years)
        return data

def create_dataset(name='data.csv', years=(0,2025)):
    """Creates a data set from the Omni low-res data that is resampled to daily and then averaged over 30day intervals"""
    # creates as csv of the DataFrame that is loaded into the variable 'data'
    start, end = years
    data = get(res='low', year_range=(start, end), flag_replace=True,  file_name=name)
    print(data.head())

    # trim data to desired fields
    filtered_data = data[['Year', 'Decimal Day', 'Hour', 'Field Magnitude Average |B|', 'Proton temperature',
                          'Proton Density', 'Plasma (Flow) speed', 'Na/Np', 'Flow Pressure', 'Kp', 'R',
                          'DST Index', 'f10.7_index', 'Bz GSE']]

    # resample the data on hour 0
    resampled_data = filtered_data[filtered_data['Hour'].isin([0])]
    resampled_data.to_csv('resampled.csv', index=False)
    # drop hourly data
    data = data.drop('Hour', axis=1)

    # convert dataset to datetime-index
    data_conv = convert_to_datetime_index(data)

    # split out dst index to find minimum
    dst_data = data_conv[['DST Index']]
    data_conv.drop(columns=['DST Index'], inplace=True)

    # find minimum dst values
    dst_data = find_min_over_30_day_intervals(dst_data)

    # find averages of the rest of the values
    data_averaged = average_over_30_day_intervals(data_conv)

    # add min dst back to the dataframe
    data_merge = pd.concat([data_averaged, dst_data['DST Index'].rename("DST Index Min")], axis=1)
    data_merge.to_csv(name, index=True)
    return data_merge

def average_over_30_day_intervals(df):
    """
    Averages all the values in each column of the DataFrame over 30-day intervals.

    Parameters:
    df (pd.DataFrame): Input DataFrame with a DateTime index and daily values.

    Returns:
    pd.DataFrame: A new DataFrame with the averaged values over 30-day intervals.
    """

    # Ensure the DataFrame has a DateTime index
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("The DataFrame must have a DateTime index.")

    # Resample the data by 30-day intervals and calculate the mean
    resampled_df = df.resample('30D').mean()

    return resampled_df


def convert_to_datetime_index(df):
    """
    Converts a DataFrame with 'Year' and 'Decimal Day' columns into a DataFrame with a datetime index.

    Parameters:
    df (pd.DataFrame): Input DataFrame with 'Year' and 'Decimal Day' columns.

    Returns:
    pd.DataFrame: A new DataFrame with a datetime index.
    """

    # Ensure the required columns exist
    if 'Year' not in df.columns or 'Decimal Day' not in df.columns:
        raise ValueError("The DataFrame must contain 'Year' and 'Decimal Day' columns.")

    # Create a datetime index
    datetime_index = []
    for year, decimal_day in zip(df['Year'], df['Decimal Day']):
        # Calculate the integer day of the year and the fractional part
        day_of_year = int(decimal_day)
        fractional_day = decimal_day - day_of_year

        # Create a datetime object for the start of the year
        start_of_year = datetime(year=year, month=1, day=1)

        # Add the days and fractional days to the start of the year
        dt = start_of_year + timedelta(days=day_of_year - 1, seconds=int(fractional_day * 86400))
        datetime_index.append(dt)

    # Create a new DataFrame with the datetime index
    df_with_datetime = df.copy()
    df_with_datetime.index = pd.to_datetime(datetime_index)

    # Drop the 'Year' and 'Decimal Day' columns as they are no longer needed
    df_with_datetime = df_with_datetime.drop(columns=['Year', 'Decimal Day'])

    return df_with_datetime


def find_min_over_30_day_intervals(df):
    """
    Finds the minimum of all the values in each column of the DataFrame over 30-day intervals.

    Parameters:
    df (pd.DataFrame): Input DataFrame with a DateTime index and daily values.

    Returns:
    pd.DataFrame: A new DataFrame with the minimum values over 30-day intervals.
    """

    # Ensure the DataFrame has a DateTime index
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("The DataFrame must have a DateTime index.")

    # Resample the data by 30-day intervals and calculate the minimum
    resampled_df = df.resample('30D').min()

    return resampled_df