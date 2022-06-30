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
path = '/home/simone/Documents/thesis/train_3/'
particle_files = glob.glob(path + 'event00000*-particles.csv')

# Take all the truth_track files
path = '/home/simone/Documents/thesis/tracksData/'
truth_files = glob.glob(path + 'truth_TrackB*.csv')

# Take all the track files
path = "/home/simone/Documents/thesis/tracksData/"
track_files = glob.glob(path + 'tracks*.csv')

# Define the cut that separates good tracks from bad ones
cut = 0.75      # 75%

# Dictionary containing all the accepted reconstructed tracks
correct_tracks = {}

#ratios = []
#momenta = []
#etas = []       # eta del primo hit

for nFile in range(len(track_files)):
    particle_df = pd.read_csv(particle_files[nFile])
    
    # Compute the trasverse momentum
    p_trasv = pd.concat([np.sqrt(particle_df['px']**2 + particle_df['py']**2)],axis=1)
    p_Trasv = p_trasv.rename(columns={0:'pTrasv'})
    
    # I also need to save the transverse momentum and eta
    eta = 0     # I'll define it later (float)

    # Separate all the tracks
    track_file = pd.read_csv(track_files[nFile])
    truth_file = pd.read_csv(truth_files[nFile])

    #len_ = len(track_file['hit_id'])
    #ind = 0
    #indexes = []
    #for j in range(len_):
    #    indexes.append(ind)
    #    if (track_file['hit_id'][j] > track_file['hit_id'][j+1]) and (j != len_-1):
    #        ind += 1
    #indexes.append(ind)
    #df_track = pd.concat([track_file['hit_id'],indexes])
    #print(df_track)
    #
    tracks = []
    single_track = []
    for j in range(len(track_file)-1):
        single_track.append(track_file['hit_id'][j])
        if j == (len(track_file)-1):
            tracks.append(single_track)
            break
        if track_file['hit_id'][j+1] < track_file['hit_id'][j]:
            tracks.append(single_track)
            single_track = []
    
    truth_tracks = []
    single_tTrack = []
    for j in range(len(truth_file)-1):
        single_tTrack.append(truth_file['hit_id'][j])
        if j == (len(truth_file)-1):
            truth_tracks.append(single_tTrack)
            break
        if truth_file['hit_id'][j+1] < truth_file['hit_id'][j]:
            truth_tracks.append(single_tTrack)
            single_tTrack = []
    #print(truth_tracks)
    
    # Counter that counts how many hits have been assigned correctly
    #counter = {}
    #for j in range(len(tracks)):
    #    counter[j] = 0
    ratios = []
    for tTrack in truth_tracks:     # Cerca la miglior compatibilita' per ogni track
        counter = {}
        for hit_t in tTrack:
            for j in range(len(tracks)):
                counter[j] = 0
                #print('real track ')
                #print(tTrack)
                #print('possible track ')
                #print(tracks[j])
                for hit in tracks[j]:
                    #print('true hit: ')
                    #print(hit_t)
                    #print('possible hit: ')
                    #print(hit)
                    if hit == hit_t:
                        #print('-------------------------------------------------------------')
                        #print(hit == hit_t)
                        counter[j] += 1
        # Find the track with the best compatibility
        #print(counter)
        max_ = max(counter.values())
        #print(max)
        ratio = max_/len(tTrack)
        ratios.append(ratio)
    print(ratios)
    
    
    #max = 0
    #for j in counter.keys():
    #    if counter[j] > max:
    #        max = counter[j]
    #        maxj
    
    #max_comp =  max(counter.values())
    #
    #ratio = max_comp/len(truth_track)
    #if ratio > cut:
    #    ratios.append(ratio)
        
# For the plot I need to make sure that the sorting of the particles in the pT dataframe is the same as in the truth_tracks File


#fig = plt.figure()
#plt.scatter(momenta,ratios)
#plt.xlabel("pT (GeV)")
#plt.ylabel("Ratio")
#plt.show() 