from urllib.request import parse_http_list
from matplotlib.backend_bases import FigureManagerBase
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

# We define a map for the indexes
index_map = {}

index_map[(7,2)] = 0
index_map[(7,4)] = 1
index_map[(7,6)] = 2
index_map[(7,8)] = 3
index_map[(7,10)] = 4
index_map[(7,12)] = 5
index_map[(7,14)] = 6
index_map[(8,2)] = 7
index_map[(8,4)] = 8
index_map[(8,6)] = 9
index_map[(8,8)] = 10
index_map[(9,2)] = 11
index_map[(9,4)] = 12
index_map[(9,6)] = 13
index_map[(9,8)] = 14
index_map[(9,10)] = 15
index_map[(9,12)] = 16
index_map[(9,14)] = 17
index_map[(12,2)] = 18
index_map[(12,4)] = 19
index_map[(12,6)] = 20
index_map[(12,8)] = 21
index_map[(12,10)] = 22
index_map[(12,12)] = 23
index_map[(13,2)] = 24
index_map[(13,4)] = 25
index_map[(13,6)] = 26
index_map[(13,8)] = 27
index_map[(14,2)] = 28
index_map[(14,4)] = 29
index_map[(14,6)] = 30
index_map[(14,8)] = 31
index_map[(14,10)] = 32
index_map[(14,12)] = 33
index_map[(16,2)] = 34
index_map[(16,4)] = 35
index_map[(16,6)] = 36
index_map[(16,8)] = 37
index_map[(16,10)] = 38
index_map[(16,12)] = 39
index_map[(17,2)] = 40
index_map[(17,4)] = 41
index_map[(18,2)] = 42
index_map[(18,4)] = 43
index_map[(18,6)] = 44
index_map[(18,8)] = 45
index_map[(18,10)] = 46
index_map[(18,12)] = 47


hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')
hit_files.sort()
par_files.sort()
truth_files.sort()

radius = []
z = []
index = []
"""
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
"""

def plotPair(r_pair_,z_pair_):
    fig = plt.figure()
    #cm = plt.cm.get_cmap('nipy_spectral')
    plt.scatter(z,radius,color='#008080')
    plt.scatter([z_pair_[0],z_pair_[1]],[r_pair_[0],r_pair_[1]],s=80,marker='X',color='red')
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1000)
    plt.show() 

open_hit_file = open("test_par_hits.dat", 'w')
open_truth_file = open("test_globalIndexes.dat", 'w') 
    
hit_df = pd.read_csv(hit_files[0])
truth_df = pd.read_csv(truth_files[0])
layer_ids = hit_df['layer_id'].values.tolist()
volume_ids = hit_df['volume_id'].values.tolist()
df_size = len(layer_ids)
indexes_list_ = []
"""
for row in range(df_size):
    indexes_list_.append(index_map[(volume_ids[row],layer_ids[row])])
    globalIndexes = pd.Series(indexes_list_)

total_df_ = pd.concat([truth_df['particle_id'],np.sqrt(hit_df['x']**2 + hit_df['y']**2),hit_df['z'],globalIndexes],axis=1)
total_df_ = total_df_.rename(columns={0:'r'})
total_df_ = total_df_.rename(columns={1:'globalIndex'})
total_df_ = total_df_.sort_values(by='particle_id',ascending=True)
par_ids_list_ = total_df_['particle_id'].values.tolist()
index_list_ = total_df_['globalIndex'].values.tolist()

total_df_size = total_df_['particle_id'].size

for i in range(total_df_size):
    if par_ids_list_[i] != 0:
        #print(par_ids_list_[i]) 
        open_hit_file.write(str(par_ids_list_[i]) + '\n')
        open_truth_file.write(str(index_list_[i]) + '\n')
    
open_hit_file.close()
open_truth_file.close() 
"""

for i in range(len(hit_files)):
    open_hit_file = open(path + "doublet_files/par_hits" + str(i) + ".dat", 'w')
    open_truth_file = open(path + "doublet_files/globalIndexes" + str(i) + ".dat", 'w') 
    
    hit_df = pd.read_csv(hit_files[i])
    truth_df = pd.read_csv(truth_files[i])
    layer_ids = hit_df['layer_id'].values.tolist()
    volume_ids = hit_df['volume_id'].values.tolist()
    df_size = len(layer_ids)
    indexes_list_ = []

    for row in range(df_size):
        indexes_list_.append(index_map[(volume_ids[row],layer_ids[row])])
    globalIndexes = pd.Series(indexes_list_)

    total_df_ = pd.concat([truth_df['particle_id'],np.sqrt(hit_df['x']**2 + hit_df['y']**2),hit_df['z'],globalIndexes],axis=1)
    total_df_ = total_df_.rename(columns={0:'r'})
    total_df_ = total_df_.rename(columns={1:'globalIndex'})
    total_df_ = total_df_.sort_values(by='particle_id',ascending=True)
    par_ids_list_ = total_df_['particle_id'].values.tolist()
    index_list_ = total_df_['globalIndex'].values.tolist()

    total_df_size = total_df_['particle_id'].size

    for i in range(total_df_size):
        if par_ids_list_[i] != 0:
            #print(par_ids_list_[i]) 
            open_hit_file.write(str(par_ids_list_[i]) + '\n')
            open_truth_file.write(str(index_list_[i]) + '\n')
    
    open_hit_file.close()
    open_truth_file.close()    

