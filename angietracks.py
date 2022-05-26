import pandas as pd
import numpy as np
import random

df_truth = pd.read_csv("~/CERN/new_data_train_2.csv")
#print(df_truth.track_id)

track_ids = set(df_truth.track_id)
#print(track_ids)
#print(len(track_ids))

track_interest = track_ids.pop()
my_mask = df_truth.track_id == track_interest
#print(my_mask)

df_truth = df_truth[my_mask]

df_truth.index
index_to_drop = random.choices(df_truth.index, k=3)
#print(index_to_drop)

#print(df_truth)
df_truth2 = df_truth.drop(index = index_to_drop)
#print(df_truth2)

#checking out volume_id
df_truth_volume_table = pd.read_csv("/Users/angies/Desktop/Geneva Study Abroad/CERN/CERN_Patatrack/trackml-library/train_2/event000002820-hits.csv")

for id in index_to_drop:
    print (df_truth_volume_table[df_truth_volume_table.hit_id == id].volume_id)


