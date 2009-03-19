#!/usr/bin/env bash

for D_s in 0.001 0.005 0.01 0.02 0.1; do
  for D_a in 0.1 0.2 0.25 0.3; do
    for D_b in 0.02 0.03 0.05 0.2; do
      for beta_i in 12; do
        ./PyMorphogenesis.py -r -p images -s $D_s -a $D_a -b $D_b -d $beta_i
      done
    done
  done
done
