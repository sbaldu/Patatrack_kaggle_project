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


##Reading in files + pulling important colns

###read in truth, just take pid & hid
truth = pd.read_csv('/Users/pfudolig/patatrack/trackml-library-master/trackml/train_1/event000001884-truth.csv')
df_truth = pd.DataFrame(data=truth.loc[:,["particle_id","hit_id"]])
#print(df_truth.head(5))


###sorting hits per pid
grouped_df = df_truth.groupby("particle_id")
grouped_lists = grouped_df["hit_id"].apply(list)
grouped_lists = grouped_lists.reset_index()
#print(grouped_lists)

###making sorted hits into dataframe
sorted = pd.DataFrame(data=grouped_lists)
#print(sorted.head(7))
#attach the column hit_id to other transverse

###read in particles
ev_particles = pd.read_csv('/Users/pfudolig/patatrack/trackml-library-master/trackml/train_1/event000001884-particles.csv')
df_part = pd.DataFrame(data=ev_particles)
#print(ev_particles.head(3))

###just what we want
pdf_new = df_part[['particle_id','q','nhits']].copy()
#print(pdf_new.head(3))

###read in hits
hitsin3d = pd.read_csv('/Users/pfudolig/patatrack/trackml-library-master/trackml/train_1/event000001884-hits.csv')
df_hits = pd.DataFrame(data=hitsin3d)
#print(hitsin3d.head(3))







##Task 1: Create a single dataframe containing all particles + hits positions

#combine for all colns we want, a little convoluted

#df_truth
#pdf_new

### all columns wanted, not sorted
ptcombo = df_truth.join(pdf_new.set_index('particle_id'), on='particle_id')

### all columns wanted, sorted
allcombo = df_hits.join(ptcombo.set_index('hit_id'), on='hit_id')

### group by hits per pid
grouped_df = allcombo.groupby("particle_id")
grouped_lists = grouped_df["hit_id"].apply(list)
grouped_lists = grouped_lists.reset_index()
single = pd.DataFrame(data=grouped_lists)

### 
rest = allcombo[['x','y','z','volume_id','layer_id','module_id','particle_id','q','nhits']].copy()
both = single.join(rest.set_index('particle_id'), on='particle_id')
#both.head(3)

### just pids, hids, & positions
### really all we wanted, idk why i took all those extra steps
single = pd.DataFrame(data=both.loc[:,["particle_id","hit_id","x","y","z"]])
#print(single.head(3))







##Task 2: Create a visualization function that takes particleId and visualizes only the hits belonging to that particle

##ask for pid and take it in
#pid = input('type the particle id: ')
#pidint = int(pid)

##take
row = sorted.index[sorted['particle_id'] == pidint].tolist()
row = row[0]

##empty arrays to fill
xdata = []
ydata = []
zdata = []
hitslist = sorted['hit_id'][row]
for i in range(len(hitslist)): #loop for number of elements in the list for the hit_id for that row aka particle id 
    xdata.append(df_hits['x'][hitslist[i]-1])
    ydata.append(df_hits['y'][hitslist[i]-1])
    zdata.append(df_hits['z'][hitslist[i]-1])
    
##plot
ax = plt.axes(projection='3d')
ax.scatter3D(zdata,xdata,ydata)    #edit: now rotated
plt.title("Single track of particle " + pid)
ax.set_xlabel('Z-axis')
ax.set_ylabel('X-axis')
ax.set_zlabel('Y-axis')
##plt.savefig(mypath + "Single-Particle-Track-" + pid + ".png")

#Simone method

#display first 5 (or any 5?) particles and their hits

#take
pids = df_truth['particle_id'].values.tolist()
vols = df_hits['volume_id'].values.tolist()
layers = df_hits['layer_id'].values.tolist()
x = df_hits['x'].values.tolist()
y = df_hits['y'].values.tolist()
z = df_hits['z'].values.tolist()

colours = ['red','blue','yellow','orange','green']

def hit_index(hit_id):                              # Define a function that takes an hit_id 
    hits_list = df_hits['hit_id'].values.tolist()     # and returns the index in the column series
    index = hits_list.index(hit_id)
    return index

def par_index_t(par_id):
    index = par_list_t.index(par_id)
    return index

# Define the function for the visualization of hits belonging to a particle
def sort_hits(particle_id):
    list_hits = []

    for i in range(df_truth['particle_id'].size):
        if df_truth['particle_id'][i] == particle_id:
            list_hits.append(df_truth['hit_id'][i])
            
    return list_hits
def vis_particle(particle_id):
    x_hit_vis = []
    y_hit_vis = []
    z_hit_vis = []
    for hit in sort_hits(particle_id):
        index = hit_index(hit)
        x_hit_vis.append(df_hits['x'][index])
        y_hit_vis.append(df_hits['y'][index])
        z_hit_vis.append(df_hits['z'][index])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(z_hit_vis,x_hit_vis,y_hit_vis)
    plt.title('Single Particle Track')
    ax.set_xlabel('Z-axis')
    ax.set_ylabel('X-axis')
    ax.set_zlabel('Y-axis')
    plt.show()
    #plt.savefig(mypath + "Single-Particle-Track_simone.png")


#Simone Method

