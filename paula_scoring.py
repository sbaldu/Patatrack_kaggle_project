from curses import KEY_NEXT
from hashlib import new
from lib2to3.pgen2 import driver
from operator import le, truth
from re import T, sub
from typing import final
from unittest.util import sorted_list_difference
#from this import s
import numpy
import pandas
import random
from random import randrange
import copy
from pathlib import Path
import matplotlib.pyplot as plt

'''Notes:
- scoring function always returns 1 for individual events, tried for diff ones
- scoring function returns a little more than 1 for multiple events when normalized (1.00002), less when not (0.9999999)
- is my normalization wrong?
- takes a while to run, probably due to big for loops and datasets'''


#importing the csv files
path = '/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/train_1'

#just one event 
hits_file = pandas.read_csv(path + '/event000001004-hits.csv')
df_hits = pandas.DataFrame(data=hits_file)
truth_file = pandas.read_csv(path + '/event000001004-truth.csv')
df_truth = pandas.DataFrame(data=truth_file)

#eliminate all data not in blue detector region
blue_section = [7,8,9]
blue_hitsdf = df_hits[df_hits['volume_id'].isin(blue_section)]
blue_hitcol = blue_hitsdf['hit_id']
blue_truthdf = df_truth[df_truth['hit_id'].isin(blue_hitcol)]

#sum weights and sort by particle
#grouped_weights = copy.deepcopy(blue_truthdf)
grouped_weights = pandas.DataFrame(data=blue_truthdf)
grouped_weights = grouped_weights.groupby("particle_id")
grouped_weights = grouped_weights["weight"].apply(list)
grouped_weights = grouped_weights.reset_index()
grouped_weights = grouped_weights.iloc[1:,:]

def calc_Sum(df):
    '''Calculate the sum of weights belonging to each hit of a particle, return dataframe with sums as a column'''
    sum = 0
    sum_array = []
    for array in df['weight']:
        for i in range(len(array)):
            sum = sum + array[i]
        sum_array.append(sum)
    df['wsum'] = sum_array
        #df.at[df.index,'wsum'] = sum
    df = df.drop(['weight'],axis=1)
    df = df.rename(columns={'wsum':'weight'},inplace=False)
    return df
#grouped_weights = calc_Sum(grouped_weights)
sort_weights = calc_Sum(grouped_weights)
#truth = blue_truthdf.groupby("particle_id")

#sort leftover hits by particle ID and add coln of weight sums              ** this is new truth file to score against
truth = pandas.DataFrame(data=blue_truthdf)
truth = truth.groupby("particle_id")
truth = truth["hit_id"].apply(list)
truth = truth.reset_index()
truth = truth.iloc[1:,:]
truth['weight'] = sort_weights['weight']
#truth = truth.iloc[2:,:]       #6759 length
truth.to_csv('truth.csv',index=False)
plswork = truth.copy(deep=True)
#print(plswork)
#plswork = copy.deepcopy(truth)

def changingHits(blue_truth,blue_hits): #slow with random.sample, faster with random.choices but might allow duplicates
    #Drops/adds a random amount of hits for every group of hits per particle, returns new dataframe
    #truth_copy = copy.deepcopy(blue_truth.iloc[:,[0,1]])
    #hits_copy = copy.deepcopy(blue_hits)
    #truth_hits = truth_copy['hit_id']
    #hits_hits = hits_copy['hit_id']
    truth_hits = blue_truth['hit_id']
    hits_hits = blue_hits['hit_id']
    new_hitarray = list()

    for hit_array in truth_hits:
        if len(hit_array) > 1 and len(hit_array) <= 10:
            ndrop = int(1) #randrange(0,1,1), making a range would be more ideal but idk
            k = randrange(1,2) #start at 1 so no empty arrays
            random_add = random.sample(list(hits_hits),k) #enclose in tuple for tuple appendage instead of array
            hit_array.append(random_add[0]) #appends as arrays, explode twice later to remove this formatting
        else:
            ndrop = randrange(0,len(hit_array),1)
            k = randrange(1,10) # again start at 1 so no empty arrays, maybe fix later
            random_add = random.sample(list(hits_hits),k)
            hit_array.append(random_add[0])
        if ndrop >= len(hit_array):
            print('fail') #makes sure no empty arrays
        #dataframe['ndrop'] = ndrop   (optional)
        hit_array.pop(ndrop)
        new_hitarray.append(hit_array)
    #truth_copy['hit_id'] = truth_hits
    blue_truth['hit_id'] = new_hitarray

    #truth_copy = truth_copy.explode('hit_id') 
    blue_truth = blue_truth.rename(columns={'particle_id':'track_id'},inplace=False)
    blue_truth = blue_truth.iloc[:,[0,1]]
    #print(truth_copy)
    #truth_copy = truth_copy.iloc[1:,:]
    #truth_copy.to_csv('truth.csv',index=False) #can alter later to make overwrite file each time
    #truth = pandas.DataFrame(data=truth_copy)
    return(blue_truth)
