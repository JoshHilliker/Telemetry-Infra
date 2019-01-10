#!/bin/bash
# setup for collectd initially.
# REFERENCE - not for production
yum install epel-release.noarch
yum install collectd collectd-rrdtool
# NOTE:  need to create github to use for both ansible & then put collectd.conf 
cd /etc
wget https://raw.githubusercontent.com/JoshHilliker/Telemetry-Infra/master/collectd.conf
#Grab collectd.conf file from the github
systemctl enable collectd
systemctl start collectd
