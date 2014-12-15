# Random Number (int ranging from 0 to 6000) Generator
# Usage: python randomgenerator.py number

import random
import sys

f = open('./numbers.dat', 'w')
if len(sys.argv) == 2:
    num = int(sys.argv[1])
else:
    num = 10000

for i in range(0, num):
    f.writelines(str(random.randrange(0, 6000)) + '\n')

f.close();
