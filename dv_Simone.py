from ossaudiodev import control_labels
from re import T
from matplotlib.pyplot import eventplot
from numpy import sort, triu_indices
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.mplot3d import Axes3D
import glob

#Define the path to the csv files
path = '/home/simonb/documents/thesis/'

# Put the files into lists to read them
hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')

# Read the dataframes from the first csv file
hits_ = pd.read_csv(hit_files[0])
particles_ = pd.read_csv(par_files[0])
truth_ = pd.read_csv(truth_files[0])

print('Hits')
print(hits_)
print('Particles')
print(particles_)
print('Truth')
print(truth_)

# Convert the necessary pd.Series into lists
par_list_t = truth_['particle_id'].values.tolist()
volumes_col = hits_['volume_id'].values.tolist()
layer_col = hits_['layer_id'].values.tolist()
x_col = hits_['x'].values.tolist()
y_col = hits_['y'].values.tolist()
z_col = hits_['z'].values.tolist()

# Define the functions returning the indexes
def hit_index(hit_id):                              # Define a function that takes an hit_id and returns the index in the column series
    hits_list = hits_['hit_id'].values.tolist()     
    index = hits_list.index(hit_id)
    return index

def par_index_t(par_id):
    index = par_list_t.index(par_id)
    return index

# Define the function for the visualization of hits belonging to a particle
def sort_hits(particle_id):
    list_hits = []

    for i in range(truth_['particle_id'].size):
        if truth_['particle_id'][i] == particle_id:
            list_hits.append(truth_['hit_id'][i])
            
    return list_hits
def vis_particle(particle_id):
    x_hit_vis = []
    y_hit_vis = []
    z_hit_vis = []
    for hit in sort_hits(particle_id):
        index = hit_index(hit)
        x_hit_vis.append(hits_['x'][index])
        y_hit_vis.append(hits_['y'][index])
        z_hit_vis.append(hits_['z'][index])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(z_hit_vis,x_hit_vis,y_hit_vis)
    plt.xlabel("z")
    plt.ylabel("x")
    plt.set_zlabel("y")
    plt.show()

# Compute the trasverse momentum with the particle file
p_trasv = pd.concat([np.sqrt(particles_['px']**2 + particles_['py']**2)],axis=1)
p_Trasv = p_trasv.rename(columns={0:'pTrasv'})
print(p_Trasv)

# Sort particles in decreasing order
p_T = (p_trasv.sort_values(by=0,ascending=False)).rename(columns={0:'pTrasv'})
print(p_T)

# Visualize the first 5 particles
par_ids = [particles_['particle_id'][i] for i in range(5)]
par_hits = [sort_hits(par_ids[i]) for i in range(5)]    # For some reason the third particle has no hits
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colour_index = 0

for i in par_hits:
    x_ = []
    y_ = []
    z_ = []
    for j in i:
        x_.append(hits_['x'][hit_index(j)])
        y_.append(hits_['y'][hit_index(j)])
        z_.append(hits_['z'][hit_index(j)])
    ax.scatter(z_,x_,y_, c=[colour_index for i in range(len(x_))], label=str(par_ids[colour_index]))      # Remember to add the colour
    colour_index += 1

ax.set_title("Visualization of the first 5 particles")
plt.xlabel("z")
plt.ylabel("x")
ax.set_zlabel("y")
plt.show()

# Group hits by volume and layer, then visualize them
volumes_ = list(set(volumes_col))      #Removes all the duplicates from the list

def sort_volume(volume):
    index_list = []

    for i in range(len(volumes_col)):
        if volumes_col[i]==volume:
            index_list.append(i)
    return index_list

vol_dict = {}
for vol in volumes_:
    vol_dict[str(vol)] = sort_volume(vol)

def sort_layer(vol_,lay_):
    index_list = []

    for i in range(len(layer_col)):
        if layer_col[i]==lay_ and volumes_col[i]==vol_:
            index_list.append(i)
    return index_list
def vis_same_layer(vol_,lay_):
    index_list = sort_layer(vol_,lay_)
    x_ = []
    y_ = []
    z_ = []
    label_ = "layer " + str(lay_) + ', volume ' + str(vol_)

    for index_ in index_list:
        x_.append(x_col[index_])
        y_.append(y_col[index_])
        z_.append(z_col[index_])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(z_,x_,y_, label=label_)
    ax.legend()
    ax.set_title("Hits on layer " + str(lay_) + " and volume " + str(vol_))
    plt.xlabel("z")
    plt.ylabel("x")
    ax.set_zlabel("y")
    plt.xlim(-3000,3000)
    plt.show()

vis_same_layer(7,2)

# Define the function that introduces the new index for the detector layers
maxLayerId = 14

def layerGlobalIndex(volume,layer):
    return (volume-7)*(maxLayerId + 1) + (layer-2)

# Take all the hits and assign an index to each of them. Then write all of this in on a file

