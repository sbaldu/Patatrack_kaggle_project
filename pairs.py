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

def plotPair(r_pair_,z_pair_):
    fig = plt.figure()
    plt.scatter([z_pair_[0],z_pair_[1]],[r_pair_[0],r_pair_[1]])
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1000)
    plt.show() 

hits_ = pd.read_csv(hit_files[0])
particles_ = pd.read_csv(par_files[0])
truth_ = pd.read_csv(truth_files[0])
print(hits_)
print(particles_)
print(truth_)

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

t_particle_types = list(set(truth_['particle_id'].values.tolist()))

for i in range(10):
    i += 8000
    indexes = sort_hits(t_particle_types[i])
    #print(indexes)
    
    hits_globalindexes = []
    r_ = []
    z_ = []
    pairs_ = []
    r_pair  =[]
    z_pair = []
    for index in indexes:
        #print(total_df['r'][index])
        if index != indexes[len(indexes)-1]:
            r_.append(total_df['r'][index])
            z_.append(total_df['z'][index])
            hits_globalindexes.append(total_df['globalIndex'][index])
            pairs_.append([total_df['globalIndex'][index],total_df['globalIndex'][indexes[indexes.index(index)+1]]])
            r_pair.append([total_df['r'][index],total_df['r'][indexes[indexes.index(index)+1]]])
            z_pair.append([total_df['z'][index],total_df['z'][indexes[indexes.index(index)+1]]])

    #print(hits_globalindexes)
    #print(r_)
    #print(z_)
    print(pairs_)
    for i in range(len(pairs_)):
        plotPair(r_pair[i],z_pair[i])
    """
    fig = plt.figure()
    plt.scatter(z_,r_)
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1000)
    plt.show()  
    """