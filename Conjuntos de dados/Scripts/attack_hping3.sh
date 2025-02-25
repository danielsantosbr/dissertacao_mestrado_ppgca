#!/bin/bash

for i in {1..21}; do
  for j in {1..21}; do
    if [ $i -eq $j ]; then
      continue
    fi
    hping3 -1 --flood -a 10.0.0.${i} 10.0.0.${j} &
    hping3 -S --flood -a 10.0.0.${i} 10.0.0.${j} &
    hping3 -2 --flood -a 10.0.0.${i} 10.0.0.${j} &
  done
done
