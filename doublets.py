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

#Set maxima
maxLayerId = hits['layer_id'].max()
maxVolId = hits['volume_id'].max()

#Make list of global indices
hits['global_index'] = (hits['volume_id']-7) * (maxLayerId+1) + (hits['layer_id'])
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

#sample: print(return_index([2,19],list))