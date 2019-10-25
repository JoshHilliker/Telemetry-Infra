#!/bin/bash
# setup for collectd initially.
# REFERENCE - not for production
yum install epel-release.noarch
yum install collectd
yum install collectd-rrdtool
yum install numactl

#IPMI Metrics - recommended no mods to config block
yum install collectd-ipmi
yum install ipmitool

#memory
yum install mcelog
yum install collectd-mcelog
modprobe mce-inject
systemctl start mcelog

#storage
yum install smartmontools
yum install collectd-smartmontools
#check the config block in collectd.conf for the right disks to get smart data on

#Intel_RDT - recommend to get plugin from Barometer or pull down latest tarball from collectd.org - check collectd.conf on github for config block
#Intel_PMU - recommend to get intel_pmu from https://github.com/andikleen/pmu-tools, then talk to your Intel rep to get Intel_PMU plugin & config block info

#recommend to check the collectd.conf file on https://raw.githubusercontent.com/JoshHilliker/Telemetry-Infra/master/collectd.conf, however each use case needs slight modifications and dependent on your infrastructure.    I have posted two different versions for reference.  Please reach out if any questions.   



systemctl enable collectd
systemctl start collectd