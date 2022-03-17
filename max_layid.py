import glob

path = '/home/simonb/Documents/Thesis/'
hit_files = glob.glob(path+'train_3/event00000*-hits.csv')

maxLayerId = 0
maxVolumeId = 0

for file in files:
    ev = pd.read_csv(file)
    ev_lay_col = ev['layer_id'].values.tolist()
    ev_vol_col = ev['volume_id'].values.tolist()
    length_= len(ev_lay_col)

    for i in range(length_):
        maxLayerId = max(maxLayerId, ev_lay_col[i])
        maxVolumeId = max(maxVolumeId, ev_vol_col[i])
print(maxLayerId)