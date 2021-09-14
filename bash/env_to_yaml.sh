#!/bin/bash
filename=$1
n=1
while read line; do
if [[ $line == *"="* ]]; then
  echo ${line/=/: }
fi
n=$((n+1))
done < $filename
