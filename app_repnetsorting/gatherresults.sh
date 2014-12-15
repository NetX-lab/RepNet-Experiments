#!/bin/bash

touch time.dat
for i in {1..12}
do
  cat time`echo $i`.dat >> time.dat
  rm time`echo $i`.dat
done
