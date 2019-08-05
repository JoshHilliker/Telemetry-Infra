This is a guide to install the ELG stack (Elasticsearch, Logstash, Grafana) on CentOS 7.6

ELASTICSEARCH INSTALLATION
==========================

    1) Install Java
        sudo yum -y install java-openjdk-devel java-openjdk

    2) Add the original ELK Stack Repo.
        sudo vim /etc/yum.repos.d/elasticsearch.repo
        ADD BELOW TO FILE
            [elasticsearch-7.x]
            name=Elasticsearch repository for 7.x packages
            baseurl=https://artifacts.elastic.co/packages/7.x/yum
            gpgcheck=1
            gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
            enabled=1
            autorefresh=1
            type=rpm-md

    3) Install elasticsearch
        sudo yum install elasticsearch -y

    4) Modify elasticsearch YAML file
        vim /etc/elasticsearch/elasticsearch.yml

    5) Uncomment and modify the following lines:
        cluster.name: {Node_name}
        network.host: {CHOSEN IP}
        http.port: 9200
        discovery.seed_hosts: ["{CHOSEN IP}"]
        path.data: /var/lib/elasticsearch
        path.logs: /var/log/elasticsearch
        cluster.initial_master_nodes: ["{CHOSEN IP}"]

    6) Start Elasticsearch service
        sudo systemctl daemon-reload
        sudo systemctl start elasticsearch
        sudo systemctl enable elasticesarch

    7) Update Firewall
        sudo firewall-cmd --permanent --add-port=9200/tcp
        sudo firewall-cmd --reload

    8) Check for valid Install
        curl http://{CHOSEN IP}:9200

    9) The below message should be seen if functioning properly.
        {
       "name" : "bBzN5Kg",
       "cluster_name" : "elasticsearch",
       "cluster_uuid" : "LKyqXXSvRvCpX9QAwKlP2Q",
       "version" : {
         "number" : "6.5.4",
         "build_flavor" : "default",
         "build_type" : "rpm",
         "build_hash" : "d2ef93d",
         "build_date" : "2018-12-17T21:17:40.758843Z",
         "build_snapshot" : false,
         "lucene_version" : "7.5.0",
         "minimum_wire_compatibility_version" : "5.6.0",
         "minimum_index_compatibility_version" : "5.0.0"
       },
       "tagline" : "You Know, for Search"
     }
        ### IF THE "name" FIELD IS BLANK, CHOOSE DIFFERENT IP OR CLUSTER NAME ###
        ### IF THE "cluster_uuid" FIELD IS "__na__", CHECK cluster.initial_master_nodes setting.

LOGSTASH INSTALLATION
=====================

    1) Install logstash, DO NOT START SERVICE, INGESTION IS DONE MANUALLY.
        sudo yum install logstash -y

GRAFANA INSTALLATION
====================

    1) Get RPM package for latest Grafana version and install. Look on
       https://grafana.com/grafana/download for the latest version. As if 8/5/2019 version is 6.2.5-1
        wget https://dl.grafana.com/oss/release/grafana-{VERSION}.x86_64.rpm 
        sudo yum localinstall grafana-{VERSION}.x86_64.rpm
        rm grafana-{VERSION}.x86_64.rpm

    2) Start Service
        sudo systemctl start grafana-server
        sudo systemctl enable grafana-server

    3) Update Firewall
        sudo firewall-cmd --permanent --add-port=3000/tcp
        sudo firewall-cmd --reload

    4) Default Login
        username: admin
        password: admin
