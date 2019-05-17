EVENTS="\

imc/event=0x04,umask=0x03,name='UNC_M_CAS_COUNT.RD'/ \

imc/event=0x04,umask=0x0c,name='UNC_M_CAS_COUNT.WR'/ \

cpu/event=0xb0,umask=0x10,name='OFFCORE_REQUESTS.L3_MISS_DEMAND_DATA_RD'/
"


PERF_EVENTS=""
for EVENT in $EVENTS ; do
  PERF_EVENTS="${PERF_EVENTS} -e \"${EVENT}\""
done
perf stat ${PERF_EVENTS} -I10000 -o $(hostname)_perfout.txt 

