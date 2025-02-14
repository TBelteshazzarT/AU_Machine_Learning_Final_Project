"""
Example of how to use the OmniDataService tool to create a dataset.
Please do not delete this file so others can use it to get started.\
Thank you,
Daniel Boyd
"""

from OmniDataService import get_omni_data as get
import pandas as pd

# rate is optional if you are using low-res. year_range will default to all values if not indicated
# creates as csv of the DataFrame that is loaded into the variable 'data'
data = get(res='high', rate='1min', year_range=(2010, 2010), file_name='high.csv')
print(data)

