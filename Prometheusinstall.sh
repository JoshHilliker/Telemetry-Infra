#!/bin/bash
# Installation of Prometheus  - REFERENCE ONLY - not for production

sudo groupadd --system prometheus
sudo useradd -s /sbin/nologin --system -g prometheus prometheus
sudo mkdir /var/lib/prometheus
for i in rules rules.d files_sd; do sudo mkdir -p /etc/prometheus/${i}; done
sudo yum -y install wget
cd /tmp
export RELEASE=2.9.2
wget https://github.com/prometheus/prometheus/releases/download/v2.9.2/prometheus-2.9.2.linux-amd64.tar.gz
tar xvf prometheus-${RELEASE}.linux-amd64.tar.gz
cd prometheus-${RELEASE}.linux-amd64/
sudo cp prometheus promtool /usr/local/bin/
sudo cp -r consoles/ console_libraries/ /etc/prometheus/
cd /etc/prometheus/
wget https://raw.githubusercontent.com/JoshHilliker/Telemetry-Infra/master/prometheus.yml
cd /etc/systemd/system/
wget https://raw.githubusercontent.com/JoshHilliker/Telemetry-Infra/master/prometheus.service
rm -rf prometheus-${RELEASE}.linux-amd64.tar.gz
rm -rf prometheus-${RELEASE}.linux-amd64/
for i in rules rules.d files_sd; do sudo chown -R prometheus:prometheus /etc/prometheus/${i}; done
for i in rules rules.d files_sd; do sudo chmod -R 775 /etc/prometheus/${i}; done
sudo chown -R prometheus:prometheus /var/lib/prometheus/
sudo systemctl daemon-reload
systemctl
