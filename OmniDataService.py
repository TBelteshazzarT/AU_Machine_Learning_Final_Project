import urllib.request
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

"""
Package created by Daniel Boyd 2/12/2025
"""

"""URLs"""
# low res data sets
omni2_all_yrs_url = 'https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2_all_years.dat'
# high res data sets
# 5 min and 1 min
omni_5min_base = 'https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_5min'
omni_1min_base = 'https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_min'
# wayback machine base url (in case of server failure)
wayback_base = 'https://web.archive.org/web/20241231162911/'

# low res column lists
low_res_columns = ['Year', 'Decimal Day', 'Hour', 'Bartels rotation number', 'ID for IMF spacecraft',
             'ID for SW plasma spacecraft', '# of points in the IMF averages', '# of points in the plasma averages',
             'Field Magnitude Average |B|', 'Magnitude of Average Field Vector', 'Lat.Angle of Aver. Field Vector',
             'Long.Angle of Aver.Field Vector', 'Bx GSE, GSM', 'By GSE', 'Bz GSE', 'By GSM', 'Bz GSM', 'sigma|B|',
             'sigma B', 'sigma Bx', 'sigma By', 'sigma Bz', 'Proton temperature', 'Proton Density',
             'Plasma (Flow) speed', 'Plasma Flow Long. Angle', 'Plasma  Flow Lat. Angle', 'Na/Np', 'Flow Pressure',
             'sigma T', 'sigma N', 'sigma V', 'sigma phi V', 'sigma theta V', 'sigma-Na/Np', 'Electric field',
             'Plasma beta', 'Alfven mach number', 'Kp', 'R', 'DST Index', 'AE-index', 'Proton flux1',
             'Proton flux2', 'Proton flux4', 'Proton flux10', 'Proton flux30', 'Proton flux60', 'Flag(***)',
             'ap-index', 'f10.7_index', 'PC(N) index', 'AL-index, from Kyoto', 'AU-index, from Kyoto',
             'Magnetosonic mach number']

# high res column lists
high_res_5_columns = ['Year','Day', 'Hour', 'Minute', 'ID for IMF spacecraft', 'ID for SW Plasma spacecraft',
                    '# of points in IMF averages', '# of points in Plasma averages	I4', 'Percent interp',
                    'Timeshift, sec', 'RMS, Timeshift', 'RMS, Phase front normal', 'Time btwn observations, sec',
                    'Field magnitude average, nT', 'Bx, nT (GSE, GSM)', 'By, nT (GSE)', 'Bz, nT (GSE)', 'By, nT (GSM)',
                    'Bz, nT (GSM)', 'RMS SD B scalar, nT', 'RMS SD field vector, nT', 'Flow speed, km/s',
                    'Vx Velocity, km/s, GSE', 'Vy Velocity, km/s, GSE', 'Vz Velocity, km/s, GSE',
                    'Proton Density, n/cc',	'Temperature, K', 'Flow pressure, nPa', 'Electric field, mV/m',
                    'Plasma beta', 'Alfven mach number', 'X(s/c), GSE, Re', 'Y(s/c), GSE, Re', 'Z(s/c), GSE, Re',
                    'BSN location, Xgse, Re', 'BSN location, Ygse, Re', 'BSN location, Zgse, Re',
                    'AE-index, nT', 'AL-index, nT', 'AU-index, nT', 'SYM/D index, nT', 'SYM/H index, nT',
                    'ASY/D index, nT', 'ASY/H index, nT', 'PC(N) index', 'Magnetosonic mach number',
                    'Proton Flux >10 MeV, 1/(cm**2-sec-ster)', 'Proton Flux >30 MeV, 1/(cm**2-sec-ster)',
                    'Proton Flux >60 MeV, 1/(cm**2-sec-ster)']

high_res_min_columns = ['Year','Day', 'Hour', 'Minute', 'ID for IMF spacecraft', 'ID for SW Plasma spacecraft',
                    '# of points in IMF averages', '# of points in Plasma averages	I4', 'Percent interp',
                    'Timeshift, sec', 'RMS, Timeshift', 'RMS, Phase front normal', 'Time btwn observations, sec',
                    'Field magnitude average, nT', 'Bx, nT (GSE, GSM)', 'By, nT (GSE)', 'Bz, nT (GSE)', 'By, nT (GSM)',
                    'Bz, nT (GSM)', 'RMS SD B scalar, nT', 'RMS SD field vector, nT', 'Flow speed, km/s',
                    'Vx Velocity, km/s, GSE', 'Vy Velocity, km/s, GSE', 'Vz Velocity, km/s, GSE',
                    'Proton Density, n/cc',	'Temperature, K', 'Flow pressure, nPa', 'Electric field, mV/m',
                    'Plasma beta', 'Alfven mach number', 'X(s/c), GSE, Re', 'Y(s/c), GSE, Re', 'Z(s/c), GSE, Re',
                    'BSN location, Xgse, Re', 'BSN location, Ygse, Re', 'BSN location, Zgse, Re',
                    'AE-index, nT', 'AL-index, nT', 'AU-index, nT', 'SYM/D index, nT', 'SYM/H index, nT',
                    'ASY/D index, nT', 'ASY/H index, nT', 'PC(N) index', 'Magnetosonic mach number']

