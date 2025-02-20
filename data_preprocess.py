from OmniDataService import get_omni_data as get
import os
import pandas as pd

def load_data():
    if os.path.exists('Unedited_set.csv'):
        # Load base dataset
        print(f"The file '{'Unedited_set.csv'}' exists. Loading DataFrame...")
        data = pd.read_csv('Unedited_set.csv')
        return data
    else:
        # Generate the data set used in the paper
        print(f"The file '{'Unedited_set.csv'}' does not exist. Generating DataFrame and saving csv...")
        data = get(res='high', rate='1min', year_range=(1964, 2024), file_name='Unedited_set.csv')
        return data

# Load or generate data
data = load_data()
print(data)