hits_ = pd.read_csv(hit_files[0])
particles_ = pd.read_csv(par_files[0])
truth_ = pd.read_csv(truth_files[0])

layer_ids = hits_['layer_id'].values.tolist()
volume_ids = hits_['volume_id'].values.tolist()
df_size = len(layer_ids)
indexes_list = []

for row in range(df_size):
    indexes_list.append(index_map[(volume_ids[row],layer_ids[row])])
globalIndexes = pd.Series(indexes_list)

total_df = pd.concat([truth_['particle_id'],np.sqrt(hits_['x']**2 + hits_['y']**2),hits_['z'],globalIndexes],axis=1)
total_df = total_df.rename(columns={0:'r'})
total_df = total_df.rename(columns={1:'globalIndex'})
#total_df = total_df.sort_values(by='r',ascending=True)
#total_df = total_df.reset_index(drop=True)
print(total_df)

total_df_size = total_df['particle_id'].size
"""
open_file = open("par_hits.dat", 'w')    
for i in range(total_df_size):
    open_file.write(str(total_df['particle_id'][i]) + '\n')
open_file.close()

open_file = open("globalIndexes.dat", 'w')    
for i in range(total_df_size):
    open_file.write(str(total_df['globalIndex'][i]) + '\n')
open_file.close()
"""
def sort_hits(particle_id):
    list_hits = []

    for i in range(total_df_size):
        if total_df['particle_id'][i] == particle_id:
            list_hits.append(i)
            
    return list_hits

# From the truth df I find all the particle ids
t_particle_types = list(set(truth_['particle_id'].values.tolist()))
n_particles = len(t_particle_types)     # 8977

# I prepare che list of global indexes from the df to be used in Paula's code
indexes_list_nodupl = np.unique(indexes_list) #remove duplicates

# Paula's code, which I'm using to assing an index to the pairs
def combine(index):
    """Given the global index of each layer ID, list every possible combination of layers"""
    pairs = []
    for i in range(len(index)):
        for j in range(i+1,len(index)):
            pairs.append([index[i], index[j]])
    pairs.sort()
    return pairs

pairs_combinations = combine(indexes_list_nodupl)
print(len(pairs_combinations))

def return_index(pair,pairs):
    for i in range(len(pairs)):
        if (pair == pairs[i]) or ([pair[1],pair[0]] == pairs[i]):
            return i
    return 'nope'

list_pair_indexes = []

for i in range(n_particles):
    print(i)
    if t_particle_types[i] != 0:
        par_hit_indexes = sort_hits(t_particle_types[i])        # I think that this function is slowing down the program
        print(t_particle_types[i])
    
        #hits_globalindexes = []
        #r_ = []
        #z_ = []
        pairs_ = []
        #r_pair  =[]
        #z_pair = []
        for index in par_hit_indexes:
            #print(total_df['r'][index])
            if (index != par_hit_indexes[len(par_hit_indexes)-1]) and (total_df['globalIndex'][index] != total_df['globalIndex'][par_hit_indexes[par_hit_indexes.index(index)+1]]):
                #r_.append(total_df['r'][index])
                #z_.append(total_df['z'][index])
                #hits_globalindexes.append(total_df['globalIndex'][index])
                pairs_.append([total_df['globalIndex'][index],total_df['globalIndex'][par_hit_indexes[par_hit_indexes.index(index)+1]]])
                #r_pair.append([total_df['r'][index],total_df['r'][par_hit_indexes[par_hit_indexes.index(index)+1]]])
                #z_pair.append([total_df['z'][index],total_df['z'][par_hit_indexes[par_hit_indexes.index(index)+1]]])
    
        #print(hits_globalindexes)
        #print(r_)
        #print(z_)
        print(pairs_)
    
        """
        fig = plt.figure()
        plt.scatter(z_,r_)
        plt.xlabel("z (mm)")
        plt.ylabel("r (mm)")
        plt.xlim(-3000,3000)
        plt.ylim(0,1000)
        plt.show() 
        """

        #for i in range(len(pairs_)):
        #    plotPair(r_pair[i],z_pair[i])
    
        # Now I want to take all the doublets created for this particle and assign to each one a pair-index
        pair_indexes = []
        for pair in pairs_:
            pair_indexes.append(return_index(pair,pairs_combinations))
        #print(pair_indexes)
        list_pair_indexes += pair_indexes   
    
dict_ = {}
#for pair_ind in list_pair_indexes:
#    key_ = str(pair_ind)
#    if (key_ in dict_) == False:
#        dict_[str(pair_ind)] = 1
#    else:
#        dict_[str(pair_ind)] += 1
#print(dict_)

n_of_pairs = len(list_pair_indexes)
#print(len(list_pair_indexes))
open_file = open("doubletsIndexes.csv", 'w')
    
for i in range(n_of_pairs):
    open_file.write(str(list_pair_indexes[i]) + '\n')
open_file.close()