#!/usr/bin/python

# Numpy is a library for handling arrays (like data points)
import numpy as np
import math

# Pyplot is a module within the matplotlib library for plotting
import matplotlib.pylab as plt
import matplotlib

font = {'family' : 'sans',
        #'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)

def getpt(data, percentile):
    return np.percentile(data, percentile)

mat = np.zeros((3, 8))
for i in range(1, 9):
    sinfile = str(i) + "sin.dat"
    repfile = str(i) + "rep.dat"
    synfile = str(i) + "syn.dat"

    sin = np.loadtxt(sinfile)
    rep = np.loadtxt(repfile)
    syn = np.loadtxt(synfile)

    len1 = len(sin[:,0])
    len2 = len(rep[:,0])
    len3 = len(syn[:,0])

    single = sin[:,0] #- 6.82
    repflow = rep[:,0] #- 7.12
    repsyn = syn[:,0] #- 7.12
    single = single[single < 400]
    repflow = repflow[repflow < 400]
    repsyn = repsyn[repsyn < 400]

    mat[0, i-1] = getpt(single, 99) 
    mat[1, i-1] = getpt(repflow, 99)
    mat[2, i-1] = getpt(repsyn, 99)
    #print np.average(single), np.average(repflow), np.average(repsyn)
    #print getpt(single, 99), getpt(repflow, 99), getpt(repsyn, 99)
    #print getpt(single, 99.9), getpt(repflow, 99.9), getpt(repsyn, 99.9)

plt.figure(figsize=(5,4))

load = np.arange(0.1, 0.9, 0.1)
plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], \
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
plt.bar(load-0.039, mat[0, :], 0.026, color='0.35', hatch='x', label="TCP")
plt.bar(load-0.013, mat[1, :], 0.026, color='0.65', hatch='.', label="RepFlow")
plt.bar(load+0.013, mat[2, :], 0.026, color='0.95', hatch='/', label="RepSYN")
plt.legend(loc='upper left', fontsize='medium')
#plt.yscale('log')

plt.xlabel('Average Bottleneck Traffic Load')

plt.tight_layout(rect=(0,0,1,1))
plt.grid()
plt.savefig("99-percentile.pdf", format='pdf')
plt.show()








