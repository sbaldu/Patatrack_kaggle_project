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
hit_arr = np.array(hits['global_index'])
print(hit_arr)

#plotting, no legend
z = hits['z']
hits['r'] = np.sqrt(hits['x']**2 + hits['y']**2)
r = hits['r']
print(np.unique(hits['global_index']))
#plt.figure()

#np_global_index = np.unique(hit_arr)
#print(np_global_index)

#layer1 = [2, ]

#for i in range(len(hit_arr)):
#    if hit_arr[i] == 2 or hit_arr[i] == 16


#scatter = plt.scatter(z,r,c=hits['global_index'],s=1,cmap="tab10")
plt.title('Global Indexing Scheme of 10 Events')
plt.xlabel('z')
plt.ylabel('r')
#np_global_index = np.unique(np.array(z))
#classes = [str(i) for i in np_global_index]
#print(len(scatter.legend_elements()[0]), len(np_global_index))
#plt.legend(handles = scatter.legend_elements()[0], labels = classes)
#plt.savefig(path2 + 'layertry1.png')
#plt.show() 

















##### ADDING LEGEND OF VOLUME IDS

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
"""
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
plt.show() """

















##### ADDING LEGEND OF LAYER IDS

r_v7_l2 = []
r_v7_l4 = []
r_v7_l6 = []
r_v7_l8 = []
r_v7_l10 = []
r_v7_l12 = []
r_v7_l14 = []
r_v8_l2 = []
r_v8_l4 = []
r_v8_l6 = []
r_v8_l8 = []
r_v9_l2 = []
r_v9_l4 = []
r_v9_l6 = []
r_v9_l8 = []
r_v9_l10 = []
r_v9_l12 = []
r_v9_l14 = []
r_v12_l2 = []
r_v12_l4 = []
r_v12_l6 = []
r_v12_l8 = []
r_v12_l10 = []
r_v12_l12 = []
r_v13_l2 = []
r_v13_l4 = []
r_v13_l6 = []
r_v13_l8 = []
r_v14_l2 = []
r_v14_l4 = []
r_v14_l6 = []
r_v14_l8 = []
r_v14_l10 = []
r_v14_l12 = []
r_v16_l2 = []
r_v16_l4 = []
r_v16_l6 = []
r_v16_l8 = []
r_v16_l10 = []
r_v16_l12 = []
r_v17_l2 = []
r_v17_l4 = []
r_v18_l2 = []
r_v18_l4 = []
r_v18_l6 = []
r_v18_l8 = []
r_v18_l10 = []
r_v18_l12 = []

z_v7_l2 = []
z_v7_l4 = []
z_v7_l6 = []
z_v7_l8 = []
z_v7_l10 = []
z_v7_l12 = []
z_v7_l14 = []
z_v8_l2 = []
z_v8_l4 = []
z_v8_l6 = []
z_v8_l8 = []
z_v9_l2 = []
z_v9_l4 = []
z_v9_l6 = []
z_v9_l8 = []
z_v9_l10 = []
z_v9_l12 = []
z_v9_l14 = []
z_v12_l2 = []
z_v12_l4 = []
z_v12_l6 = []
z_v12_l8 = []
z_v12_l10 = []
z_v12_l12 = []
z_v13_l2 = []
z_v13_l4 = []
z_v13_l6 = []
z_v13_l8 = []
z_v14_l2 = []
z_v14_l4 = []
z_v14_l6 = []
z_v14_l8 = []
z_v14_l10 = []
z_v14_l12 = []
z_v16_l2 = []
z_v16_l4 = []
z_v16_l6 = []
z_v16_l8 = []
z_v16_l10 = []
z_v16_l12 = []
z_v17_l2 = []
z_v17_l4 = []
z_v18_l2 = []
z_v18_l4 = []
z_v18_l6 = []
z_v18_l8 = []
z_v18_l10 = []
z_v18_l12 = []

"""
def appends(low_z, high_z, low_r, high_r, z_arr, r_arr):
    for i in range(len(r)):
        if r[i] > low_r and r[i] < high_r:
            if z[i] > low_z and z[i] < high_z:
                r_arr.append(r[i])
                z_arr.append(z[i]) #-597.5

                plt.figure()
                plt.scatter(z_arr,r_arr)
                plt.show()


appends(-1550,-1450,0,200,z_v7_l2,r_v7_l2)
appends(-1350,-1250,0,200,z_v7_l4,r_v7_l4)
appends(-1150,-1050,0,200,z_v7_l6,r_v7_l6)



appends(-1550,-1450,0,200,z_v7_l2,r_v7_l2)
appends(-1350,-1250,0,200,z_v7_l4,r_v7_l4)
appends(-1150,-1050,0,200,z_v7_l6,r_v7_l6)
plt.scatter(z_v7_l2,r_v7_l2,c='r')
plt.scatter(z_v7_l4,r_v7_l4,c='b')
plt.scatter(z_v7_l6,r_v7_l6,c='g')
plt.show()


        if z[i] > -1495 and z[i] < -1200:
            r_v7_l4.append(r[i])
            z_v7_l4.append(z[i])

        elif z[i] > -500 and z[i] < 500:
            r_arr8.append(r[i])
            z_arr8.append(z[i]) #max 71
        
        elif z[i] > 500 and z[i] < 2000:
            r_arr9.append(r[i])
            z_arr9.append(z[i]) #max 1502.7

    if r[i] > 200 and r[i] < 700:
        if z[i] > -3000 and z[i] < -1200:
            r_arr12.append(r[i])
            z_arr12.append(z[i]) #max -1215.5

        elif z[i] > -1100 and z[i] < 1100:
            r_arr13.append(r[i])
            z_arr13.append(z[i]) #max 1083.4
        
        elif z[i] > 1200 and z[i] < 3000:
            r_arr14.append(r[i])
            z_arr14.append(z[i]) #max 2954.5

    if r[i] > 700 and r[i] < 2000:
        if z[i] > -3000 and z[i] < -1200:
            r_arr16.append(r[i])
            z_arr16.append(z[i]) #max -1214.5

        elif z[i] > -1100 and z[i] < 1100:
            r_arr17.append(r[i])
            z_arr17.append(z[i]) #max 1078.6
        
        elif z[i] > 1200 and z[i] < 3000:
            r_arr18.append(r[i])
            z_arr18.append(z[i]) #max 2955.5"""
