from OmniDataService import get_omni_data as get
import pandas as pd

# Generate the data set used in the paper
data = get(res='high', rate='1min', year_range=(1964, 2024), file_name='Unedited_set.csv')
print(data)

