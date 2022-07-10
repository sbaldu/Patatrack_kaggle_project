"""TrackML scoring metric"""

__authors__ = ['Sabrina Amrouche', 'David Rousseau', 'Moritz Kiehn',
               'Ilija Vukotic']

import numpy
import pandas
import random

#importing the csv files
df_truth = pandas.read_csv("/Users/angies/Desktop/Geneva Study Abroad/CERN/CERN_Patatrack/trackml-library/train_2/event000002820-truth.csv")
df_hits = pandas.read_csv("/Users/angies/Desktop/Geneva Study Abroad/CERN/CERN_Patatrack/trackml-library/train_2/event000002820-hits.csv")

#generating random tracks to test the scoring using the randomize code
import randomize_call
df_tracks = randomize_call.random_solution(df_hits, 5)
#print(df_tracks)


def _analyze_tracks(truth, submission):
    """Compute the majority particle, hit counts, and weight for each track.
    Parameters
    ----------
    truth : pandas.DataFrame
        Truth information. Must have hit_id, particle_id, and weight columns.
    submission : pandas.DataFrame
        Proposed hit/track association. Must have hit_id and track_id columns.
    Returns
    -------
    pandas.DataFrame
        Contains track_id, nhits, major_particle_id, major_particle_nhits,
        major_nhits, and major_weight columns.
    """
    # true number of hits for each particle_id
    particles_nhits = truth['particle_id'].value_counts(sort=False)
    total_weight = truth['weight'].sum()
    # combined event with minimal reconstructed and truth information
    event = pandas.merge(truth[['hit_id', 'particle_id', 'weight']],
                         submission[['hit_id', 'track_id']],
                         on=['hit_id'], how='left', validate='one_to_one')
    event.drop('hit_id', axis=1, inplace=True)
    event.sort_values(by=['track_id', 'particle_id'], inplace=True)
    #print(event)

    # ASSUMPTIONs: 0 <= track_id, 0 <= particle_id

    tracks = []
    # running sum for the reconstructed track we are currently in
    rec_track_id = -1
    rec_nhits = 0
    # running sum for the particle we are currently in (in this track_id)
    cur_particle_id = -1
    cur_nhits = 0
    cur_weight = 0
    # majority particle with most hits up to now (in this track_id)
    maj_particle_id = -1
    maj_nhits = 0
    maj_weight = 0

    for hit in event.itertuples(index=False):
        # we reached the next track so we need to finish the current one
        if (rec_track_id != -1) and (rec_track_id != hit.track_id):
            # could be that the current particle is the majority one
            if maj_nhits < cur_nhits:
                maj_particle_id = cur_particle_id
                maj_nhits = cur_nhits
                maj_weight = cur_weight
            # store values for this track
            tracks.append((rec_track_id, rec_nhits, maj_particle_id,
                particles_nhits[maj_particle_id], maj_nhits,
                maj_weight / total_weight))

        # setup running values for next track (or first)
        if rec_track_id != hit.track_id:
            rec_track_id = hit.track_id
            rec_nhits = 1
            cur_particle_id = hit.particle_id
            cur_nhits = 1
            cur_weight = hit.weight
            maj_particle_id = -1
            maj_nhits = 0
            maj_weights = 0
            continue

        # hit is part of the current reconstructed track
        rec_nhits += 1

        # reached new particle within the same reconstructed track
        if cur_particle_id != hit.particle_id:
            # check if last particle has more hits than the majority one
            # if yes, set the last particle as the new majority particle
            if maj_nhits < cur_nhits:
                maj_particle_id = cur_particle_id
                maj_nhits = cur_nhits
                maj_weight = cur_weight
            # reset runnig values for current particle
            cur_particle_id = hit.particle_id
            cur_nhits = 1
            cur_weight = hit.weight
        # hit belongs to the same particle within the same reconstructed track
        else:
            cur_nhits += 1
            cur_weight += hit.weight

    # last track is not handled inside the loop
    if maj_nhits < cur_nhits:
        maj_particle_id = cur_particle_id
        maj_nhits = cur_nhits
        maj_weight = cur_weight
    # store values for the last track
    tracks.append((rec_track_id, rec_nhits, maj_particle_id,
        particles_nhits[maj_particle_id], maj_nhits, maj_weight / total_weight))

    cols = ['track_id', 'nhits',
            'major_particle_id', 'major_particle_nhits',
            'major_nhits', 'major_weight']
    return pandas.DataFrame.from_records(tracks, columns=cols)