fig = plt.figure()
radius = []
z = []
index = []
for i in range(10):
    ev = pd.read_csv(hit_files[i])
    ev_hitid_col = ev['hit_id'].values.tolist()
    ev_lay_col = ev['layer_id'].values.tolist()
    ev_vol_col = ev['volume_id'].values.tolist()
    ev_x_col = ev['x'].values.tolist()
    ev_y_col = ev['y'].values.tolist()
    ev_z_col = ev['z'].values.tolist()
    length_= len(ev_lay_col)    

    for i in range(length_):
        if (i%1) == 0:
            radius.append(np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2))
            z.append(ev_z_col[i])
            index.append(layerGlobalIndex(ev_vol_col[i],ev_lay_col[i]))

cm = plt.cm.get_cmap('nipy_spectral')
plt.scatter(z,radius, c = index, cmap = cm)
plt.xlabel("z (mm)")
plt.ylabel("r (mm)")
#plt.show()


# Write hits per layer on a .dat file, so that ROOT can read it
def write_to_dat(event_):       # event_ should be the path to the file written as a string. The files list should be used for convenience
    event = pd.read_csv(event_)
    
    # Define a unique name for the file
    event_ = event_.split(sep='/')
    name = event_[6]
    name = name.split(sep='.')
    open_file = open(name[0] + '.dat', 'w')
    
    #hitid_col = event['hit_id'].values.tolist()
    lay_col = event['layer_id'].values.tolist()
    vol_col = event['volume_id'].values.tolist()
    x_col = event['x'].values.tolist()
    y_col = event['y'].values.tolist()
    z_col = event['z'].values.tolist()
    length= len(lay_col)
    list_ = []
    for i in range(length):
        list_.append(layerGlobalIndex(vol_col[i],lay_col[i]))
        open_file.write(str(layerGlobalIndex(vol_col[i],lay_col[i])) + '\n')
    print(list(set(list_)))
    open_file.close()
write_to_dat(hit_files[10])

def write_to_csv(event_):       # Same thing but it writes the data to a csv file
    event = pd.read_csv(event_)
    
    # Define a unique name for the file
    event_ = event_.split(sep='/')
    name = event_[6]
    name = name.split(sep='.')
    open_file = open(name[0] + '.csv', 'a')
    
    #hitid_col = event['hit_id'].values.tolist()
    lay_col = event['layer_id'].values.tolist()
    vol_col = event['volume_id'].values.tolist()
    x_col = event['x'].values.tolist()
    y_col = event['y'].values.tolist()
    z_col = event['z'].values.tolist()
    length= len(lay_col)

    open_file.write('x,y,z,globalIndex' + '\n')
    for i in range(length):
        open_file.write(str(x_col[i]) + ',' + str(y_col[i]) + ',' 
        + str(z_col[i]) + ',' + str(layerGlobalIndex(vol_col[i],lay_col[i])) + '\n')
    open_file.close()
#write_to_csv(hit_files[10])

#Define df containing particle_ids, hit positions and vol/lay ids
i = 2       # Right now I'm only doing it for one event. I'll add all the others later
hit_df = pd.read_csv(hit_files[i])
truth_df = pd.read_csv(truth_files[i])
new_df = pd.concat([truth_df['particle_id'],np.sqrt(hit_df['x']**2 + hit_df['y']**2)
    ,hit_df['z'],layerGlobalIndex(hit_df['volume_id'],hit_df['layer_id'])],axis=1)

new_df = new_df.rename(columns={0:'r'})
new_df = new_df.rename(columns={1:'globalIndex'})
new_df = new_df.sort_values(by='r',ascending=True)
new_df_len = 128183

print(new_df)

open_file = open("test.dat", 'w')

open_file.write('particle_id,r,z,globalIndex' + '\n')
for i in range(new_df_len):
    open_file.write(str(new_df['particle_id'].values.tolist()[i]) + ',' + str(new_df['r'].values.tolist()[i]) + ',' + str(new_df['z'].values.tolist()[i]) + ',' + str(new_df['globalIndex'].values.tolist()[i]) + '\n')
open_file.close()

"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for event in particles_ten_events:
    ev_particles = event['particle_id'].values.tolist()
    ev_particles.sort()
    for particle in ev_particles:
        if (particle in par_ids) == True:
            particle_hits = sort_hits(particle)
            x_10 = []
            y_10 = []
            z_10 = []
            for i in particle_hits:
                x_10.append(hits_['x'].values.tolist()[i])
                y_10.append(hits_['y'].values.tolist()[i])
                z_10.append(hits_['z'].values.tolist()[i])
            ax.scatter(x_10,y_10,z_10, color=colours[par_ids.index(particle)])
ax.set_title("First ten events")
plt.xlabel("x")
plt.ylabel("y")
ax.set_zlabel("z")
plt.show()
"""
"""
str(x_col[i]) + '\t' + str(y_col[i]) + '\t' 
        + str(z_col[i]) + '\t' + 
"""