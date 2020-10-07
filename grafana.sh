#! /bin/bash
wget https://dl.grafana.com/oss/release/grafana-7.2.0-1.x86_64.rpm
sudo yum install grafana-7.2.0-1.x86_64.rpm
#wget https://dl.grafana.com/oss/release/grafana-5.4.2-1.x86_64.rpm
#sudo yum localinstall grafana-5.4.2-1.x86_64.rpm
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service