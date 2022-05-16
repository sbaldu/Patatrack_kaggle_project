"""TrackML metric weight calculation"""

from __future__ import print_function
__authors__ = ['Moritz Kiehn']
import numpy
import math
import pandas
import csv
import glob
from pathlib import Path
from utils import decode_particle_id


#constrain the hit weights to have sum 1 & create weights dep on nhits (starting from ORDER_PROPOSAL)
def _compute_order_weight_matrix(proposal, min_hits, max_hits):
    """Compute the hit order weight matrix.

    Returns
    -------
    numpy.ndarray
        Weight matrix indexed by (nhits, ihit), i.e. the total number of
        hits in the tracks and the hit index.
    """
    w = numpy.zeros((max_hits + 1, max_hits))
    for nhits in range(min_hits, max_hits + 1):
        # scale proposal weights to the number of hits on track
        supports = numpy.arange(len(proposal)) * (nhits - 1) / (len(proposal) - 1)
        # compute normalized weights so that a full track has a sum of 1
        weights = numpy.interp(numpy.arange(nhits), supports, proposal)
        weights /= weights.sum()
        w[nhits, :nhits] = weights
    return w

ORDER_PROPOSAL = [10., 8., 6., 5., 3., 3., 3., 5., 6.]
ORDER_MIN_HITS = 4
ORDER_MAX_HITS = 20
ORDER_MATRIX = _compute_order_weight_matrix(ORDER_PROPOSAL, ORDER_MIN_HITS, ORDER_MAX_HITS)

def print_order_weight_matrix(prefix=''):
    print(prefix, 'order weight matrix (weights in percent):', sep='')
    print(prefix, 'nhits | ihit', sep='')
    print(prefix, '      |', sep='', end='')
    for i in range(len(ORDER_MATRIX[1:][0])):
        print(' {:2d}'.format(i), end='')
    print()
    print(prefix, '------+' + len(ORDER_MATRIX[1:][0]) * 3 * '-', sep='')
    for nhits, row in enumerate(ORDER_MATRIX[1:], start=1):
        print(prefix, '  {: 3d} |'.format(nhits), sep='', end='')
        for ihit in range(nhits):
            print(' {:2.0f}'.format(100 * row[ihit]), end='')
        print()


#marking which hits will be assigned weight 0 & taking care of errors
def weight_order(args):
    """Return the weight due to the hit order along the track.
    """
    ihit, nhits = args
    if nhits < ORDER_MIN_HITS:
        return 0.
    if ORDER_MAX_HITS < nhits:
        nhits = ORDER_MAX_HITS
    if ORDER_MAX_HITS <= ihit:
        print("warning long true track ihit ", ihit, " proceeding with weight zero.")
        return 0.
    if nhits <= ihit:
        raise Exception("hit index ", ihit, " is larger than total number of hits ", nhits)
    if nhits < 0:
        raise Exception("total number of hits ", nhits, " is below zero")
    if ihit < 0:
        raise Exception("hit index ", ihit, " is below zero")
    return ORDER_MATRIX[nhits, ihit]


#transverse momentum????
def weight_pt(pt, pt_inf=0.5, pt_sup=3, w_min=0.2, w_max=1.):
    """Return the transverse momentum dependent hit weight.
    """
    # lower cut just to be sure, should not happen except maybe for noise hits
    xp = [min(0.05, pt_inf), pt_inf, pt_sup]
    fp = [w_min, w_min, w_max]
    return numpy.interp(pt, xp, fp, left=0.0, right=w_max)

# particle id for noise hits
INVALID_PARTICLED_ID = 0

