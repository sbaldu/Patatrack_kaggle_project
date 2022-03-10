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

# Read the dataframes from the csv files
hits_ = pd.read_csv('~/Documents/Courses/Thesis/train_3/event000004590-hits.csv')
particles_ = pd.read_csv('~/Documents/Courses/Thesis/train_3/event000004590-particles.csv')
truth_ = pd.read_csv('~/Documents/Courses/Thesis/train_3/event000004590-truth.csv')

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

# Define a list of colours for the different tracks
colours = ['red','blue','yellow','orange','green','aqua','beige','black','chartreuse','chocolate','coral','cyan',
'crimson','gold','fuchsia','green','salmon','lime','navy','khaki','lavender','magenta','olive','wheat','ivory',
'grey','maroon','lightblue','plum','sienna','silver','teal','violet','pink','orchid','torquoise','tan','indigo',
'red','blue','yellow','orange','green','aqua','beige','black','chartreuse','chocolate','coral','cyan',
'crimson','gold','fuchsia','green','salmon','lime','navy','khaki','lavender','magenta','olive','wheat','ivory',
'grey','maroon','lightblue','plum','sienna','silver','teal','violet','pink','orchid','torquoise','tan','indigo',
'red','blue','yellow','orange','green','aqua','beige','black','chartreuse','chocolate','coral','cyan',
'crimson','gold','fuchsia','green','salmon','lime','navy','khaki','lavender','magenta','olive','wheat','ivory',
'grey','maroon','lightblue','plum','sienna','silver','teal','violet','pink','orchid','torquoise','tan','indigo',
'red','blue','yellow','orange','green','aqua','beige','black','chartreuse','chocolate','coral','cyan',
'crimson','gold','fuchsia','green','salmon','lime','navy','khaki','lavender','magenta','olive','wheat','ivory',
'grey','maroon','lightblue','plum','sienna','silver','teal','violet','pink','orchid','torquoise','tan','indigo',
'red','blue','yellow','orange','green','aqua','beige','black','chartreuse','chocolate','coral','cyan',
'crimson','gold','fuchsia','green','salmon','lime','navy','khaki','lavender','magenta','olive','wheat','ivory',
'grey','maroon','lightblue','plum','sienna','silver','teal','violet','pink','orchid','torquoise','tan','indigo',
'red','blue','yellow','orange','green','aqua','beige','black','chartreuse','chocolate','coral','cyan',
'crimson','gold','fuchsia','green','salmon','lime','navy','khaki','lavender','magenta','olive','wheat','ivory',
'grey','maroon','lightblue','plum','sienna','silver','teal','violet','pink','orchid','torquoise','tan','indigo']
print(len(colours))

def hit_index(hit_id):                              # Define a function that takes an hit_id 
    hits_list = hits_['hit_id'].values.tolist()     # and returns the index in the column series
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
    ax.scatter(z_,x_,y_, color=colours[colour_index], label=str(par_ids[colour_index]))
    colour_index += 1

#ax.legend()
ax.set_title("Visualization of the first 5 particles")
plt.xlabel("z")
plt.ylabel("x")
ax.set_zlabel("y")
plt.show()

# Read the dataframes from the first 10 events
hits_ten_events = []
particles_ten_events = []
cells_ten_events = []
truth_ten_events = []

for i in range(10):
    name_h = '~/Documents/Courses/Thesis/train_3/event00000459' + str(i) +'-hits.csv'
    name_p = '~/Documents/Courses/Thesis/train_3/event00000459' + str(i) +'-particles.csv'
    name_c = '~/Documents/Courses/Thesis/train_3/event00000459' + str(i) +'-cells.csv'
    name_t = '~/Documents/Courses/Thesis/train_3/event00000459' + str(i) +'-truth.csv'

    hits_ten_events.append(pd.read_csv(name_h))     # Lists of DataFrames
    particles_ten_events.append(pd.read_csv(name_p))
    cells_ten_events.append(pd.read_csv(name_c))
    truth_ten_events.append(pd.read_csv(name_t))

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

maxLayerId = 0
maxVolumeId = 0

files = glob.glob('/home/simonb/Documents/Courses/Thesis/train_3/event00000*-hits.csv')
"""
for file in files:
    ev = pd.read_csv(file)
    ev_lay_col = ev['layer_id'].values.tolist()
    ev_vol_col = ev['volume_id'].values.tolist()
    length_= len(ev_lay_col)

    for i in range(length_):
        maxLayerId = max(maxLayerId, ev_lay_col[i])
        maxVolumeId = max(maxVolumeId, ev_vol_col[i])
#print(maxLayerId)      it returns 14 

def layerGlobalIndex(volume,layer):
    return (volume-7)*(maxLayerId + 1) + layer
"""
maxLayerId = 14
def layerGlobalIndex(volume,layer):
    return (volume-7)*(maxLayerId + 1) + layer

# Take all the hits and assign an index to each of them. Then write all of this in on a file

