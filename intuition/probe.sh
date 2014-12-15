#!/bin/bash

rm time*

for i in {1..10000}
do
  node ./singleprobe.js >> timesingleprobe.dat
  node ./doubleprobe.js >> timedoubleprobe.dat
done
