#!/bin/bash
time=60
echo ""
echo "collecting perfstat + ipmi + dstat"
echo ""
exec python /home/otp/perf/perf-collect.py -e /home/otp/perf/events/skx_reduced_pmu.txt -t $time 2>&1 &
. /home/otp/ipmi/otp_ipmi.sh > /home/otp/ipmi/$HOSTNAME-ipmi.txt 2>&1 &
IPMI=$!
dstat -drmny --output /home/otp/dstat/dstat_metrics.csv 2>&1 &
DSTAT=$!
sleep $time
kill $IPMI
kill $DSTAT
exit
