#!/bin/bash

rm time*

for i in {1..10000}
do
  node ./tcpsend.js >> timetcpsend.dat
  node ./repsynsend.js >> timerepsynsend.dat
  node ./repflowsend.js >> timerepflowsend.dat
done
