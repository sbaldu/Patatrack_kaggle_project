from urllib.request import parse_http_list
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.pyplot import eventplot
from more_itertools import first
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

hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
hit_df = pd.read_csv(hit_files[1])
volume_col = hit_df['volume_id'].values.tolist()

hits_dict = {}
for i in range(len(volume_col)):
    if volume_col[i] in hits_dict.keys():
        hits_dict[volume_col[i]] += 1
    else:
        hits_dict[volume_col[i]] = 1

print(hits_dict)
# {7: 15045, 8: 24686, 9: 14540, 12: 6692, 13: 22351, 14: 6802, 16: 2430, 17: 9396, 18: 2600}
