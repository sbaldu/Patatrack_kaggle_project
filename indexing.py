import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

path = '/Users/pfudolig/patatrack/trackml-library-master/trackml/train_1/'

#global dataframe of everything
def read_in(filepath,count,type):
    """Given filepath, read in count-amount of each type of file and return one
    concatenated dataframe"""
    i=0
    pathlist = Path(filepath).rglob('*' + type + '.csv')
    df = None
    for filepath in pathlist:
        path_in_str = str(filepath)
        i += 1
        toadd = pd.read_csv(path_in_str)
        if df is None: 
            df = toadd
        else:
            df.append(toadd)
        if i == count:
            break
    return(df)

truth = read_in(path, 10, 'truth')
hits = read_in(path, 10, 'hits')

#Set maxima
maxLayerId = hits['layer_id'].max()
maxVolId = hits['volume_id'].max()

#Add new column of global index
hits['global_index'] = (hits['volume_id']-7) * (maxLayerId+1) + (hits['layer_id'])
hits.sort_values('global_index')

#plotting
z = hits['z']
hits['r'] = np.sqrt(hits['x']**2 + hits['y']**2)
r = hits['r']
plt.figure()
plt.scatter(z,r,c=hits['global_index'],s=1,cmap="rainbow")
plt.title('Global Indexing Scheme of 10 Events')
plt.xlabel('z')
plt.ylabel('r')
plt.savefig('/Users/pfudolig/patatrack/trackml-library-master/trackml/globalindex.png')
plt.show()