#radius_list = []
#z_list = []
#index_list = []

fig = plt.figure()
#ax = fig.add_subplot(111, projection='2d')
ev = pd.read_csv(files[10])
ev_hitid_col = ev['hit_id'].values.tolist()
ev_lay_col = ev['layer_id'].values.tolist()
ev_vol_col = ev['volume_id'].values.tolist()
ev_x_col = ev['x'].values.tolist()
ev_y_col = ev['y'].values.tolist()
ev_z_col = ev['z'].values.tolist()
length_= len(ev_lay_col)
 
#for i in range(length_):
for i in range(10000):
    #radius_list.append(np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2))
    #z_list.append(ev_z_col[i])
    #index_list.append(layerGlobalIndex(ev_lay_col[i],ev_vol_col[i]))
    radius_ = np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2)
    z_value = ev_z_col[i]
    index_value = layerGlobalIndex(ev_lay_col[i],ev_vol_col[i])
    print(i)
    plt.scatter(z_value,radius_, color=colours[index_value])
"""
for file in files:
    ev = pd.read_csv(file)

    ev_hitid_col = ev['hit_id'].values.tolist()
    ev_lay_col = ev['layer_id'].values.tolist()
    ev_vol_col = ev['volume_id'].values.tolist()
    ev_x_col = ev['x'].values.tolist()
    ev_y_col = ev['y'].values.tolist()
    ev_z_col = ev['z'].values.tolist()
    length_= len(ev_lay_col)
    print(files.index(file))
 
    for i in range(length_):
        #radius_list.append(np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2))
        #z_list.append(ev_z_col[i])
        #index_list.append(layerGlobalIndex(ev_lay_col[i],ev_vol_col[i]))
        radius_ = np.sqrt(ev_x_col[i]**2 + ev_y_col[i]**2)
        z_value = ev_z_col[i]
        index_value = layerGlobalIndex(ev_lay_col[i],ev_vol_col[i])

        plt.scatter(z_value,radius_, color=colours[index_value])
"""
#plt.scatter(z_list,radius_list_)
#ax.legend()
#ax.set_title("Hits on layer " + str(lay_) + " and volume " + str(vol_))
plt.xlabel("z")
plt.ylabel("r")
#plt.xlim(-3000,3000)
plt.show()
#pos_and_ind = pd.concat([radius_list,z_list,index_list],axis=1)
#p_a_i_sorted = pos_and_ind.sort_values(by=2,ascending=True)


# Write hits per layer on a .dat file, so that ROOT can read it
def write_to_dat(vol_,lay_):
    open_file = open('test.dat', 'a')
    index_list = sort_layer(vol_,lay_)

    for index_ in index_list:
        open_file.write(str(hits_['x'].values.tolist()[index_]) + '\t' 
        + str(hits_['y'].values.tolist()[index_]) + '\t' 
        + str(hits_['z'].values.tolist()[index_]) + '\t' + str(index(vol_,lay_)) +'\n')
    open_file.close()

"""
for comb in list__:
    write_to_dat(comb[0],comb[1])
"""

def write_to_csv(vol_,lay_):
    open_file = open('test.csv', 'a')
    index_list = sort_layer(vol_,lay_)

    open_file.write('x,y,z')
    for index_ in index_list:
        open_file.write(str(hits_['x'].values.tolist()[index_]) + ',' 
        + str(hits_['y'].values.tolist()[index_]) + ',' 
        + str(hits_['z'].values.tolist()[index_]) + '\n')
    open_file.close()

"""
# Create the "Hits dataframe"
hits_df = hits_.loc[:,['hit_id', 'x', 'y', 'z']]

# Create the "Particle dataframe"
par_df = pd.concat([particles_['particle_id'],
    particles_['px'],particles_['py'],particles_['pz']],axis=1)
"""
"""
    # Solution 1
def max_layer(volume):
    if (volume in volumes_col) == False:
        return 0
    else:
        indexes = sort_volume(volume)
        layers_ = []

        for index in indexes:
            layers_.append(layer_col[index])
        max_ = max(layers_)
        return max_
def index(vol_,lay_):
    index_ = 0
    for i in range(vol_):
        index_ += max_layer(i)
    index_ += lay_
    return index_

    # Solution 2
length = len(layer_col)
list_ = []
    
for i in range(length):
    list_.append(volumes_col[i] + layer_col[i]/100)
list_ = list(set(list_))
list_.sort()
list__ = []
for element in list_:
    element = str(element)
    split_ = element.split(sep='.')
    if len(split_[1]) == 1:
        list__.append([int(split_[0]),int(split_[1])*10])
    else:
        list__.append([int(split_[0]),int(split_[1])])

def indexing(v_,l_):
    index = 0
    
    
    for i in range(len(list__)):
        if list__[i]==[v_,l_]:
            break
        if list__[i]!=[v_,l_]:
            index += 1

    return index
"""