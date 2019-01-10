#!/usr/bin/sh
# setup for collectd initially.
# REFERENCE - not for production
# pull this down first.. it will grab collectd.conf file from this repo  


yum install epel-release.noarch
yum install collectd collectd-rrdtool 
# NOTE:  need to create github to use for both ansible & then put collectd.conf 
cd /etc
wget https://raw.githubusercontent.com/JoshHilliker/Telemetry-Infra/master/collectd.conf
#Grab collectd.conf file from the github

#  add these sections back if you are planning to do a local webserver to look at RRD files.
#yum install git rrdtool rrdtool-devel rrdtool-perl perl-HTML-Parser perl-JSON perl-CGI-Session     
#cd /usr/local/
#git clone https://github.com/httpdss/collectd-web.git
#chmod +x collectd-web/cgi-bin/graphdefs.cgi

#sed -i -re "s/127.0.0.1/0.0.0.0/g" /usr/local/collectd-web/runserver.py

#mkdir -p /etc/collectd/
#echo 'datadir: "/var/lib/collectd/rrd"' > /etc/collectd/collection.conf

systemctl enable collectd
systemctl start collectd 
 
#python /usr/local/collectd-web/runserver.py &

