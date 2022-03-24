import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

path = '/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/train_1/'
path2 = '/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/'

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
#print(hits)


#data
z = hits['z']
hits['r'] = np.sqrt(hits['x']**2 + hits['y']**2)
r = hits['r']

#empty arrays to fill
r_arr7 = []
z_arr7 = []
r_arr8 = []
z_arr8 = []
r_arr9 = []
z_arr9 = []
r_arr12 = []
z_arr12 = []
r_arr13 = []
z_arr13 = []
r_arr14 = []
z_arr14 = []
r_arr16 = []
z_arr16 = []
r_arr17 = []
z_arr17 = []
r_arr18 = []
z_arr18 = []

#dividing up data to plot
for i in range(len(r)):
    if r[i] > 0 and r[i] < 200:
        if z[i] > -2000 and z[i] < -500:
            r_arr7.append(r[i])
            z_arr7.append(z[i])

        elif z[i] > -500 and z[i] < 500:
            r_arr8.append(r[i])
            z_arr8.append(z[i])
        
        elif z[i] > 500 and z[i] < 2000:
            r_arr9.append(r[i])
            z_arr9.append(z[i])

    if r[i] > 200 and r[i] < 700:
        if z[i] > -3000 and z[i] < -1200:
            r_arr12.append(r[i])
            z_arr12.append(z[i])

        elif z[i] > -1100 and z[i] < 1100:
            r_arr13.append(r[i])
            z_arr13.append(z[i])
        
        elif z[i] > 1200 and z[i] < 3000:
            r_arr14.append(r[i])
            z_arr14.append(z[i])

    if r[i] > 700 and r[i] < 2000:
        if z[i] > -3000 and z[i] < -1200:
            r_arr16.append(r[i])
            z_arr16.append(z[i])

        elif z[i] > -1100 and z[i] < 1100:
            r_arr17.append(r[i])
            z_arr17.append(z[i])
        
        elif z[i] > 1200 and z[i] < 3000:
            r_arr18.append(r[i])
            z_arr18.append(z[i])


#scatter plot for each layer, overlayed on one
fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(z_arr7,r_arr7,c='r',s=1.5,label='volume 7')
ax.scatter(z_arr8,r_arr8,c='darkorange',s=1.5,label='volume 8')
ax.scatter(z_arr9,r_arr9,c='y',s=1.5,label='volume 9')
ax.scatter(z_arr12,r_arr12,c='lime',s=1.5,label='volume 12')
ax.scatter(z_arr13,r_arr13,c='g',s=1.5,label='volume 13')
ax.scatter(z_arr14,r_arr14,c='c',s=1.5,label='volume 14')
ax.scatter(z_arr16,r_arr16,c='b',s=1.5,label='volume 16')
ax.scatter(z_arr17,r_arr17,c='m',s=1.5,label='volume 17')
ax.scatter(z_arr18,r_arr18,c='indigo',s=1.5,label='volume 18')
ax.legend(loc='lower right')
plt.title('Global Indexing Scheme of 10 Events')
plt.xlabel('z')
plt.ylabel('r')
plt.savefig(path2 + 'scheme_scatter.png')
plt.show()