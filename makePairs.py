#from ossaudiodev import control_labels
#from re import T
#from matplotlib.pyplot import eventplot
#from numpy import sort, triu_indices
from operator import index
import pandas as pd
import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt
#from matplotlib import colors
#import matplotlib as mpl
#from matplotlib.ticker import PercentFormatter
#from mpl_toolkits.mplot3d import Axes3D
import glob

path = '/home/simonb/documents/thesis/'

hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')

maxLayerId = 14
def layerGlobalIndex(volume,layer):
    return (volume-7)*(maxLayerId + 1) + (layer-2)

N = 10       # Number of events that I want to work with
total_df = None

for i in range(N):
    ev_hit = pd.read_csv(hit_files[i])
    ev_truth = pd.read_csv(truth_files[i])
    #total_df = pd.concat([ev_truth['particle_id'],np.sqrt(ev_hit['x']**2 + ev_hit['y']**2),ev_hit['z'],layerGlobalIndex(ev_hit['volume_id'],ev_hit['layer_id'])],axis=1)
    total_df = pd.concat([np.sqrt(ev_hit['x']**2 + ev_hit['y']**2),ev_hit['z'],layerGlobalIndex(ev_hit['volume_id'],ev_hit['layer_id'])],axis=1)

    """
    if i == 0:
        total_df = df_
    elif i > 0:
        total_df = pd.concat([total_df,df_],ignore_index=True)
    """

    # Sort the dataframe by radius
    total_df = total_df.rename(columns={0:'r'})
    total_df = total_df.rename(columns={1:'globalIndex'})
    #total_df = total_df.sort_values(by='r',ascending=True)

    print(total_df)

    # Get the number of rows in the dataframe
    df_length = total_df['r'].size
    print(df_length)
    indexes = total_df['globalIndex'].values.tolist()

    pairs = []
    for i in range(df_length-1):
        if indexes[i] != indexes[i+1]:
            pairs.append([indexes[i],indexes[i+1]])
    print(pairs)
"""
pairs = []
for i in range(df_length):
    if (total_df['globalIndex'].values.tolist()[i] != total_df['globalIndex'].values.tolist()[i+1]) and (total_df['particle_id'].values.tolist()[i] == 445859661644562432):
        pairs.append([total_df['globalIndex'].values.tolist()[i],total_df['globalIndex'].values.tolist()[i+1]])
print(pairs)
"""
# I write the indexes list on a file to process the data in c++
"""
open_file = open("indexes.dat", 'w')
    
for i in range(df_length):
    open_file.write(str(indexes[i]) + '\n')
open_file.close()
"""
# Create all the possible combinations between the detector layers
#pairs = []
#for i in range(df_length):
#    for j in range(i+1,df_length):
#        pairs.append([indexes[i],indexes[j]])
#print(pairs)

"""
# I want to get the list of all the r for the same particle
new_df = pd.read_csv(path+'Patatrack_kaggle_project/test.csv')

print(new_df)

parids_list = new_df['particle_id'].values.tolist()
newdf_len = len(parids_list)
list_of_parids = list(set(parids_list))

par_id = 0
r_list = []
z_list = []
index_list = []

for i in range(newdf_len):
    if new_df['particle_id'].values.tolist()[i] == par_id:
        r_list.append(new_df['r'].values.tolist()[i])
        z_list.append(new_df['z'].values.tolist()[i])
        index_list.append(new_df['globalIndex'].values.tolist()[i])

r_series = pd.Series(r_list)
z_series = pd.Series(z_list)
index_series = pd.Series(index_list)

#index_series_list = index_series.values.tolist()
len_ = len(index_list)

par_df = pd.concat([r_series,z_series,index_series],axis=1)
par_df = par_df.rename(columns={0:'r'})
par_df = par_df.rename(columns={1:'z'})
par_df = par_df.rename(columns={2:'globalIndex'})

print(par_df)

def makePairs():
    list_of_pairs = []
    for i in range(len_-1):
        if par_df['globalIndex'].values.tolist()[i] != par_df['globalIndex'].values.tolist()[i+1]:
            list_of_pairs.append([par_df['globalIndex'].values.tolist()[i],par_df['globalIndex'].values.tolist()[i+1]])
    return list_of_pairs

print(makePairs())
"""