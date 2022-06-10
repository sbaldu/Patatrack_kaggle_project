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
path = '/home/simone/Documents/thesis/'

# Put the files into lists to read them
hit_files = glob.glob(path+'train_3/event00000*-hits.csv')
par_files = glob.glob(path+'train_3/event00000*-particles.csv')
truth_files = glob.glob(path+'train_3/event00000*-truth.csv')

# Read the dataframes from the first csv file
#hits_ = pd.read_csv(hit_files[0])
hits_ = pd.read_csv(path+'train_3/event000004590-hits.csv')
particles_ = pd.read_csv(par_files[0])
truth_ = pd.read_csv(path+'train_3/event000004590-truth.csv')

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
print(sort_hits(585476747651186688))
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
    plt.xlabel("z (mm)")
    plt.ylabel("x (mm)")
    ax.set_zlabel("y (mm)")
    plt.show()
vis_particle(585476747651186688)

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
plt.xlabel("z (mm)")
plt.ylabel("x (mm)")
ax.set_zlabel("y (mm)")
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
    plt.xlabel("z (mm)")
    plt.ylabel("x (mm)")
    ax.set_zlabel("y (mm)")
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


# Write hits per layer on a .dat file, so that C++ can read it
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
    for i in range(length):
        open_file.write(str(layerGlobalIndex(vol_col[i],lay_col[i])) + '\n')
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