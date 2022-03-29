"""Make a new indexing scheme that assigns a number to each layer pair"""

import pandas as pd
import numpy as np
from pathlib import Path

path = '/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/train_1/'

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

#hits sorted by increasing radius
hits_read = read_in(path, 10, 'hits')
hits_read['r'] = np.sqrt(hits_read['x']**2 + hits_read['y']**2)
hits = pd.DataFrame(data=hits_read.loc[:,["hit_id","r","z","volume_id","layer_id"]])
hits = hits.sort_values('r')


compactLayerId = hits['layer_id']/2 -1
#Set maxima
maxLayerId = hits['layer_id'].max()
maxVolId = hits['volume_id'].max() -7

#Make list of global indices
hits['global_index'] = maxVolId * (maxLayerId+1) + compactLayerId

index_list = hits['global_index'].values.tolist()
index_list = list(set(index_list)) #remove duplicates
index_list.sort() #note: missing ghost layers

#make list of all possible combinations
def combine(index):
    """Given the global index of each layer ID, list every possible combination of layers"""
    pairs = []
    for i in range(len(index_list)):
        for j in range(i+1,len(index_list)):
            pairs.append([index_list[i], index_list[j]])
    pairs.sort()
    return pairs

list = combine(index_list)

def return_index(pair,pairs):
    for i in range(len(pairs)):
        if pair == pairs[i]:
            return i

print(return_index([7,2],list))

#Felice notes
### layer id in dataframe
#2 4 6 8 
#newLayerId = layerId/2 -1 

#manually input indices per volid,layerid pair
globalIndex = {}
globalIndex[(7,2)] = 0
globalIndex[(7,4)] = 1
globalIndex[(7,6)] = 2
globalIndex[(7,8)] = 3
globalIndex[(7,10)] = 4
globalIndex[(7,12)] = 5
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
#print(globalIndex[(7,10)])