def weight_hits_phase1(truth, particles):
    """Compute per-hit weights for the phase 1 scoring metric.

    Hits w/ invalid particle ids, e.g. noise hits, have zero weight.

    Parameters
    ----------
    truth : pandas.DataFrame
        Truth information. Must have hit_id, particle_id, and tz columns.
    particles : pandas.DataFrame
        Particle information. Must have particle_id, vz, px, py, and nhits
        columns.

    Returns
    -------
    pandas.DataFrame
        `truth` augmented with additional columns: particle_nhits, ihit,
        weight_order, weight_pt, and weight.
    """
    # fill selected per-particle information for each hit
    selected = pandas.DataFrame({
        'particle_id': particles['particle_id'],
        'particle_vz': particles['vz'],
        'particle_nhits': particles['nhits'],
        'weight_pt': weight_pt(numpy.hypot(particles['px'], particles['py'])),
    })
    combined = pandas.merge(truth, selected,
                            how='left', on=['particle_id'],
                            validate='many_to_one')

    # fix pt weight for hits w/o associated particle
    combined['weight_pt'].fillna(0.0, inplace=True) #.fillna fills with NaN values
    # fix nhits for hits w/o associated particle
    combined['particle_nhits'].fillna(0.0, inplace=True)
    combined['particle_nhits'] = combined['particle_nhits'].astype('i4')
    # compute hit count and order using absolute distance from particle vertex
    combined['abs_dvz'] = numpy.absolute(combined['tz'] - combined['particle_vz'])
    combined['ihit'] = combined.groupby('particle_id')['abs_dvz'].rank().transform(lambda x: x - 1).fillna(0.0).astype('i4')
    # compute order-dependent weight
    combined['weight_order'] = combined[['ihit', 'particle_nhits']].apply(weight_order, axis=1)

    # compute combined weight normalized to 1
    w = combined['weight_pt'] * combined['weight_order']
    w /= w.sum()    #Paula Fudolig edit: comment out to undo normalization
    combined['weight'] = w

    # return w/o intermediate columns
    return combined.drop(columns=['particle_vz', 'abs_dvz'])

def weight_hits_phase2(truth, particles):
    """Compute per-hit weights for the phase 2 scoring metric.

    This is the phase 1 metric with an additional particle preselection, i.e.
    only a subset of the particles have a non-zero score.

    Parameters
    ----------
    truth : pandas.DataFrame
        Truth information. Must have hit_id, particle_id, and tz columns.
    particles : pandas.DataFrame
        Particle information. Must have particle_id, vz, px, py, and nhits
        columns.

    Returns
    -------
    pandas.DataFrame
        `truth` augmented with additional columns: particle_nhits, ihit,
        weight_order, weight_pt, and weight.
    """
    # fill selected per-particle information for each hit
    selected = pandas.DataFrame({
        'particle_id': particles['particle_id'],
        'particle_vz': particles['vz'],
        'particle_nhits': particles['nhits'],
        'weight_pt': weight_pt(numpy.hypot(particles['px'], particles['py'])),
    })
    selected = decode_particle_id(selected)
    combined = pandas.merge(truth, selected,
                            how='left', on=['particle_id'],
                            validate='many_to_one')

    # fix pt weight for hits w/o associated particle
    combined['weight_pt'].fillna(0.0, inplace=True)
    # fix nhits for hits w/o associated particle
    combined['particle_nhits'].fillna(0.0, inplace=True)
    combined['particle_nhits'] = combined['particle_nhits'].astype('i4')

    # compute hit count and order using absolute distance from particle vertex
    combined['abs_dvz'] = numpy.absolute(combined['tz'] - combined['particle_vz'])
    combined['ihit'] = combined.groupby('particle_id')['abs_dvz'].rank().transform(lambda x: x - 1).fillna(0.0).astype('i4')
    # compute order-dependent weight
    combined['weight_order'] = combined[['ihit', 'particle_nhits']].apply(weight_order, axis=1)

    # compute normalized combined weight w/ extra particle selection
    weight = combined['weight_pt'] * combined['weight_order']
    weight[combined['generation'] != 0] = 0
    weight /= weight.sum()
    # normalize total event weight
    combined['weight'] = weight

    # return w/o intermediate columns
    return combined.drop(columns=['particle_vz', 'abs_dvz'])

################################################## end of Moritz Kiehn code

'''Apply weighting system to train_1 data with ability to choose what sections of the detector to apply to'''

