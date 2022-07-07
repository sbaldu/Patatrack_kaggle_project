from urllib.request import parse_http_list
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.pyplot import eventplot
from more_itertools import first
from numpy import NaN, row_stack, sort, triu_indices
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
truth_df_files = glob.glob(path + 'event00000*-truth.csv')

# Take all the hit files
path = '/home/simone/Documents/thesis/train_3/'
hit_files = glob.glob(path + 'event00000*-hits.csv')

# Take all the particle files
path = '/home/simone/Documents/thesis/train_3/'
particle_files = glob.glob(path + 'event00000*-particles.csv')

# Take all the truth_track files
path = '/home/simone/Documents/thesis/tracksData/'
truth_files = glob.glob(path + 'truth_TrackB*.csv')

# Take all the track files
path = "/home/simone/Documents/thesis/tracksData/"
track_files = glob.glob(path + 'tracksP*.csv')
print(track_files)

# Define the cut that separates good tracks from bad ones
cut = 0.75      # 75%

# Dictionary containing all the accepted reconstructed tracks
correct_tracks = {}

def getKey(map_, value_):
    return list(map_.keys())[list(map_.values()).index(value_)] 

for nFile in range(len(track_files)):
    hits_df = pd.read_csv('/home/simone/Documents/thesis/train_3/event000006000-hits.csv')
    par_df = pd.read_csv('/home/simone/Documents/thesis/train_3/event000006000-particles.csv')
    truth_df = pd.read_csv('/home/simone/Documents/thesis/train_3/event000006000-truth.csv') 

    # Compute the trasverse momentum
    p_trasv = pd.concat([np.sqrt(par_df['px']**2 + par_df['py']**2)],axis=1)
    p_Trasv = p_trasv.rename(columns={0:'pTrasv'})
    par_df = pd.concat([par_df,p_Trasv],axis=1)
    
    allowed_pars = []
    for j in range(len(par_df['particle_id'].values.tolist())):
        if par_df['pTrasv'][j] >= 2:
            allowed_pars.append(par_df['particle_id'][j])
    print(len(allowed_pars))
    print(len(truth_df['hit_id'].values.tolist()))

    new_df = truth_df[truth_df['particle_id'].isin(allowed_pars)]
    new_df = new_df.reset_index()
    print(new_df)

    # I need a map that allows me to move from the original hit_id to the ones with fewer particles
    new_id_ = 0
    id_map = {}
    for j in range(len(truth_df['hit_id'].values.tolist())):
        if (truth_df['particle_id'][j] in allowed_pars):
            id_map[truth_df['hit_id'][j]] = new_id_
            new_id_ += 1
    print(id_map)

    #print(allowed_pars)
    #print(len(allowed_pars))
    #print(len(par_df['particle_id'].values.tolist()))
    #print(par_df)

    # Separate all the tracks
    track_file = pd.read_csv(track_files[nFile])
    truth_file = pd.read_csv(truth_files[nFile])

##################################################################################################     
    
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
    print(tracks)
    
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

    # Calculate the pseudorapidity for the graphs
    eta = []     # I'll define it later (float)
    for track in truth_tracks:
        last_id = track[-1]
        z = float(hits_df['z'][hits_df['hit_id'] == last_id])
        y = float(hits_df['y'][hits_df['hit_id'] == last_id])
        theta_ = np.arctan(y/z)
        eta_ = -np.log(np.abs(np.tan(theta_/2)))
        #print(eta_)
        eta.append(eta_)

    
    # Counter that counts how many hits have been assigned correctly
    counter = {}
    for j in range(len(tracks)):
        counter[j] = 0
    ratios = []
    for tTrack in truth_tracks:     # Cerca la miglior compatibilita' per ogni track
        counter = {}
        for hit_t in tTrack:
            for j in range(len(tracks)):
                counter[j] = 0
                for hit in tracks[j]:
                    if hit == hit_t:
                        counter[j] += 1
        
        # Find the track with the best compatibility
        #print(counter)
        max_ = max(counter.values())
        if max_ != 0:
            print(max_)
        ratio = max_/len(tTrack)
        print(ratio)
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

################################################################################################## 

#len_ = len(track_file['hit_id'])
    #trackId_series = pd.Series(np.zeros((len_)))
    #id_ = 0
    #for i in range(len_-1):
    #    trackId_series[i] = id_
    #    if track_file['hit_id'][i+1] < track_file['hit_id'][i]:
    #        id_ += 1
    #trackId_series[len_-1] = id_
    #df_track = pd.concat([track_file['hit_id'],trackId_series],axis=1)
    #df_track = df_track.rename(columns={0:'TrackId'})
    #print(df_track)
    #
    #tlen_ = len(truth_file['hit_id'])
    #tTrackId_series = pd.Series(np.zeros((tlen_)))
    #id_ = 0
    #for i in range(tlen_-1):
    #    tTrackId_series[i] = id_
    #    if truth_file['hit_id'][i+1] < truth_file['hit_id'][i]:
    #        id_ += 1
    #tTrackId_series[tlen_-1] = id_
    #df_tTrack = pd.concat([truth_file['hit_id'],tTrackId_series],axis=1)
    #df_tTrack = df_tTrack.rename(columns={0:'TrackId'})
    #print(df_tTrack)
    #
    ## Count how many hits have been assigned correctly
    ##tTracks_ids = list(set(df_tTrack['TrackId']))
    #tTracks_ids = np.unique(df_tTrack['TrackId'].values)
    #tracks_ids = np.unique(df_track['TrackId'].values)
    #tTracks = []
    #for id1 in tTracks_ids:
    #    r = 0
    #    t = 0
    #    saved_id = 0
    #    for id2 in tracks_ids:
    #        t = r
    #        r = np.max(r,len(list(set(df_tTrack[df_tTrack['TrackId'] == id1].hit_id) & set(df_track[df_track['TrackId'] == id2].hit_id))))
    #        if t != r:
    #            saved_id = id2
    #    print('a')
    #    if r/len(df_tTrack[df_tTrack['TrackId'] == id1].hit_id) > cut:
    #        tracks_ids.remove(saved_id)
    #        print(r)

    #id1 = 0
    #r = 0
    #t = 0
    #saved_id = 0
    #for id2 in tracks_ids:
    #    t = r
    #    r = np.max(r,len(list(set(df_tTrack[df_tTrack['TrackId'] == id1].hit_id) & set(df_track[df_track['TrackId'] == id2].hit_id))))
    #    if t != r:
    #        saved_id = id2
    #if r/len(df_tTrack[df_tTrack['TrackId'] == id1].hit_id) > cut:
    #    tracks_ids.remove(saved_id)
    #print(r)

# For the plot I need to make sure that the sorting of the particles in the pT dataframe is the same as in the truth_tracks File


#fig = plt.figure()
#plt.scatter(momenta,ratios)
#plt.xlabel("pT (GeV)")
#plt.ylabel("Ratio")
#plt.show() 