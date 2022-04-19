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

path = '/home/simone/Documents/thesis/'

# We define a map for the indexes
index_map = {}

index_map[(7,2)] = 10
index_map[(7,4)] = 9
index_map[(7,6)] = 8
index_map[(7,8)] = 7
index_map[(7,10)] = 6
index_map[(7,12)] = 5
index_map[(7,14)] = 4
index_map[(8,2)] = 0
index_map[(8,4)] = 1
index_map[(8,6)] = 2
index_map[(8,8)] = 3
index_map[(9,2)] = 11
index_map[(9,4)] = 12
index_map[(9,6)] = 13
index_map[(9,8)] = 14
index_map[(9,10)] = 15
index_map[(9,12)] = 16
index_map[(9,14)] = 17
index_map[(12,2)] = 27
index_map[(12,4)] = 26
index_map[(12,6)] = 25
index_map[(12,8)] = 24
index_map[(12,10)] = 23
index_map[(12,12)] = 22
index_map[(13,2)] = 18
index_map[(13,4)] = 19
index_map[(13,6)] = 20
index_map[(13,8)] = 21
index_map[(14,2)] = 28
index_map[(14,4)] = 29
index_map[(14,6)] = 30
index_map[(14,8)] = 31
index_map[(14,10)] = 32
index_map[(14,12)] = 33
index_map[(16,2)] = 41
index_map[(16,4)] = 40
index_map[(16,6)] = 39
index_map[(16,8)] = 38
index_map[(16,10)] = 37
index_map[(16,12)] = 36
index_map[(17,2)] = 34
index_map[(17,4)] = 35
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

df = pd.concat([pd.read_csv(truth_files[0])['particle_id'],pd.read_csv(hit_files[0])],axis=1)
print(df)

vol = df['volume_id'].values.tolist()
size = len(vol)

nine_count = 0
seven_count = 0
all_count = 0
for i in range(size):
    if df['particle_id'][i] == 0:
        all_count += 1
        if vol[i] == 9:
            nine_count += 1
        if vol[i] == 7:
            seven_count += 1
print(nine_count)
print(all_count)
print(seven_count)
