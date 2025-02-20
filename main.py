"""
Best attempt on copying the results of the paper,
"Machine learning models for predicting geomagnetic
storms across five solar cycles using Dst index and heliospheric varaibles"
Daniel Boyd
"""

from Preprocessing_Tools import load_data
import matplotlib.pyplot as plt

data = load_data('processed_dat.csv', years=(1989,1994))


plt.plot(data.index, data['DST Index Min'])
plt.xlabel('Month')
plt.ylabel('DST Index')
plt.title('Time Series Plot of DST Index Min')
plt.show()

