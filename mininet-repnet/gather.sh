#!/bin/bash

rm sin.txt
rm repsyn.txt
rm rep.txt

for i in {0..53}
do
  cat "$i"sin.txt >> sin.txt
  cat "$i"rep.txt >> rep.txt
  cat "$i"repsyn.txt >> repsyn.txt
  rm "$i"sin.txt
  rm "$i"repsyn.txt
  rm "$i"rep.txt
done
