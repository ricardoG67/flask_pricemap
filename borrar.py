import numpy as np

price = np.array([[2.6, 2.6], [1.3, 1.5], [4, 5], []])

mins=[]
maxs=[]

for i in price:
    if len(i)!=0:
        mins.append(np.min(i))
        maxs.append(np.max(i))
    else:
        mins.append(None)
        maxs.append(None)

print(maxs)

