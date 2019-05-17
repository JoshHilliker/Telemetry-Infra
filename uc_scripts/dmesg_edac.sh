
while /bin/true ; do
   dmesg | grep EDAC >> $(hostname)_test.txt
  sleep 30
done
