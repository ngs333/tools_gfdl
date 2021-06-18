#!/bin/bash

etext="teardown"
ctext="Zteardown"

for i in $(find .  -regex ".*\.\(sh\|csh\)$");	 
do
    if (grep -q "$etext" $i) then
       echo " on $i"
      sed -i "s/$etext/$ctext/gi" $i
    fi
done

etext="rm -rf"
ctext="#rm -rf"

for i in $(find .  -regex ".*\.\(sh\|csh\)$");	 
do
    if (grep -q "$etext" $i) then
       echo " on $i"
      sed -i "s/$etext/$ctext/gi" $i
    fi
done
