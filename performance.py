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

# Take all the truth files
path = '/home/simone/Documents/thesis/train_3/'
truth_files = glob.glob(path + 'event00000*-truth.csv')

#Take all the truth_track files
path = '/home/simone/Documents/thesis/not_sorted/'
truth_files = glob.glob(path + 'hist_ns*.csv')

# Take all the track files
path = "/home/simone/Documents/thesis/tracksData/"
track_files = glob.glob(path + 'track*.dat')

# Define the cut that separates good tracks from bad ones
cut = 0.75      # 75%

# Dictionary containing all the accepted reconstructed tracks
correct_tracks = {}

ratios = []
momenta = []
etas = []       # eta del primo hit

for nFile in len(track_files):
    # I also need to save the transverse momentum and eta
    pT = 0
    eta = 0     # I'll define them later (float)

    track = pd.read_csv(track_files[nFile])
    truth_track = pd.read_csv(truth_files[nFile])
    
    # Counter that counts how many hits have been assigned correctly
    counter = 0

    for hit in truth_track:     # Cerca la miglior compatibilita' per ogni track
        if hit in track:    # metti un altro for
            counter += 1
    
    ratio = counter/len(truth_track)
    if ratio > cut:
        #correct_tracks[nFile] = [ratio,pT,eta]
        ratios.append(ratio)
        momenta.append(pT)
        etas.append(eta)
        
fig = plt.figure()
plt.scatter(momenta,ratios)
plt.xlabel("pT (GeV)")
plt.ylabel("Ratio")
plt.show() 