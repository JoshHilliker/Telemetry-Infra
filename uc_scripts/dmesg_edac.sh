
while /bin/true ; do
  date '+%s'
  dmesg | grep EDAC >> $(hostname)_test.txt
  sleep 30
done
