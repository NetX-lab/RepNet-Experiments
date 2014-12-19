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

rtt = ['ping2.trace', 'ping3.trace', 'ping4.trace']
rttdata = []
for i in range(3):
  rttdata.append(np.loadtxt(rtt[i], dtype='str'))
  rttdata[i] = rttdata[i][:, 6]
  rttdata[i] = [float(j[5:]) for j in rttdata[i]]
  rttdata[i] = np.array(rttdata[i][3000:5000])

x = np.arange(0, 200, 0.1)

plt.figure(1, figsize=(7,5.5))
plt.subplot(311)
plt.plot(x, rttdata[0], 'b-', linewidth=1)
plt.ylim([0.1, 5])
plt.tick_params(\
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
plt.ylabel('RTT (ms)')

plt.subplot(312)
plt.plot(x, rttdata[1], 'r-', linewidth=1)
plt.ylim([0.1, 5])
plt.tick_params(\
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
plt.ylabel('RTT (ms)')

plt.subplot(313)
plt.plot(x, rttdata[2], 'y-', linewidth=1)
plt.ylim([0.1, 5])
#plt.legend(loc='lower right', fontsize='medium')
#plt.yscale('log')
#plt.xscale('log')
plt.figure(1)
plt.ylabel('RTT (ms)')
plt.xlabel('Elapsed Time (s)')
#plt.yticks([0.1, 0.2, 0.5, 1, 2, 4, 8, 16, 32, 64], [99.9, 99.8, 99.5, 99, 98, 96, 92, 84, 68, 36])
#plt.xticks([20, 50, 100, 200, 500, 1000], [20, 50, 100, 200, 500, 1000])
#plt.yticks([0, 33.3, 66.7, 88.9, 100], [0, 33.3, 66.7, 88.9, 100])

#plt.xlim([94, 1300])
# plt.axis('tight')
#plt.tight_layout(rect=(0,0,1,1))
#plt.grid()

plt.savefig('./RTTfluctuation.pdf', format='pdf')
plt.show()
