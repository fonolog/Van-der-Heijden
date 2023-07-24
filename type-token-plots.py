#type-token-plots.py
from matplotlib import pyplot as plt
import numpy as np

import os
testing = False
if testing: # We do not go through all files but only a selection
	#filenames = ['2005_Brouwers, Jeroen_Ts Feuilletons 7 .txt', '1959_Bomans, Godfried_Wandelingen door Rome (4ed).txt', '1973_Bomans, Godfried_Op de keper beschouwd (5ed).txt', '1979_Streekromanomnibus (Margreet, Meester, Heide).txt']#
    filenames = [ 'manon uphoff.txt', 'oek de jong.txt', 'wessel te gussinklo.txt', 'sander kollaard.txt', 'marijke schermer.txt', 'saskia de coster.txt']
else:
	filenames = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f)) if f[-4:]=='.txt']

results = []

for filename in filenames:
    print (filename)
    word_stock = set()
    tokens = 0
    types = []
    type_total = 0
    honden = 0
    with open(filename,'r') as current_file:
        for line in current_file.readlines():
            for word in line.split():
                tokens +=1
                if word in ['poes', 'poezen', 'poesje', 'poesjes', 'kat', 'katten', 'katjes', 'katje']:
                    honden +=1 
                if not word in word_stock:
                    type_total += 1
                    word_stock.add(word)
                types += [type_total]

    results += [(filename[:-4],range(tokens),types, honden)]

plt.ion()
fig = plt.figure(figsize = (10,4))
for r in results:
    p = np.poly1d(np.polyfit(r[1],r[2], 3))
    #plt.plot(r[1],r[2],label=r[0])
    plt.plot(r[1], p(r[1]), label=r[0])#+'('+str(r[3])+')')
plt.title('Δtype/token')
plt.legend()
fig.savefig('type-token.png', bbox_inches = "tight")
plt.close(fig)
plt.ioff()
print(len(results))
