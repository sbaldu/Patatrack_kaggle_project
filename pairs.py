from urllib.request import parse_http_list
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.pyplot import eventplot
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

# We define a map for the indexes
index_map = {}

index_map[(7,2)] = 10
index_map[(7,4)] = 9
index_map[(7,6)] = 8
index_map[(7,8)] = 7
index_map[(7,10)] = 6
index_map[(7,12)] = 5
index_map[(7,14)] = 4
index_map[(8,2)] = 0
index_map[(8,4)] = 1
index_map[(8,6)] = 2
index_map[(8,8)] = 3
index_map[(9,2)] = 11
index_map[(9,4)] = 12
index_map[(9,6)] = 13
index_map[(9,8)] = 14
index_map[(9,10)] = 15
index_map[(9,12)] = 16
index_map[(9,14)] = 17
index_map[(12,2)] = 27
index_map[(12,4)] = 26
index_map[(12,6)] = 25
index_map[(12,8)] = 24
index_map[(12,10)] = 23
index_map[(12,12)] = 22
index_map[(13,2)] = 18
index_map[(13,4)] = 19
index_map[(13,6)] = 20
index_map[(13,8)] = 21
index_map[(14,2)] = 28
index_map[(14,4)] = 29
index_map[(14,6)] = 30
index_map[(14,8)] = 31
index_map[(14,10)] = 32
index_map[(14,12)] = 33
index_map[(16,2)] = 41
index_map[(16,4)] = 40
index_map[(16,6)] = 39
index_map[(16,8)] = 38
index_map[(16,10)] = 37
index_map[(16,12)] = 36
index_map[(17,2)] = 34
index_map[(17,4)] = 35
index_map[(18,2)] = 42
index_map[(18,4)] = 43
index_map[(18,6)] = 44
index_map[(18,8)] = 45
index_map[(18,10)] = 46
index_map[(18,12)] = 47


hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')
hit_files.sort()
par_files.sort()
truth_files.sort()

radius = []
z = []
index = []

for i in range(2):
    ev = pd.read_csv(hit_files[i])
    ev_hitid_col = ev['hit_id'].values.tolist()
    ev_lay_col = ev['layer_id'].values.tolist()
    ev_vol_col = ev['volume_id'].values.tolist()
    ev_x_col = ev['x'].values.tolist()
    ev_y_col = ev['y'].values.tolist()
    ev_z_col = ev['z'].values.tolist()
    length_= len(ev_lay_col)

    for i in range(length_):
        if (i%50) == 0:
            radius.append(np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2))
            z.append(ev_z_col[i])
            #index.append(layerGlobalIndex(ev_vol_col[i],ev_lay_col[i]))

def plotPair(r_pair_,z_pair_):
    fig = plt.figure()
    #cm = plt.cm.get_cmap('nipy_spectral')
    point1 = [1, 2]
    point2 = [3, 4]
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    #plt.scatter(z,radius,color='royalblue')
    #plt.plot([z_pair_[0],z_pair_[1]], [r_pair_[0],r_pair_[1]], 'bo', linestyle="-", color='red')
    plt.xlabel("z (mm)")
    plt.ylabel("r (mm)")
    plt.xlim(-3000,3000)
    plt.ylim(0,1100)
    plt.show() 
plotPair([0],[1])

#open_hit_file = open("test_par_hits.dat", 'w')
#open_truth_file = open("test_globalIndexes.dat", 'w') 
    