def read_dat_from_url(url):
    """Reads from a .dat file from a url and returns a string"""
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        return f"Error opening URL: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_omni_data(res='low', rate=None, year_range=(0, 0), file_name='OmniData.csv'):
    """
    Creates a pandas dataframe from the low-res or high-res omini datasets from nasa

    :param res: choose between high and low res.
    :param rate: for high-res indicate 5min or 1min sample rate. Leave blank for low-res.
    :param year_range: tuple containing first year to include and last year to include. For single year, enter the year
     as first and second item in tuple.
    :param file_name: str of the name of csv that is saved e.g.'OmniData.csv'
    :return: a pandas dataframe
    """
    if res == 'low':
        start_yr, end_yr = year_range
        if start_yr < 1963:
            start_yr = 1963
        if end_yr > 2025:
            end_yr = 2025
        years = list(range(start_yr, end_yr + 1))
        years_str = [str(x) for x in years]
        url_set = omni2_all_yrs_url
        column_name_set = low_res_columns
        dat_content = read_dat_from_url(url_set)
        if "Error" not in dat_content:
            # Process the data
            df = string_to_df(dat_content, column_name_set)
            df = df[df['Year'].isin(years_str)]
            return type_correct_and_save(df, file_name)
        else:
            print('Database not reached. Trying backup...')
            dat_content = read_dat_from_url((wayback_base + url_set))
            if "Error" not in dat_content:
                print('Backup successful')
                # Process the data
                df = string_to_df(dat_content, column_name_set)
                df = df[df['Year'].isin(years_str)]
                return type_correct_and_save(df, file_name)
            else:
                print(dat_content)

    elif res == 'high':
        start_yr, end_yr = year_range
        if start_yr < 1981:
            start_yr = 1981
        if end_yr > 2025:
            end_yr = 2025
        num_of_years = end_yr - start_yr
        column_name_set = high_res_5_columns
        if rate is None or '5min':
            url_base = omni_5min_base
        elif rate == '1min':
            url_base = omni_1min_base
        df = multi_url_read_to_df(num_of_years, url_base, start_yr, column_name_set)
        if "Error" not in df:
            return type_correct_and_save(df, file_name)
        else:
            print('Database not reached. Trying backup...')
            df = multi_url_read_to_df(num_of_years, (wayback_base + url_base), start_yr, column_name_set)
            if "Error" not in df:
                print('Backup successful')
                return type_correct_and_save(df, file_name)
            else:
                return None

def multi_url_read_to_df(iterations, base_url, start_val, col_names):
    """
    Creates a pandas dataframe from an input string and a list of column names

    :param iterations: number of iterations to make.
    :param base_url: str of the target url.
    :param start_val: starting number of the data set.
    :param col_names: list of column names.
    :return: a pandas dataframe of the given data
    """
    error = "Error url not reached"
    df_combined = pd.DataFrame()
    for i in range(iterations + 1):
        url_set = base_url + str(start_val + i) + '.asc'
        dat_content = read_dat_from_url(url_set)
        if "Error" not in dat_content:
            df1 = string_to_df(dat_content, col_names)
            df_combined = pd.concat([df_combined, df1], ignore_index=True)
        else:
            print(dat_content)
    if "Empty DataFrame" in str(df_combined):
        return error
    else:
        return df_combined

def string_to_df(data, column_names):
    """
    Creates a pandas dataframe from an input string and a list of column names

    :param data: a string from a data file.
    :param column_names: List of strings to be used as the column names.
    :return: a pandas dataframe of the given data
    """
    # split the string into words
    itemized_entries = data.split()
    # create a list of dictionaries
    list_of_dictionaries = create_list_of_dicts_with_keys(itemized_entries, column_names, chunk_size=len(column_names))
    # return dataframe
    return pd.DataFrame(list_of_dictionaries)

def create_list_of_dicts_with_keys(words, key_names, chunk_size=55):
    """
    Creates a list of dictionaries from a list of words, where each dictionary contains
    a chunk of words (default chunk size is 55). The keys of the dictionaries are renamed
    based on the provided list of key names.

    :param words: List of strings (words).
    :param key_names: List of strings to be used as keys in the dictionaries.
    :param chunk_size: Size of each chunk (default is 55).
    :return: List of dictionaries, where each dictionary contains a chunk of words with renamed keys.
    """
    list_of_dicts = []
    for i in range(0, len(words), chunk_size):
        # Create a dictionary for the current chunk using the provided key names
        chunk_dict = {}
        for j, key in enumerate(key_names):
            if i + j < len(words):
                chunk_dict[key] = words[i + j]
        list_of_dicts.append(chunk_dict)
    return list_of_dicts

def type_correct_and_save(df, name):
    """
     Creates new DataFrame with pandas auto type detection, as well as creates a csv of the DataFrame.

     :param df: pandas DataFrame.
     :param name: str of the filename e.g. 'OmniData.csv'
     """
    df.to_csv(str(name), index=False)
    return pd.read_csv(str(name))
