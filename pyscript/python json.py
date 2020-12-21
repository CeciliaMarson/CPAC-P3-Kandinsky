#%%
import json
import numpy as np


array=np.array([[100,23,55],[20,9,120]])


arr=[]

for c in array:
    x={"R":int(c[0]),
    "G":int(c[1]),
    "B":int(c[2]),
    }
    arr.append(x)

print(arr)
with open('string.json', 'w') as outfile:
    json.dump(arr, outfile)
# %%