hit_df = pd.read_csv(hit_files[0])
truth_df = pd.read_csv(truth_files[0])
layer_ids = hit_df['layer_id'].values.tolist()
volume_ids = hit_df['volume_id'].values.tolist()
df_size = len(layer_ids)
indexes_list_ = []
"""
for row in range(df_size):
    indexes_list_.append(index_map[(volume_ids[row],layer_ids[row])])
    globalIndexes = pd.Series(indexes_list_)

total_df_ = pd.concat([truth_df['particle_id'],np.sqrt(hit_df['x']**2 + hit_df['y']**2),hit_df['z'],globalIndexes],axis=1)
total_df_ = total_df_.rename(columns={0:'r'})
total_df_ = total_df_.rename(columns={1:'globalIndex'})
total_df_ = total_df_.sort_values(by='particle_id',ascending=True)
par_ids_list_ = total_df_['particle_id'].values.tolist()
index_list_ = total_df_['globalIndex'].values.tolist()

total_df_size = total_df_['particle_id'].size

for i in range(total_df_size):
    if par_ids_list_[i] != 0:
        #print(par_ids_list_[i]) 
        open_hit_file.write(str(par_ids_list_[i]) + '\n')
        open_truth_file.write(str(index_list_[i]) + '\n')
    
open_hit_file.close()
open_truth_file.close() 
"""

######
# This creates the dat files used in the c++ code for all the events (it takes a couple of hours to run, so don't un-comment it)

# Save the number of hits for each event and the event ids
#hits_per_event = {}