submission = changingHits(plswork,blue_hitsdf) #53478 length              ** This is submission file
#print('truth')
#print(truth)
#print('submission')
#print(submission)


submission = submission.to_csv('submission.csv',index=False)
truth = pandas.read_csv('truth.csv')
submission = pandas.read_csv('submission.csv')
#print(truth)
#print('here')
#print(truth)
#print(submission)


###################################################################

# TEST FILES

truth_copy1 = df_truth.copy()
truth_copy1.rename(columns={"particle_id":"track_id"},inplace=True)
df_truth2 = df_truth.copy()
truth_copy1 = truth_copy1.iloc[1:,:]
df_truth2 = df_truth2.iloc[1:,:]
#df_truth2.rename(columns={"particle_id":"track_id"},inplace=True)

################################################################### 

# SCORING FUNCTIONS

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
    print(particles_nhits)
    total_weight = truth['weight'].sum()
    # combined event with minimal reconstructed and truth information
    event = pandas.merge(truth[['hit_id', 'particle_id', 'weight']],
                         submission[['hit_id', 'track_id']],
                         on=['hit_id'], how='left', validate='m:m') #changed validate='one_to_one'
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
    #print(hit.track_ids)
    return pandas.DataFrame.from_records(tracks, columns=cols)

#print(_analyze_tracks(df_truth,truth_copy1))
#print(_analyze_tracks(truth,submission))

def score_event(truth, submission):
    """Compute the TrackML event score for a single event.
    Parameters
    ----------
    truth : pandas.DataFrame
        Truth information. Must have hit_id, particle_id, and weight columns.
    submission : pandas.DataFrame
        Proposed hit/track association. Must have hit_id and track_id columns.
    

    if 'event' in truth.columns:
        
        tracks = _analyze_tracks(truth, submission)
    else:"""
    tracks = _analyze_tracks(truth, submission)
    #print(tracks)


    ##EDIT: NORMALIZED
    tracks['major_nhits'] /= tracks['major_nhits'].sum()
    tracks['nhits'] /= tracks['nhits'].sum()
    tracks['major_particle_nhits'] /= tracks['major_particle_nhits'].sum()
    tracks['major_weight'] /= tracks['major_weight'].sum()

    purity_rec = numpy.true_divide(tracks['major_nhits'], tracks['nhits'])
    purity_maj = numpy.true_divide(tracks['major_nhits'], tracks['major_particle_nhits'])
    good_track = (0.5 < purity_rec) & (0.5 < purity_maj)
    return tracks['major_weight'][good_track].sum() #comment out/fix so score is per track not per event

#print(score_event(df_truth2,truth_copy1))
#print(score_event(truth,submission))

#############################################################
##################################################

# TRACKS INSTEAD OF EVENTS

'''
def oneFakeTrack(tracks):
    #random_track_id = random.sample(list(tracks),k=1)
    random_track_id = random.choice(tracks,1)
    track_interest = numpy.empty((0,3),int)
    print(random_track_id)
    for track in tracks:
        if track == random_track_id:
            return True
        else:
            return False
            #track_interest.append(random_track_id)
            #track_interest = numpy.append(track_interest, numpy.array([random_track_id]),axis=0)
            #print(track_interest)
#print(oneFakeTrack(tracks))'''


###############################

# BRAINSTORM
'''
def makeTuple(df):
    for item in df.columns:
        item = tuple(item)
    return(df)
s = makeTuple(truth)
plswork = pandas.DataFrame(data = s)'''