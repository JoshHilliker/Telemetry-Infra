**Infrastructure Management** - the start of exposing telemetry

These reference files are to be used for lab use only, not for production.  I would recommend pulling down the files, then modifying for your use case.   

**Files**
1.  **Collectdinstall.sh** - this will startup collectd & the code is available to run the python service to expose for browser access via IP:8888.  
2.  **Collectd.conf** - reduced version with key plugins for our use cases (NOTE: this has prerequisites for specific packages to be installed prior)  NOTE:  there is more work to be done on this configuration file to remove # to turn on plugins & specific settings.  I would recommend spending time as this will be a key config file to ensure you get the data out.   
3.  **Promehteusinstall.sh** - this will download & startup prometheus (NOTE:  to add in machines/nodes you need to update the prometheus.yml file)
4.  **Prometheus.yml** - yml file for prometheus configuration that gets pulled down from script above.  NOTE: Pending if you are using collectd_exporter you will need to change the port # to 9103.  
5.  **Prometheus.service** - service file required for service to run and gets pulled down from script above.  NOTE: if you have an issue at start of prometheus then I recommend cut/paste out this file & create a new service file.  I continue to fine tune this.  
6.  **CoreMetrics** - json file for importing into grafana to show collectd metrics with prometheus.   

**Key Telemetry reference links:**
https://github.com/andikleen/pmu-tools – PMU tool that is a PERF wrapper  
https://github.com/andikleen/mce-inject – MCE – Inject  
https://github.com/andikleen/mcelog – MCE log information  
https://github.com/intel/ipmctl/ – ipmctl for Intel® Optane™ DC Persistent Memory  
https://github.com/intel/intel-cmt-cat – Intel® Resource Director Technology (Intel® RDT) usages  
https://github.com/intel/platform-resource-manager – Workload co-location Intel® Platform Resource Manager (Intel® PRM)  
https://github.com/intel/owca/ - Orchestration aware workload collection agent  

**Blogs:**  
Know your Data Center -  https://itpeernetwork.intel.com/know-your-data-center/    
Collect or not collect -   https://itpeernetwork.intel.com/collect-or-not-collect/  
Intel tools for DC Transformation -  https://itpeernetwork.intel.com/data-center-transformation/   	
Let’s rock Telemetry - https://itpeernetwork.intel.com/from-concept-to-reality-so-are-you-ready-to-rock-on-telemetry/  
