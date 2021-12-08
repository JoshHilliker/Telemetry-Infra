**Infrastructure Management** - Drive towards a Modern Autonomous Data Center!</br>
The growing demand for cloud services means new opportunities for cloud service providers (CSPs) to generate and diversify revenue streams by delivering new services, faster. However, this puts added pressure on data center performance, power, and capacity. The new challenge for CSPs is then, how do they keep total cost of ownership (TCO) down while driving towards increasing revenue from these new services. The answer: Data center modernization and automation. By utilizing hardware and software telemetry, analytics, machine learning and ultimately AI, in your data center management, you can optimize and improve your power usage effectiveness (PUE), resource utilization, and performance by a significant margin. The best part is that your Intel CPUs and components already bring you one step closer to achieving this modernization.


These reference files are to be used for lab use only, not for production.  I would recommend pulling down the files, then modifying for your use case.  I have recently moved each of the files into their corresponding directory. 

**Files**
1.  **collectdinstall.sh** - this will startup collectd service with ipmi, smart, mcelog & reference points for Intel_RDT & Intel_PMU.    
2.  **collectd.conf** - reduced version with key plugins for our use cases (NOTE: this has prerequisites for specific packages to be installed prior). I would recommend spending time as this will be a key config file to ensure you get the data out.   
3.  **promehteusinstall.sh** - this will download & startup prometheus (NOTE:  to add in machines/nodes you need to update the prometheus.yml file)
4.  **prometheus.yml** - yml file for prometheus configuration that gets pulled down from script above.  NOTE: Pending if you are using collectd_exporter you will need to change the port # to 9103.  
5.  **prometheus.service** - service file required for service to run and gets pulled down from script above.  NOTE: if you have an issue at start of prometheus then I recommend cut/paste out this file & create a new service file.  I continue to fine tune this.  
6.  **CoreMetrics** - json file for importing into grafana to show collectd metrics with prometheus.   
7.  **collectd_exporter.service** - if you are using collectd_exporter to expose metrics to Prom /TSDB then this is a helpful service to use to help w/ restarts, etc.. 
8.  **grafana.sh** - starting grafana service 
9.  **collectd_master.conf** - another version of the collectd.conf that is closer to what I run on my nodes.  Note: this conf needs editing in your environment before you scale it. 


**Key Telemetry reference links:**  
https://github.com/andikleen/pmu-tools – PMU tool that is a PERF wrapper  </br>
https://github.com/andikleen/mce-inject – MCE – Inject  - helpful for injecting errors to track end to end </br>
https://github.com/andikleen/mcelog – MCE log information  </br>
https://github.com/intel/ipmctl/ – ipmctl for Intel® Optane™ DC Persistent Memory  </br>
https://github.com/intel/intel-cmt-cat – Intel® Resource Director Technology (Intel® RDT) usages  </br>
https://github.com/intel/platform-resource-manager – Workload co-location Intel® Platform Resource Manager (Intel® PRM)  </br>
https://github.com/intel/owca/ - Orchestration aware workload collection agent  </br>
https://wiki.opnfv.org/display/fastpath/Barometer+Home - Barometer - where you can see container examples of all the Intel Plugins, plus you can grab the plugins from here as well </br>
https://github.com/tianocore/edk2-staging/tree/UEFI_Redfish -EDKII Redfish Host Interface support </br>
https://github.com/intel-BMC -Intel OpenBMC Repository </br>

**Blogs:**  
*Know your Data Center -  https://itpeernetwork.intel.com/know-your-data-center/ </br>
*Collect or not collect -   https://itpeernetwork.intel.com/collect-or-not-collect/ </br>
*Intel tools for DC Transformation -  https://itpeernetwork.intel.com/data-center-transformation/ </br>
*Let’s rock Telemetry - https://itpeernetwork.intel.com/from-concept-to-reality-so-are-you-ready-to-rock-on-telemetry/  </br>
#Let's talk about OTP - https://itpeernetwork.intel.com/from-infrastructure-analysis-to-scaling-out-telemetry-lets-talk-about-otp/ </br>
#Intel Telemetry meets containers - https://itpeernetwork.intel.com/intel-telemetry-meets-containers/ </br>

**Notes**
In most cases we are using collectd + Prometheus + Grafana as a telemetry reference stack. 
