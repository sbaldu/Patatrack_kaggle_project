from matplotlib.cbook import ls_mapper
from matplotlib.pyplot import eventplot
from numpy import sort, triu_indices
from operator import index
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.mplot3d import Axes3D
import glob

path = '/home/simonb/documents/thesis/'

hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')
hit_files.sort()
par_files.sort()
truth_files.sort()

maxLayerId = 14
def layerGlobalIndex(volume,layer):
    return (volume-7)*(maxLayerId + 1) + (layer-2)

N = 1       # Number of events that I want to work with
total_df = None

# Paula's codem which I'm using to assing an index to the pairs
def combine(index):
    """Given the global index of each layer ID, list every possible combination of layers"""
    pairs = []
    for i in range(len(index)):
        for j in range(i+1,len(index)):
            pairs.append([index[i], index[j]])
    pairs.sort()
    return pairs

def return_index(pair,pairs):
    for i in range(len(pairs)):
        if pair == pairs[i]:
            return i

# I define a function that plots a pair of hits
def plotPair(r_pair_,z_pair_):
    fig = plt.figure()
    plt.scatter([z_pair_[0],z_pair_[1]],[r_pair_[0],r_pair_[1]])
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1000)
    plt.show() 

for i in range(N):
    ev_hit = pd.read_csv(hit_files[i])
    ev_truth = pd.read_csv(truth_files[i])
    #total_df = pd.concat([ev_truth['particle_id'],np.sqrt(ev_hit['x']**2 + ev_hit['y']**2),ev_hit['z'],layerGlobalIndex(ev_hit['volume_id'],ev_hit['layer_id'])],axis=1)
    total_df = pd.concat([np.sqrt(ev_hit['x']**2 + ev_hit['y']**2),ev_hit['z'],layerGlobalIndex(ev_hit['volume_id'],ev_hit['layer_id'])],axis=1)

    # Sort the dataframe by radius
    total_df = total_df.rename(columns={0:'r'})
    total_df = total_df.rename(columns={1:'globalIndex'})
    total_df = total_df.sort_values(by='r',ascending=True)

    print(total_df)

    # Get the number of rows in the dataframe
    df_length = total_df['r'].size
    print(df_length)
    indexes = total_df['globalIndex'].values.tolist()

    r_list = total_df['r'].values.tolist()
    z_list = total_df['z'].values.tolist()

    pairs = []
    r_pair = []
    z_pair = []
    for i in range(df_length-1):
        if indexes[i] != indexes[i+1]:
            pairs.append([indexes[i],indexes[i+1]])
            r_pair.append([r_list[i],r_list[i+1]])
            z_pair.append([z_list[i],z_list[i+1]])
    """
    print(pairs)
    print('\n'+'\n'+'\n')
    print(r_pair)
    print('\n'+'\n'+'\n')
    print(z_pair)
    print('\n'+'\n'+'\n')
    print(r_pair[0])
    print(z_pair[0])
    """
    for i in range(100):
        plotPair(r_pair[40000+i],z_pair[40000+i])
# I write the indexes list on a file to process the data in c++
"""
open_file = open("indexes.dat", 'w')
    
for i in range(df_length):
    open_file.write(str(indexes[i]) + '\n')
open_file.close()
"""