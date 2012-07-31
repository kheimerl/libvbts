#!/bin/sh

for i in *.wav
do
    #convert to gsm
    sox $i -r 8000 -g -c 1 $(basename $i .wav).gsm resample -ql
    #make louder
    q=$(basename $i .wav).gsm
    sox -v 6.0 $q loud.$q
    mv loud.$q $q
done