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

volume_array= []
score_array = []

#track_interest = track_ids.pop()
#my_mask = df_truth_track.track_id == track_interest
#print(my_mask)
#print(df_truth_track[my_mask])

 # using the real data 
df_truth = pd.read_csv("~/CERN/new_data_train_2.csv")
#print(df_truth.track_id)

track_ids = set(df_truth.track_id)
#print("previoustrackids\n",track_ids)
#print(len(track_ids))

track_interest = random.choice(tuple(track_ids))
number_of_hits_dropped_from_volume = {}

for track_interest in random.sample(track_ids,100):
    print(track_interest)
    my_mask = df_truth.track_id == track_interest
    #print(my_mask)
    df_truth_one_track = df_truth[my_mask]
    df_truth_one_track = copy.deepcopy(df_truth_one_track)
    #scoring a track with dropped hits 
    df_truth_one_track.index
    df_truth_one_track["particle_id"] = df_truth_one_track.track_id
    #looking at relationship between volume ids and scores
    df_truth_volume_table = pd.read_csv("/Users/angies/Desktop/Geneva Study Abroad/CERN/CERN_Patatrack/trackml-library/train_2/event000002820-hits.csv")
    #new_hit = df_truth_one_track.iloc[:1]
    volume = random.choice([7,8,9,12,13,14,16,17,18])
    mask = df_truth_volume_table.volume_id == volume
    all_hits_in_volume_12 = df_truth_volume_table[mask]
    random_hit = all_hits_in_volume_12.sample()
    new_hit = df_truth[df_truth.hit_id == random_hit.hit_id.iloc[0]]
    new_hit['particle_id'] = df_truth_one_track.particle_id.iloc[0] 
    df_truth_one_track_plus_hit = pd.concat([df_truth_one_track, new_hit])

    score_array.append(score_event(df_truth_one_track,df_truth_one_track_plus_hit))
    volume_array.append(volume)

print(number_of_hits_dropped_from_volume)
#print(volume_array)
#print(score_array)

import matplotlib.pyplot as plt 

volume_list = list(set(volume_array))  # get a list of volumes with no duplicates 
scores = []

for volume_id in volume_list:
    list_scores_in_volume=[]
    for volume,score in zip(volume_array, score_array): 
        if volume == volume_id: 
            list_scores_in_volume.append(score)
    scores.append(np.mean(list_scores_in_volume))

plt.bar(volume_list,scores)
plt.ylabel('Scores')
plt.xlabel('Volumes')
plt.xticks([7,8,9,12,13,14,16,17,18])
plt.title('Scores vs Volumes')
plt.show()