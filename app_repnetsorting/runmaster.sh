#!/bin/bash

touch time.dat
rm ./time*.dat
rm ./temp*

killall node
node ./sortslave.js &

for i in $(seq 1 2 300)
do
  node ./sortmaster.js
  sleep 1
done

scp ./time*.dat iQua@miami.csl.toronto.edu:~/git/app_repnetsorting/
rm ./temp*
killall node
