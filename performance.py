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

# Take all the particle files
path = '/home/simone/Documents/thesis/particle/'
particle_files = glob.glob(path + 'event00000*-particle.csv')

# Take all the truth_track files
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
    print(track_file[len(track_file)-2])
    particle_df = pd.read_csv(particle_files[nFile])
    
    # Compute the trasverse momentum
    p_trasv = pd.concat([np.sqrt(particle_df['px']**2 + particle_df['py']**2)],axis=1)
    p_Trasv = p_trasv.rename(columns={0:'pTrasv'})
    
    # I also need to save the transverse momentum and eta
    eta = 0     # I'll define it later (float)

    # Separate all the tracks
    track_file = pd.read_csv(track_files[nFile])
    tracks = []
    for j in range(len(track_file)-1):
        single_track = []
        single_track.append(track_file[j])
        if j == (len(track_file)-2):
            single_track.append(track_file[j])
            break
        if track_file[j+1] < track_file[j]:
            tracks.append(single_track)
            single_track = []

    truth_track = pd.read_csv(truth_files[nFile])
    
    # Counter that counts how many hits have been assigned correctly
    counter = {}
    compatibiliy = {}

    for hit_t in truth_track:     # Cerca la miglior compatibilita' per ogni track
        for j in len(tracks):
            for hit in tracks[j]:
                if hit == hit_t:
                    counter[j] += 1
    
    # Find the track with the best compatibility
    
    #max = 0
    #for j in counter.keys():
    #    if counter[j] > max:
    #        max = counter[j]
    #        maxj
    max_comp =  max(counter.values())

    ratio = max_comp/len(truth_track)
    if ratio > cut:
        ratios.append(ratio)
        
# For the plot I need to make sure that the sorting of the particles in the pT dataframe is the same as in the truth_tracks File


#fig = plt.figure()
#plt.scatter(momenta,ratios)
#plt.xlabel("pT (GeV)")
#plt.ylabel("Ratio")
#plt.show() 