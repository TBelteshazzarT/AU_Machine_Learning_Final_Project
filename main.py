"""
Best attempt on copying the results of the paper,
"Machine learning models for predicting geomagnetic
storms across five solar cycles using Dst index and heliospheric varaibles"
Daniel Boyd
"""

from Preprocessing_Tools import load_data

data = load_data('processed_dat.csv', years=(2024,2024))
print(list(data))
print(data)

