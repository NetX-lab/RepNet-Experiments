#!/bin/bash

for i in {1..8}
do
  LOAD=$1
  TIME=$((LOAD / i))
  sudo python run_experiment.py $TIME 0."$i"
  sudo ./gather.sh
  sudo chmod 666 sin.txt
  mv sin.txt "$i"sin.dat
  sudo chmod 666 rep.txt
  mv rep.txt "$i"rep.dat
  sudo chmod 666 repsyn.txt
  mv repsyn.txt "$i"syn.dat
  echo "done running load 0.$i"
  sleep 2
done
