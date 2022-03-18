from matplotlib.pyplot import eventplot
from numpy import sort, triu_indices
from operator import index, truth
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.mplot3d import Axes3D
import glob

path = '/home/simonb/Documents/thesis/'

hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')
hit_files.sort()
par_files.sort()
truth_files.sort()

maxLayerId = 6
def layerGlobalIndex(volume,layer):
    return (volume-7)*(maxLayerId + 1) + (layer-2)

radius = []
z = []
index = []
for i in range(2):
    ev = pd.read_csv(hit_files[i])
    ev_hitid_col = ev['hit_id'].values.tolist()
    ev_lay_col = ev['layer_id'].values.tolist()
    ev_vol_col = ev['volume_id'].values.tolist()
    ev_x_col = ev['x'].values.tolist()
    ev_y_col = ev['y'].values.tolist()
    ev_z_col = ev['z'].values.tolist()
    length_= len(ev_lay_col)

    for i in range(length_):
        if (i%50) == 0:
            radius.append(np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2))
            z.append(ev_z_col[i])
            index.append(layerGlobalIndex(ev_vol_col[i],ev_lay_col[i]))

def plotPair(r_pair_,z_pair_):
    fig = plt.figure()
    plt.scatter([z_pair_[0],z_pair_[1]],[r_pair_[0],r_pair_[1]],marker='x',color='red')
    #cm = plt.cm.get_cmap('nipy_spectral')
    plt.scatter(z,radius)
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1000)
    plt.show() 

hits_ = pd.read_csv(hit_files[0])
particles_ = pd.read_csv(par_files[0])
truth_ = pd.read_csv(truth_files[0])

total_df = pd.concat([truth_['particle_id'],np.sqrt(hits_['x']**2 + hits_['y']**2),hits_['z'],layerGlobalIndex(hits_['volume_id'],hits_['layer_id'])],axis=1)
print(total_df)
total_df = total_df.rename(columns={0:'r'})
total_df = total_df.rename(columns={1:'globalIndex'})
total_df = total_df.sort_values(by='r',ascending=True)
total_df = total_df.reset_index(drop=True)
print(total_df)

def sort_hits(particle_id):
    list_hits = []

    for i in range(total_df['particle_id'].size):
        if total_df['particle_id'][i] == particle_id:
            list_hits.append(i)
            
    return list_hits

# From the truth df I find all the particle ids
t_particle_types = list(set(truth_['particle_id'].values.tolist()))
n_particles = len(t_particle_types)     # 8977

# I prepare che list of global indexes from the df to be used in Paula's code
index_list = total_df['globalIndex'].values.tolist()
index_list = np.unique(index_list) #remove duplicates

# Paula's code, which I'm using to assing an index to the pairs
def combine(index):
    """Given the global index of each layer ID, list every possible combination of layers"""
    pairs = []
    for i in range(len(index)):
        for j in range(i+1,len(index)):
            pairs.append([index[i], index[j]])
    pairs.sort()
    return pairs

pairs_combinations = combine(index_list)
#print(pairs_combinations)

def return_index(pair,pairs):
    for i in range(len(pairs)):
        if (pair == pairs[i]) or ([pair[1],pair[0]] == pairs[i]):
            return i
    return 'nope'

for i in range(int(n_particles/191)):
    par_hit_indexes = sort_hits(t_particle_types[i])
    #print(indexes)
    
    #hits_globalindexes = []
    r_ = []
    z_ = []
    pairs_ = []
    r_pair  =[]
    z_pair = []
    for index in par_hit_indexes:
        #print(total_df['r'][index])
        if (index != par_hit_indexes[len(par_hit_indexes)-1]) and (total_df['globalIndex'][index] != total_df['globalIndex'][par_hit_indexes[par_hit_indexes.index(index)+1]]):
            r_.append(total_df['r'][index])
            z_.append(total_df['z'][index])
            #hits_globalindexes.append(total_df['globalIndex'][index])
            pairs_.append([total_df['globalIndex'][index],total_df['globalIndex'][par_hit_indexes[par_hit_indexes.index(index)+1]]])
            r_pair.append([total_df['r'][index],total_df['r'][par_hit_indexes[par_hit_indexes.index(index)+1]]])
            z_pair.append([total_df['z'][index],total_df['z'][par_hit_indexes[par_hit_indexes.index(index)+1]]])

    #print(hits_globalindexes)
    #print(r_)
    #print(z_)
    #print(pairs_)
    
    fig = plt.figure()
    plt.scatter(z_,r_)
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1000)
    plt.show() 

    for i in range(len(pairs_)):
        plotPair(r_pair[i],z_pair[i])
    
    # Now I want to take all the doublets created for this particle and assign to each one a pair-index
    pair_indexes = []
    for pair in pairs_:
        pair_indexes.append(return_index(pair,pairs_combinations))
    print(pair_indexes)

    #dict_ = {}
    #for pair_ind in pair_indexes:
    #    dict_[pair_indexes] += 1