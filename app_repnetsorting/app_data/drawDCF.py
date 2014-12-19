#!/usr/bin/env python

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

synfile = "time-syn.dat"
repfile = "time-rep.dat"
sinfile = "time-sin.dat"

sin = np.loadtxt(sinfile)
rep = np.loadtxt(repfile)
syn = np.loadtxt(synfile)

len1 = len(sin)
len2 = len(rep)
len3 = len(syn)

x = np.logspace(-1, 1.999, num=50)
p1 = []
p2 = []
p3 = []
xlab = []
for i in x:
  p1.append(getpt(sin, 100-i))
  p2.append(getpt(rep, 100-i))
  p3.append(getpt(syn, 100-i))
  xlab.append(i)

plt.figure(figsize=(6,4))
plt.plot(p1, xlab, 'bx-', label="TCP", linewidth=2, markersize=3)
plt.plot(p2, xlab, 'y*-', label="RepFlow", linewidth=2, markersize=3)
plt.plot(p3, xlab, 'ro-', label="RepSYN", linewidth=2, markersize=3)
plt.legend(loc='lower right', fontsize='medium')
plt.yscale('log')
#plt.xscale('log')
plt.ylabel('(%)')
plt.xlabel('Sorting Time (ms)')
plt.yticks([0.1, 0.2, 0.5, 1, 2, 4, 8, 16, 32], [99.9, 99.8, 99.5, 99, 98, 96, 92, 84, 68])
plt.xticks([100, 300, 500, 700, 900, 1100, 1300], [100, 300, 500, 700, 900, 1100, 1300])

plt.xlim([94, 1300])
# plt.axis('tight')
plt.ylim([64, 0.1])
plt.tight_layout(rect=(0,0,1,1))
plt.grid()

plt.savefig('./sorting-CDF.pdf', format='pdf')
plt.show()
