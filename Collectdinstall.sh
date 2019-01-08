#! /bin/bash
# setup for collectd initially.   


yum install epel-release.noarch
yum install collectd collectd-rrdtool 
# NOTE:  need to create github to use for both ansible & then put collectd.conf 
cd /etc
wget https://github.com/JoshHilliker/Telemetry-Infra/blob/master/collectd.conf
#Grab collectd.conf file from the github

yum install git rrdtool rrdtool-devel rrdtool-perl perl-HTML-Parser perl-JSON perl-CGI-Session     

cd /usr/local/
git clone https://github.com/httpdss/collectd-web.git
chmod +x collectd-web/cgi-bin/graphdefs.cgi

sed -i -re "s/127.0.0.1/0.0.0.0/g" /usr/local/collectd-web/runserver.py

mkdir -p /etc/collectd/
echo 'datadir: "/var/lib/collectd/rrd"' > /etc/collectd/collection.conf

systemctl enable collectd
systemctl start collectd 
 
python /usr/local/collectd-web/runserver.py &

