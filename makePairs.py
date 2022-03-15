#from ossaudiodev import control_labels
#from re import T
#from matplotlib.pyplot import eventplot
#from numpy import sort, triu_indices
import pandas as pd
#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt
#from matplotlib import colors
#import matplotlib as mpl
#from matplotlib.ticker import PercentFormatter
#from mpl_toolkits.mplot3d import Axes3D
#import glob

path = '/home/simonb/documents/thesis/'

# I want to get the list of all the r for the same particle
new_df = pd.read_csv(path+'Patatrack_kaggle_project/test.dat')

par_id = 0
r_list = []
z_list = []
index_list = []
ids = list(set(new_df['particle_id'].values.tolist()))
r_series = []
z_series = []
index_series = []

for i in range(10000):
    if new_df['particle_id'].values.tolist()[i] == par_id:
        r_series.append(new_df['r'].values.tolist()[i])
        z_series.append(new_df['z'].values.tolist()[i])
        index_series.append(new_df['globalIndex'].values.tolist()[i])

r_series = pd.Series(r_series)
z_series = pd.Series(z_series)
index_series = pd.Series(index_series)

index_series_list = index_series.values.tolist()
len_ = len(index_series_list)

par_df = pd.concat([r_series,z_series,index_series],axis=1)
par_df = par_df.rename(columns={0:'r'})
par_df = par_df.rename(columns={1:'z'})
par_df = par_df.rename(columns={2:'globalIndex'})

print(par_df)

def makePairs():
    list_of_pairs = []
    for i in range(len_-1):
        list_of_pairs.append([par_df['globalIndex'].values.tolist()[i],par_df['globalIndex'].values.tolist()[i+1]])
    return list_of_pairs

print(makePairs())