#manually input indices per volume id,layer id pair
globalIndex = {}
globalIndex[(7,2)] = 0
globalIndex[(7,4)] = 1
globalIndex[(7,6)] = 2
globalIndex[(7,8)] = 3
globalIndex[(7,10)] = 4
globalIndex[(7,12)] = 5
globalIndex[(7,14)] = 6
globalIndex[(8,2)] = 7
globalIndex[(8,4)] = 8
globalIndex[(8,6)] = 9
globalIndex[(8,8)] = 10
globalIndex[(9,2)] = 11
globalIndex[(9,4)] = 12
globalIndex[(9,6)] = 13
globalIndex[(9,8)] = 14
globalIndex[(9,10)] = 15
globalIndex[(9,12)] = 16
globalIndex[(9,14)] = 17
globalIndex[(12,2)] = 18
globalIndex[(12,4)] = 19
globalIndex[(12,6)] = 20
globalIndex[(12,8)] = 21
globalIndex[(12,10)] = 22
globalIndex[(12,12)] = 23
globalIndex[(13,2)] = 24
globalIndex[(13,4)] = 25
globalIndex[(13,6)] = 26
globalIndex[(13,8)] = 27
globalIndex[(14,2)] = 28
globalIndex[(14,4)] = 29
globalIndex[(14,6)] = 30
globalIndex[(14,8)] = 31
globalIndex[(14,10)] = 32
globalIndex[(14,12)] = 33
globalIndex[(16,2)] = 34
globalIndex[(16,4)] = 35
globalIndex[(16,6)] = 36
globalIndex[(16,8)] = 37
globalIndex[(16,10)] = 38
globalIndex[(16,12)] = 39
globalIndex[(17,2)] = 40
globalIndex[(17,4)] = 41
globalIndex[(18,2)] = 42
globalIndex[(18,4)] = 43
globalIndex[(18,6)] = 44
globalIndex[(18,8)] = 45
globalIndex[(18,10)] = 46
globalIndex[(18,12)] = 47


path = '/Users/pfudolig/patatrack/trackml-library-master/trackmlrepo/Patatrack_kaggle_project/train_1'

#Read in data
hits_file = pandas.read_csv(path + '/event000002819-hits.csv')
hits_event = pandas.DataFrame(data=hits_file)
truth_file = pandas.read_csv(path + '/event000002819-truth.csv')
truth_event = pandas.DataFrame(data=truth_file)
truth_event['layer_id'] = hits_event['layer_id']
particles_file = pandas.read_csv(path + '/event000002819-particles.csv')
particles_event = pandas.DataFrame(data=particles_file)

#Create necessary columns on data files
hits_event['global_index'] = 0
truth_event['global_index'] = 0
particles_event['global_index'] = 0
truth_event['volume_id'] = hits_event['volume_id']
particles_event['volume_id'] = hits_event['volume_id']
particles_event['layer_id'] = hits_event['layer_id']

for volume,layer in globalIndex:
    '''To add global index column to truth and particles files'''
    hits_event.loc[(hits_event['volume_id'] == volume) & (hits_event['layer_id'] == layer), 'global_index'] = globalIndex[(volume,layer)]
    truth_event.loc[(truth_event['volume_id'] == volume) & (truth_event['layer_id'] == layer), 'global_index'] = globalIndex[(volume,layer)]
    particles_event.loc[(particles_event['volume_id'] == volume) & (particles_event['layer_id'] == layer), 'global_index'] = globalIndex[(volume,layer)]

def pick_indices(indices):
    '''Given a range of global indices, display the phase 1 or phase 2 weights of each hit at these indices in the truth dataframe
       - argument must be a list'''

    narrow_hits = hits_event[hits_event['global_index'].isin(indices)]
    narrow_truth = truth_event[truth_event['global_index'].isin(indices)]
    narrow_particles = particles_event[particles_event['global_index'].isin(indices)]

    phase1 = weight_hits_phase1(narrow_truth, narrow_particles) #returns a df
    #return phase1['weight'], phase1['weight'].sum() ### for checking if normalization possible, should =/0
    return phase1, 'Sum of weights: ' + str(numpy.sum(phase1['weight']))

    #phase2 = weight_hits_phase2(narrow_truth,narrow_particles)
    #return phase2

#Define sections of detectors by color
blue_vols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17] #Sum of weights: 0.9999999999999998
    #without normalization, returns 1130.577 sum of weights
red_vols = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33] #Sum 0, w/ norm all weights are NaNs
    #without normalization, all weights are 0
green_vols = [34,35,36,37,38,39,40,41,42,43,44,45,46,47] #Sum 0, w/ norm all weights are NaNs
    #without normalization, all weights are 0
    
#print(pick_indices(red_vols))