# Visualize the first 5 particles
par_ids = [df_part['particle_id'][i] for i in range(5)]
par_hits = [sort_hits(par_ids[i]) for i in range(5)]    # For some reason the third particle has no hits
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colour_index = 0

for i in par_hits:
    x_ = []
    y_ = []
    z_ = []
    for j in i:
        x_.append(df_hits['x'][hit_index(j)])
        y_.append(df_hits['y'][hit_index(j)])
        z_.append(df_hits['z'][hit_index(j)])
    ax.scatter(z_,x_,y_, color=colours[colour_index], label=str(par_ids[colour_index]))
    colour_index += 1

#ax.legend()
ax.set_title("Visualization of the first 5 particles")
plt.xlabel("z")
plt.ylabel("x")
ax.set_zlabel("y")
plt.show()
#plt.savefig(mypath + "First-5-particles_simone.png")








##Task 3: From the hits dataframe, group hits by volume and layer id create a visualization function that displays only hits on
##the same detector layer

#sorting hits per vol_id

grouped_volhits = df_hits.groupby("volume_id")
vollist = grouped_volhits["hit_id"].apply(list)
vollist = vollist.reset_index()
#print(vollist)

df_volid = pd.DataFrame(data=vollist)
#print(df_volid)

#Visualizes all hits in that Volume 

#ask for volume id and take it in
volid = input('type the volume id: ')
volidint = int(volid)

#take
row = df_volid.index[df_volid['volume_id'] == volidint].tolist()
row = row[0]

#empty arrays to fill
xdata = []
ydata = []
zdata = []
vidslist = df_volid['hit_id'][row]
for i in range(len(vidslist)):
    xdata.append(df_hits['x'][vidslist[i]-1])
    ydata.append(df_hits['y'][vidslist[i]-1])
    zdata.append(df_hits['z'][vidslist[i]-1])
    
#plot
fig=plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(xdata,ydata,zdata)
plt.title("All hits in volume " + volid)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.show()
#plt.savefig(mypath + "All-hits-vol-" + volid + ".png")

#edit: try rotated
fig=plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(zdata,xdata,ydata)
plt.title("All hits in volume " + volid + " (rotated)")
ax.set_xlabel('Z-axis')
ax.set_ylabel('X-axis')
ax.set_zlabel('Y-axis')
plt.show()
#plt.savefig(mypath + "All-hits-vol-" + volid + "_rotated.png")

#sorting hits per layer_id

grouped_layhits = df_hits.groupby("layer_id")
laylist = grouped_layhits["hit_id"].apply(list)
laylist = laylist.reset_index()
#print(laylist)

df_layerid = pd.DataFrame(data=laylist)
#print(df_layerid)

#Visualizes all hits on that layer

#ask for layer id and take it in
lid = input('type the layer id: ')
lidint = int(lid)

#take
row = df_layerid.index[df_layerid['layer_id'] == lidint].tolist()
row = row[0]

#empty arrays to fill
xdata = []
ydata = []
zdata = []
lidslist = df_layerid['hit_id'][row]
for i in range(len(lidslist)):
    xdata.append(df_hits['x'][lidslist[i]-1])
    ydata.append(df_hits['y'][lidslist[i]-1])
    zdata.append(df_hits['z'][lidslist[i]-1])
    
#plot
fig=plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(xdata,ydata,zdata)
plt.title("All hits on layer " + lid)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.show()
#plt.savefig(mypath + "All-hits-layer-" + lid + ".png")

#plot rotated
fig=plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(zdata,xdata,ydata)
plt.title("All hits on layer " + lid)
ax.set_xlabel('Z-axis')
ax.set_ylabel('X-axis')
ax.set_zlabel('Y-axis')
plt.show()
#plt.savefig(mypath + "All-hits-layer-" + lid + "_rotated.png")

#Simone method

# Group hits by volume and layer, then visualize them
volumes_ = list(set(vols))      #Removes all the duplicates from the list

def sort_volume(volume):
    index_list = []

    for i in range(len(vols)):
        if vols[i]==volume:
            index_list.append(i)
    return index_list

vol_dict = {}
for vol in volumes_:
    vol_dict[str(vol)] = sort_volume(vol)
def sort_layer(vol_,lay_):
    index_list = []

    for i in range(len(layers)):
        if layers[i]==lay_ and vols[i]==vol_:
            index_list.append(i)
    return index_list
def vis_same_layer(vol_,lay_):
    index_list = sort_layer(vol_,lay_)
    x_ = []
    y_ = []
    z_ = []
    label_ = "layer " + str(lay_) + ', volume ' + str(vol_)

    for index_ in index_list:
        x_.append(x[index_])
        y_.append(y[index_])
        z_.append(z[index_])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(z_,x_,y_, label=label_)
    ax.legend()
    ax.set_title("Hits on layer " + str(lay_) + " and volume " + str(vol_) + (" (rotated)"))
    plt.xlabel("z")
    plt.ylabel("x")
    ax.set_zlabel("y")
    plt.show()
    #plt.savefig(mypath + "All-hits-layer-" + str(lay_) + "-vol-" + str(vol_) + "_rotated.png")
#vis_same_layer(7,2)