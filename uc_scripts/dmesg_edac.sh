#! /bin/bash
# purpose to do daily pull of DMESG in order to grab EDAC data (Error Detection and Correction driver) to utilize with a machine learning model for memory failure prediction. 

while /bin/true ; do
   dmesg | grep EDAC >> $(hostname)_test.txt
  sleep 8640
done
