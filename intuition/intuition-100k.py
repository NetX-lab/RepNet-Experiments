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

synfile = "timerepsynsend.dat"
repfile = "timerepflowsend.dat"
sinfile = "timetcpsend.dat"

sin = np.loadtxt(sinfile)
rep = np.loadtxt(repfile)
syn = np.loadtxt(synfile)

len1 = len(sin)
len2 = len(rep)
len3 = len(syn)

x = np.arange(0.1, 100, 0.1)
p1 = []
p2 = []
p3 = []
xlab = []
for i in x:
  p1.append(getpt(sin, i))
  p2.append(getpt(rep, i))
  p3.append(getpt(syn, i))
  xlab.append(i)

plt.figure(figsize=(6,6))
plt.plot(p1, xlab, 'b-', label="TCP", linewidth=3, markersize=4)
plt.plot(p2, xlab, 'y-', label="RepFlow", linewidth=3, markersize=4)
plt.plot(p3, xlab, 'r-', label="RepSYN", linewidth=3, markersize=4)
plt.legend(loc='lower right', fontsize='medium')
#plt.yscale('log')
#plt.xscale('log')
plt.ylabel('(%)')
plt.xlabel('Flow Completion Time (ms)')
#plt.yticks([0.1, 0.2, 0.5, 1, 2, 4, 8, 16, 32, 64], [99.9, 99.8, 99.5, 99, 98, 96, 92, 84, 68, 36])
#plt.xticks([20, 50, 100, 200, 500, 1000], [20, 50, 100, 200, 500, 1000])

#plt.xlim([94, 1300])
# plt.axis('tight')
plt.ylim([0,100])
plt.tight_layout(rect=(0,0,1,1))
plt.grid()

plt.savefig('./intuition-100k.pdf', format='pdf')
plt.show()
