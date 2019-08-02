Follow below guide once OTP\_InitialRun and ELG\_Install are complete.

INGESTION TYPES INTO ELG STACK (T&L)
====================================

FIRST TIME SETUP
================

    1) Create logstash config file or use example with modifications.
        vim /etc/logstash/conf.d/logstash-{TELEMETRY_TYPE}.conf
        ### OR ###
        cp /home/otp/dstat/logstash-dstat.conf /etc/logstash/conf.d/
        ### THEN MODIFY ###

    2) For .csv ingestion, model as below:
        
        input {
           file {
                max_open_files => "65535"
                path => "/var/log/node_perf_tests/*"  ### DIRECTORY WHERE FILES ARE LOCATED ###
                start_position => "beginning"
                mode => "read"
                sincedb_path => "/dev/null"
           }
        }
        filter{
           csv {
                separator => ","
                columns => ['time','IOPS read','IOPS writ','disk throughput (MB/s) read','disk throughput (MB/s) writ','memory usage % used','memory usage % buff','memory usage % cach','memory usage % free','network throughput (MB/s) recv','network throughput (MB/s) send','system Interrupts/Second','system Context Switches/Second'] ### COLUMN HEADERS ###
           }
           mutate{
                ### COLUMN DATA TYPES ###
                convert => { 
                                'time' => 'string'
                                'IOPS read' => 'float'
                                'IOPS writ' => 'float'
                                'disk throughput (MB/s) read' => 'float'
                                'disk throughput (MB/s) writ' => 'float'
                                'memory usage % used' => 'float'
                                'memory usage % buff' => 'float'
                                'memory usage % cach' => 'float'
                                'memory usage % free' => 'float'
                                'network throughput (MB/s) recv' => 'float'
                                'network throughput (MB/s) send' => 'float'
                                'system Interrupts/Second' => 'float'
                                'system Context Switches/Second' => 'float'
                }
           }
           ### GET TIMESTAMP IN ELASTICSEARCH FORMAT FROM EPOCH ###
           date {
                timezone => "UTC"
                match => ["time","UNIX"]
                target => "@timestamp"
           }
           grok {
                match => ["path","%{GREEDYDATA}/%{GREEDYDATA:filename}\.csv"]
           }
        }
        output {
           stdout { codec => rubydebug }
           elasticsearch {
                hosts => ["{CHOSEN IP}:9200"]
                index => "{CHOSEN INDEX}"
           }
        }

PERF-STAT
=========

    1) Navigate to location of OTP - One Telemetry Package
        cd /home/otp/perf

    2) Post process the raw perf-collect.py output.
        python perf-postprocess.py -r results/perfstat.csv

    3) Rename file to node
        mv results/metric_out.csv {NODENAME}_perf.csv

    4) Copy file to logstash destination directory.
        {EITHER CHOSEN DIRECTORY OR BELOW}
        cp results/{NODENAME}_perf.csv /var/log/node_telemetry
        ### Moving is not recommended, logstash deletes ingested file from directory ###

    5) Navigate to logstash directory.
        cd /usr/share/logstash/bin

    6) Start logstash using perf config file created in ELG_Install.README
        ./logstash -f /etc/logstash/conf.d/logstash-perf.conf

    7) Logstash will parse all files within the target directory.
        ### DO NOT PLACE NON-PERF FILES IN SAME DIRECTORY WHEN INGESTING ###

    8) After parsing has completed successfully, Logstash will hang, waiting for more files.
       If ingestion is completed, kill logstash or send SIGINT (ctrl + c)

    9) Verify in Elasticsearch indices for correct upload.
        Navigate to http://{CHOSEN IP}:9200/_cat/indices?v and look for perf index.

IPMI
====

    1) Navigate to location of IPMI OTP - One Telemetry Package.
        cd /home/otp/ipmi

    2) Find file with {Hostname}_ipmi.txt within IPMI OTP package.

    3) Post-process the raw output of IPMI.
        python parse_out.py {HOSTNAME}

    4) Copy file to logstash destination directory.
        {EITHER CHOSEN DIRECTORY OR BELOW}
        cp {NODENAME}_ipmi.csv /var/log/node_telemetry
        ### Moving is not recommended, logstash deletes ingested file from directory ###

    5) Navigate to logstash directory.
        cd /usr/share/logstash/bin

    6) Start logstash using perf config file created in ELG_Install.README
        ./logstash -f /etc/logstash/conf.d/logstash-ipmi.conf

    7) Logstash will parse all files within the target directory.
        ### DO NOT PLACE NON-PERF FILES IN SAME DIRECTORY WHEN INGESTING ###

    8) After parsing has completed successfully, Logstash will hang, waiting for more files.
       If ingestion is completed, kill logstash or send SIGINT (ctrl + c).

    9) Verify in Elasticsearch indices for correct upload.
        Navigate to http://{CHOSEN IP}:9200/_cat/indices?v and look for ipmi index.

DSTAT
=====

    1) Navigate to location of DSTAT OTP - One Telemetry Package.
        cd /home/otp/dstat

    2) Ensure dstat_metrics.csv is located in file directory.

    3) Post-process the raw output of DSTAT.
        python parser_dstat.py {HOSTNAME}

    4) Copy file to logstash destination directory.
        {EITHER CHOSEN DIRECTORY OR BELOW}
        cp {NODENAME}_dstat.csv /var/log/node_telemetry
        ### Moving is not recommended, logstash deletes ingested file from directory ###

    5) Navigate to logstash directory.
        cd /usr/share/logstash/bin

    6) Start logstash using perf config file created in ELG_Install.README
        ./logstash -f /etc/logstash/conf.d/logstash-dstat.conf

    7) Logstash will parse all files within the target directory.
        ### DO NOT PLACE NON-PERF FILES IN SAME DIRECTORY WHEN INGESTING ###

    8) After parsing has completed successfully, Logstash will hang, waiting for more files.
       If ingestion is completed, kill logstash or send SIGINT (ctrl + c).

    9) Verify in Elasticsearch indices for correct upload.
        Navigate to http://{CHOSEN IP}:9200/_cat/indices?v and look for dstat index.