for i in range(len(hit_files)):

    # Each file will contain the event_id in its name
    event_indentifier = hit_files[i][48:52]
    
    if event_indentifier == '6000':
        # The output files are opened
        #open_hit_file = open(path + "not_sorted/par_hits_ns" + event_indentifier + ".dat", 'w')
        #open_truth_file = open(path + "not_sorted/globalIndexes_ns" + event_indentifier + ".dat", 'w') 
        #open_x_file = open(path + "not_sorted/x_ns" + event_indentifier + ".dat", 'w')
        #open_y_file = open(path + "not_sorted/y_ns" + event_indentifier + ".dat", 'w')
        #open_z_file = open(path + "not_sorted/z_ns" + event_indentifier + ".dat", 'w')
        #open_truth_file = open(path + "not_sorted/globalIndexes_blue" + event_indentifier + ".dat", 'w')
        #open_hit_file = open(path + "not_sorted/par_hits_blue" + event_indentifier + ".dat", 'w')
        #open_x_file = open(path + "not_sorted/x_blue" + event_indentifier + ".dat", 'w')
        #open_y_file = open(path + "not_sorted/y_blue" + event_indentifier + ".dat", 'w')
        #open_z_file = open(path + "not_sorted/z_blue" + event_indentifier + ".dat", 'w')
        #open_phi_file = open(path + "not_sorted/phi_blue" + event_indentifier + ".dat", 'w')
        open_truth_file_P = open(path + "not_sorted/globalIndexes_P" + event_indentifier + ".dat", 'w')
        open_hit_file_P = open(path + "not_sorted/par_hits_P" + event_indentifier + ".dat", 'w')
        open_x_file_P = open(path + "not_sorted/x_P" + event_indentifier + ".dat", 'w')
        open_y_file_P = open(path + "not_sorted/y_P" + event_indentifier + ".dat", 'w')
        open_z_file_P = open(path + "not_sorted/z_P" + event_indentifier + ".dat", 'w')
        #open_phi_file_P = open(path + "not_sorted/phi_P" + event_indentifier + ".dat", 'w')

        # Select the df that I'll read
        hit_df = pd.read_csv('/home/simone/Documents/thesis/train_3/event000006000-hits.csv')
        truth_df = pd.read_csv('/home/simone/Documents/thesis/train_3/event000006000-truth.csv')
        par_df = pd.read_csv('/home/simone/Documents/thesis/train_3/event000006000-particles.csv')        
        layer_ids = hit_df['layer_id'].values.tolist()
        volume_ids = hit_df['volume_id'].values.tolist()

        # Create a list of all the particles whose momentum is too low to be acceptable
        p_trasv = pd.concat([np.sqrt(par_df['px']**2 + par_df['py']**2)],axis=1)
        p_Trasv = p_trasv.rename(columns={0:'pTrasv'})
        par_df = pd.concat([par_df,p_Trasv],axis=1)

        #forb_pars = []
        #for j in range(len(par_df['particle_id'].values.tolist())):
        #    if par_df['pTrasv'][j] < 2:
        #        forb_pars.append(par_df['particle_id'][j])
        #print(forb_pars)
        #print(len(forb_pars))
        #print(len(par_df['particle_id'].values.tolist()))
        #print(par_df)

        #hits_per_event[event_indentifier] = len(layer_ids)

        # Using a map I create a series that contains the global index and another one that contains the polar angle phi
        df_size = len(layer_ids)
        phi_list = []
        indexes_list_ = []
        for row in range(df_size):
            phi_list.append(np.arctan(hit_df['y'][row]/hit_df['x'][row]))
            indexes_list_.append(index_map[(volume_ids[row],layer_ids[row])])
        globalIndexes = pd.Series(indexes_list_)
        phi = pd.Series(phi_list)       

        # Create the final df and sort it
        print(len(hit_df['hit_id'].values.tolist()))
        print(len(truth_df['hit_id'].values.tolist()))
        total_df_ = pd.concat([hit_df['hit_id'],truth_df['particle_id'],np.sqrt(hit_df['x']**2 + hit_df['y']**2),hit_df['x'],hit_df['y'],hit_df['z'],globalIndexes,phi],axis=1)
        total_df_ = total_df_.rename(columns={0:'r'})
        total_df_ = total_df_.rename(columns={1:'globalIndex'})
        total_df_ = total_df_.rename(columns={2:'phi'})
        total_df_.sort_values(by=['phi'])
        print(total_df_)

        allowed_pars = []
        for j in range(len(par_df['particle_id'].values.tolist())):
            if par_df['pTrasv'][j] >= 2:
                allowed_pars.append(par_df['particle_id'][j])
        print(len(allowed_pars))
        print(len(truth_df['hit_id'].values.tolist()))

        new_df = total_df_[total_df_['particle_id'].isin(allowed_pars)]
        new_df = new_df.reset_index()
        print(new_df)

        new_df_size = len(new_df['particle_id'].values.tolist())

        for k in range(new_df_size):
            #print(k)
            if total_df_['globalIndex'][k] == 27:
                break
            else:
                #open_truth_file.write(str(new_df['globalIndex'][i]) + '\n')
                #open_x_file.write(str(hit_df['x'][i]) + '\n')
                #open_y_file.write(str(hit_df['y'][i]) + '\n')
                #open_z_file.write(str(hit_df['z'][i]) + '\n')
                #open_phi_file.write(str(int(total_df_['phi'][i])) + '\n')
                ##open_hit_file.write(str(total_df_['particle_id'][i]) + '\n')
                ##open_truth_file.write(str(total_df_['globalIndex'][i]) + '\n')
                #open_x_file.write(str(hit_df['x'][i]) + '\n')
                #open_y_file.write(str(hit_df['y'][i]) + '\n')
                #open_z_file.write(str(hit_df['z'][i]) + '\n')
                open_truth_file_P.write(str(new_df['globalIndex'][k]) + '\n')
                open_hit_file_P.write(str(new_df['particle_id'][k]) + '\n')
                open_x_file_P.write(str(new_df['x'][k]) + '\n')
                open_y_file_P.write(str(new_df['y'][k]) + '\n')
                open_z_file_P.write(str(new_df['z'][k]) + '\n')
                #open_phi_file_P.write(str(total_df_['phi'][k]) + '\n')
    
        open_truth_file_P.close()
        open_hit_file_P.close()
        open_x_file_P.close()
        open_y_file_P.close()
        open_z_file_P.close()
        #open_phi_file_P.close()
        #open_hit_file.close()
        #open_truth_file.close()  
        #open_x_file.close()
        #open_y_file.close()
        #open_z_file.close()   
        #open_truth_file.close()
        #open_x_file.close()
        #open_y_file.close()
        #open_z_file.close()
        #open_phi_file.close()
#open_hpe_file = open(path + "not_sorted/hits_per_event.csv", 'w')
#for event_identifier_ in hits_per_event:
#    open_hpe_file.write(event_identifier_ + ',' + str(hits_per_event[event_identifier_]) + '\n')
#open_hpe_file.close()
######