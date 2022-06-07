"""want to make a new global index column of manually input indices so we can plot legend by layer"""
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
z = hits['z']
hits['r'] = np.sqrt(hits['x']**2 + hits['y']**2)
r = hits['r']
hits['global_index'] = z + r

#Set maxima
maxLayerId = hits['layer_id'].max()
maxVolId = hits['volume_id'].max()

#manually input indices per volid,layerid pair
globalIndex = {}
globalIndex[(7,2)] = 0 #2
globalIndex[(7,4)] = 1 #4
globalIndex[(7,6)] = 2 #6
globalIndex[(7,8)] = 3 #8
globalIndex[(7,10)] = 4 #10
globalIndex[(7,12)] = 5 #12
globalIndex[(7,14)] = 6
globalIndex[(8,2)] = 7
globalIndex[(8,4)] = 8
globalIndex[(8,6)] = 9
globalIndex[(8,8)] = 10
globalIndex[(9,2)] = 11
globalIndex[(9,4)] = 12
globalIndex[(9,6)] = 13
globalIndex[(9,8)] = 14
globalIndex[(9,10)] = 15
globalIndex[(9,12)] = 16
globalIndex[(9,14)] = 17
globalIndex[(12,2)] = 18
globalIndex[(12,4)] = 19
globalIndex[(12,6)] = 20
globalIndex[(12,8)] = 21
globalIndex[(12,10)] = 22
globalIndex[(12,12)] = 23
globalIndex[(13,2)] = 24
globalIndex[(13,4)] = 25
globalIndex[(13,6)] = 26
globalIndex[(13,8)] = 27
globalIndex[(14,2)] = 28
globalIndex[(14,4)] = 29
globalIndex[(14,6)] = 30
globalIndex[(14,8)] = 31
globalIndex[(14,10)] = 32
globalIndex[(14,12)] = 33
globalIndex[(16,2)] = 34
globalIndex[(16,4)] = 35
globalIndex[(16,6)] = 36
globalIndex[(16,8)] = 37
globalIndex[(16,10)] = 38
globalIndex[(16,12)] = 39
globalIndex[(17,2)] = 40
globalIndex[(17,4)] = 41
globalIndex[(18,2)] = 42
globalIndex[(18,4)] = 43
globalIndex[(18,6)] = 44
globalIndex[(18,8)] = 45
globalIndex[(18,10)] = 46
globalIndex[(18,12)] = 47

vols = hits['volume_id']
lays = hits['layer_id']

#empty arrays
z_layer2 = []
r_layer2 = []
z_layer4 = []
r_layer4 = []
z_layer6 = []
r_layer6 = []
z_layer8 = []
r_layer8 = []
z_layer10 = []
r_layer10 = []
z_layer12 = []
r_layer12 = []
z_layer14 = []
r_layer14 = []

#for each layer, appends z and r data to arrays to plot separately
def add_col(globalIndex,hits):
    #actually might not even need this but good to have
    for i in range(hits.shape[0]): #create a new column for manually inputted global indices
        key = (hits.iloc[i, 4], hits.iloc[i, 5])
        hits.iloc[i,8] = globalIndex[key]

    for i in range(len(hits['layer_id'])):
        if i == 2:
            l2 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 2].copy()))
            z_layer2.append(l2.iloc[:,3])
            r_layer2.append(l2.iloc[:,7])

    for i in range(len(hits['layer_id'])):
        if i == 4:
            l4 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 4].copy()))
            z_layer4.append(l4.iloc[:,3])
            r_layer4.append(l4.iloc[:,7])

    for i in range(len(hits['layer_id'])):
        if i == 6:
            l6 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 6].copy()))
            z_layer6.append(l6.iloc[:,3])
            r_layer6.append(l6.iloc[:,7])

    for i in range(len(hits['layer_id'])):
        if i == 8:
            l8 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 8].copy()))
            z_layer8.append(l8.iloc[:,3])
            r_layer8.append(l8.iloc[:,7])

    for i in range(len(hits['layer_id'])):
        if i == 10:
            l10 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 10].copy()))
            z_layer10.append(l10.iloc[:,3])
            r_layer10.append(l10.iloc[:,7])

    for i in range(len(hits['layer_id'])):
        if i == 12:
            l12 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 12].copy()))
            z_layer12.append(l12.iloc[:,3])
            r_layer12.append(l12.iloc[:,7])

    for i in range(len(hits['layer_id'])):
        if i == 14:
            l14 = pd.DataFrame(data = (hits.loc[hits['layer_id'] == 14].copy()))
            z_layer14.append(l14.iloc[:,3])
            r_layer14.append(l14.iloc[:,7])

            
add_col(globalIndex, hits)
#print(hits['layer_id'] == 14)

#plotting
fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(z_layer2,r_layer2,c = 'r', s=1.5,label='layer 2s')
ax.scatter(z_layer4,r_layer4,c='darkorange',s=1.5,label='layer 4s')
ax.scatter(z_layer6,r_layer6,c='y',s=1.5,label='layer 6s')
ax.scatter(z_layer8,r_layer8,c='g',s=1.5,label='layer 8s')
ax.scatter(z_layer10,r_layer10,c='c',s=1.5,label='layer 10s')
ax.scatter(z_layer12,r_layer12,c='b',s=1.5,label='layer 12s')
ax.scatter(z_layer14,r_layer14,c='indigo',s=1.5,label='layer 14s')
plt.title('Global Indexing Scheme of 10 Events')
plt.xlabel('z')
plt.ylabel('r')
ax.legend(loc='lower right')
#plt.savefig(path2 + 'indexing_bylayer.png')
plt.show()












###BRAINSTORMING
"""
fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(z_layer2,r_layer2,s=1.5,label='layer 2s')
plt.title('Global Indexing Scheme of 10 Events')
plt.xlabel('z')
plt.ylabel('r')
#np_global_index = np.unique(np.array(z))
#classes = [str(i) for i in np_global_index]
#print(len(scatter.legend_elements()[0]), len(np_global_index))
#plt.legend(handles = scatter.legend_elements()[0], labels = classes)
#plt.savefig(path2 + 'layertry1.png')
plt.show() """

"""
layer2s = [(7,2), (8,2), (9,2)]

#Add new column of global index
def manual_indices(globalIndex,key):
    #for key in globalIndex.keys():
    #    return globalIndex[key]
    if key == (7,2) or key == (8,2):
        return globalIndex[key]
    else:
        print('bad')

print(manual_indices(globalIndex, (8,2)))
#print(globalIndex)"""
"""
def add_col(globalindex,key):
    for i in range(len(r)):
        for j in range(len(z)):
            if key == (i,j):
                hits['global_index'] = globalIndex[key]
                print(hits)

add_col(globalIndex, (hits['volume_id'], hits['layer_id'])"""

#plotting, no legend
#plt.figure()

#np_global_index = np.unique(hit_arr)
#print(np_global_index)

#layer1 = [2, ]

#for i in range(len(hit_arr)):
#    if hit_arr[i] == 2 or hit_arr[i] == 16
