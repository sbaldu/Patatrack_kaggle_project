from curses import KEY_NEXT
from lib2to3.pgen2 import driver
from operator import le, truth
from typing import final
#from this import s
import numpy
import pandas
import random
from random import randrange
import copy

#importing the csv files
path = '/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/train_1'
hits_file = pandas.read_csv(path + '/event000002819-hits.csv')
df_hits = pandas.DataFrame(data=hits_file)
truth_file = pandas.read_csv(path + '/event000002819-truth.csv')
df_truth = pandas.DataFrame(data=truth_file)


'''
#Running multiple events through   ** might have to reset index
def read_in(filepath,count,type):
    """Given filepath, read in count-amount of each type of file and return one
    concatenated dataframe"""
    i=0
    pathlist = Path(filepath).rglob('*' + type + '.csv')
    df = None
    for filepath in pathlist:
        path_in_str = str(filepath)
        i += 1
        toadd = pd.read_csv(path_in_str)
        if df is None: 
            df = toadd
        else:
            df.append(toadd)
        if i == count:
            break
    return(df)
big_truth = read_in(path,100,truth)
big_hits = read_in(path,100,hits)
'''


#eliminate all data not in blue detector region
blue_section = [7,8,9]
blue_hitsdf = df_hits[df_hits['volume_id'].isin(blue_section)]
blue_hitcol = blue_hitsdf['hit_id']
blue_truthdf = df_truth[df_truth['hit_id'].isin(blue_hitcol)]


#sum weights and sort by particle
grouped_weights = copy.deepcopy(blue_truthdf)
grouped_weights = grouped_weights.groupby("particle_id")
grouped_weights = grouped_weights["weight"].apply(list)
grouped_weights = grouped_weights.reset_index()

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
grouped_weights = calc_Sum(grouped_weights)

#sort leftover hits by particle ID and add coln of weight sums              ** this is new truth file to score against
grouped_truth = blue_truthdf.groupby("particle_id")
sorted_hits = grouped_truth["hit_id"].apply(list)
sorted_hits = sorted_hits.reset_index()
sorted_hits['weight'] = grouped_weights['weight']       #6760 length


#double check no duplicate particle ids
def duplicateCheck(array):
    ''' Check if given array contains any duplicates '''
    if len(array) == len(set(array)):
        return 'none!'
    else:
        return 'oh no!'
#print(duplicateCheck(particles))


def changingHits(blue_truth,blue_hits): #slow with random.sample, faster with random.choices but might allow duplicates
    '''Drops/adds a random amount of hits for every group of hits per particle, returns new dataframe'''
    truth_copy = copy.deepcopy(blue_truth)
    hits_copy = copy.deepcopy(blue_hits)
    truth_hits = truth_copy['hit_id'][1:]
    hits_hits = hits_copy['hit_id']

    for hit_array in truth_hits:
        if len(hit_array) > 1 and len(hit_array) <= 10:
            ndrop = int(1) #randrange(0,1,1), making a range would be more ideal but idk
            k = randrange(1,2) #start at 1 so no empty arrays
            random_add = random.sample(list(hits_hits),k)
            hit_array.append(random_add) #appends as arrays, explode twice later to remove this formatting
        else:
            ndrop = randrange(0,len(hit_array),1)
            k = randrange(1,10) # again start at 1 so no empty arrays, maybe fix later
            random_add = random.sample(list(hits_hits),k)
            hit_array.append(random_add)
        if ndrop >= len(hit_array):
            print('fail') #makes sure no empty arrays
        #dataframe['ndrop'] = ndrop   (optional)
        hit_array.pop(ndrop)

    truth_copy = truth_copy.explode('hit_id') 
    truth_copy = truth_copy.explode('hit_id')
    truth_copy = truth_copy.rename(columns={'particle_id':'track_id'},inplace=False)
    return truth_copy
final_fakes = changingHits(sorted_hits,blue_hitsdf) #53478 length              ** This is submission file

#idk = final_fakes['hit_id']
#blue_truthdf2 = blue_truthdf[blue_truthdf['hit_id'].isin(idk)]

print(sorted_hits)
print(final_fakes)


#test files, mainly **ignore this**
#truth_copy1 = df_truth.copy()
#truth_copy1.rename(columns={"particle_id":"track_id"},inplace=True)
#random_truthfile = pandas.read_csv(path + '/event000001000-truth.csv')
#df_truth2 = pandas.DataFrame(data=random_truthfile)
#df_truth2.rename(columns={"particle_id":"track_id"},inplace=True)

################################################################### pre-written scoring

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


    ##EDIT: NORMALIZED
    tracks['major_nhits'] /= tracks['major_nhits'].sum()
    tracks['nhits'] /= tracks['nhits'].sum()
    tracks['major_particle_nhits'] /= tracks['major_particle_nhits'].sum()
    tracks['major_weight'] /= tracks['major_weight'].sum()

    purity_rec = numpy.true_divide(tracks['major_nhits'], tracks['nhits'])
    purity_maj = numpy.true_divide(tracks['major_nhits'], tracks['major_particle_nhits'])
    good_track = (0.5 < purity_rec) & (0.5 < purity_maj)
    return tracks['major_weight'][good_track].sum() #comment out/fix so score is per track not per event

#print(score_event(df_truth,truth_copy1))
#print(score_event(sorted_hits,final_fakes))

#############################################################

#print(score_event(df_truth,final_fakes))












def oneFakeTrack(dataframe):
    random_track_id = random.choice(dataframe['track_id'])
    track_interest = []
    for track in dataframe:
        if dataframe['track_id'] == random_track_id:
            track_interest.append(dataframe['hit_id'])
            print(track_interest)

#print(blue_truthdf)
#print(final_fakes)
#print(oneFakeTrack(final_fakes))

def repeats(dataframe):
    hit_id = dataframe['track_id']
    unique = numpy.unique(hit_id)
    for id in hit_id:
        #print(unique)
        if id not in unique:
            print(hit_id)

#print(len(set(blue_truthdf['particle_id']))) #only 6760/47134 unique particle ids 
#print(repeats(final_fakes))

def remove_reps(truth,submission):
    pids = truth['particle_id']
    trids = submission['track_id']
    for particle in pids:
        if particle in trids:
            df_part = truth[truth['particle_id']]
            truth = truth.append([df_part],ignore_index=True)
    print(truth)

#print(remove_reps(blue_truthdf,final_fakes))
