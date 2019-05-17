
while /bin/true ; do
  date '+%s'
  dmesg | grep EDAC >> $(hostname)_joshtest.txt
  sleep 30
done
