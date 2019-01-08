#**Infrastructure Management** - the start of exposing telemetry

These reference files are to be used for lab use only, not for production. 

##**Files**
1.  **Collectdinstall.sh** - this will startup collectd & run the python service to expose for browser access via IP:8888
2.  **Collectd.conf** - reduced version with key plugins for our use cases (NOTE: this has prerequisites for specific packages to be installed prior) 
3.  **Promehteusinstall.sh** - this will download & startup prometheus (NOTE:  to add in machines/nodes you need to update the prometheus.yml file)
4.  **Prometheus.yml** - yml file for prometheus configuration that gets pulled down from script above
5.  **Prometheus.service** - service file required for service to run and gets pulled down from script above