def score_event(truth, submission):
    """Compute the TrackML event score for a single event.
    Parameters
    ----------
    truth : pandas.DataFrame
        Truth information. Must have hit_id, particle_id, and weight columns.
    submission : pandas.DataFrame
        Proposed hit/track association. Must have hit_id and track_id columns.
    """
    tracks = _analyze_tracks(truth, submission)
    purity_rec = numpy.true_divide(tracks['major_nhits'], tracks['nhits'])
    purity_maj = numpy.true_divide(tracks['major_nhits'], tracks['major_particle_nhits'])
    good_track = (0.5 < purity_rec) & (0.5 < purity_maj)
    return tracks['major_weight'][good_track].sum()

import pandas as pd
import numpy as np
import copy

#testing a reconstructed track from the data 
#df_truth_track = pd.read_csv("~/CERN/new_data_train_2.csv")
#print(df_truth.track_id)

#track_ids = set(df_truth_track.track_id) #removes duplicates
#print(track_ids)
#print(len(track_ids))

hits_dropped_volume_7= []
score_array = []

#track_interest = track_ids.pop()
#my_mask = df_truth_track.track_id == track_interest
#print(my_mask)
#print(df_truth_track[my_mask])

 # using the real data 
df_truth = pd.read_csv("~/CERN/new_data_train_2.csv")
df_truth_volume_table = pd.read_csv("/Users/angies/Desktop/Geneva Study Abroad/CERN/CERN_Patatrack/trackml-library/train_2/event000002820-hits.csv")
#print(df_truth.track_id)
df_merged = df_truth.merge(df_truth_volume_table, how='outer', left_index=True, right_index=True)
del df_merged['hit_id_y']
df_merged = df_merged.rename(columns={"hit_id_x": "hit_id"})

track_ids = set(df_truth.track_id)
#print("previoustrackids\n",track_ids)
#print(len(track_ids))

#track_interest = random.choice(tuple(track_ids))
number_of_hits_dropped_from_volume = {}

for track_interest in random.sample(track_ids,100): #pick random track
    print(track_interest)
    my_mask = df_merged.track_id == track_interest #mask is the filter, df truth has a bunch of hits in a bunch of tracks, but filter the hits to be when its in a specific track, pick one track 
    #print(my_mask)
    df_truth_one_track = df_merged[my_mask] #apply filter, the square brackets apply the filter 
    df_truth_one_track = copy.deepcopy(df_truth_one_track)
    #scoring a track with dropped hits 
    df_truth_one_track.index
    df_truth_one_track["particle_id"] = df_truth_one_track.track_id
    #looking at relationship between volume ids and scores
    df_truth_one_track.volume_id
    set(df_truth_one_track.volume_id)
    #for volume in set(df_truth_one_track.volume_id): #loop over every volume of df_truth_one_track
    volume = 8 #for loop inside that for loop, drop up to max number of hits in that given volume, for that given track
    volume_mask = df_truth_one_track.volume_id == volume
    max_number_hits_in_volume = sum(volume_mask)
    for number_hits_to_drop in range(0, max_number_hits_in_volume):
         index_to_drop = df_truth_one_track[volume_mask].iloc[0:3].index 
         df_truth_track_with_dropped_hits = df_truth_one_track.drop(index = index_to_drop)
         score_array.append(score_event(df_truth_one_track,df_truth_track_with_dropped_hits))
         hits_dropped_volume_7.append(number_hits_to_drop)

#print(score_array)

import matplotlib.pyplot as plt 

scores_filtered = []

for num_dropped in range(max(hits_dropped_volume_7)):
    scores_for_fixed_number_drops = [] #save into this array
    for number_dropped,score in zip(hits_dropped_volume_7, score_array):   # for loop to find all of them
        if number_dropped == num_dropped:
            scores_for_fixed_number_drops.append(score)
    scores_filtered.append(np.mean(scores_for_fixed_number_drops)) #take the mean 

plt.bar(range(0,max(hits_dropped_volume_7)),scores_filtered)
plt.ylabel('Scores')
plt.xlabel('Number of Hits Dropped in Volume 7')
#plt.xticks([7,8,9,12,13,14,16,17,18])
plt.title('Scores vs Dropped Hits')
plt.show()