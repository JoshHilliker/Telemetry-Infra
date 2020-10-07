#! /bin/bash
#objective - install GO, cAdvisor for perf metrics out of a container 
#requirements:   docker 

if [ ! -f /usr/bin/docker ]; then
echo "please install docker"
exit
fi


# start with GO install 
#1.	 Install go – validate it is working
wget https://dl.google.com/go/go1.13.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.13.linux-amd64.tar.gz
echo 'PATH=$PATH:/usr/local/go/bin' >> /etc/profile
source /etc/profile

#1a.  yum install libpfm libpfm-devel
set -e
YUM_PACKAGE_NAME="libpfm4 libpfm4-dev"
DEB_PACKAGE_NAME="libpfm4 libpfm4-dev"

 if cat /etc/*release | grep ^NAME | grep CentOS; then
    echo "==============================================="
    echo "Installing packages $YUM_PACKAGE_NAME on CentOS"
    echo "==============================================="
    yum install -y $YUM_PACKAGE_NAME
 elif cat /etc/*release | grep ^NAME | grep Ubuntu; then
    echo "==============================================="
    echo "Installing packages $DEB_PACKAGE_NAME on Ubuntu"
    echo "==============================================="
    apt-get update
    apt-get install -y $DEB_PACKAGE_NAME
 else
    echo "OS NOT DETECTED, couldn't install package $PACKAGE"
    exit 1;
 fi

exit 0

#2.	go get -d github.com/google/cadvisor
go get -d github.com/google/cadvisor

#3.	cd $GOPATH/go/src/github.com/google/cadvisor 
cd /root/go/src/github.com/google/cadvisor

#4.	make build GO_FLAGS=”-tags=libpfm,netgo”
make build GO_FLAGS="-tags=libpfm,netgo"

#5.  Prepare for docker build
#5a. copy the Dockerfile_perf from _______.  Put into deploy directory

echo "

FROM alpine:3.10

RUN apk update && \\
    apk add --no-cache wget && \\
    apk --no-cache add libc6-compat=1.1.22-r3 device-mapper=2.02.184-r0 findutils=4.6.0-r1 zfs=0.8.2-r0 build-base=0.5-r1 linux-headers=4.19.36-r0 && \\
    apk --no-cache add thin-provisioning-tools=0.7.1-r3 --repository http://dl-3.alpinelinux.org/alpine/edge/main/ && \\
    echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf

RUN wget https://sourceforge.net/projects/perfmon2/files/libpfm4/libpfm-4.10.1.tar.gz && \\
  tar -xvf libpfm-4.10.1.tar.gz && \\
  rm -f libpfm-4.10.1.tar.gz

RUN export DBG=\"-g -Wall\" && \\
  make -e -C libpfm-4.10.1 && \\
  make install -C libpfm-4.10.1

# Grab cadvisor from the staging directory.
COPY cadvisor /usr/bin/cadvisor

EXPOSE 8080

ENV CADVISOR_HEALTHCHECK_URL=http://localhost:8080/healthz

HEALTHCHECK --interval=30s --timeout=3s \\
  CMD wget --quiet --tries=1 --spider $CADVISOR_HEALTHCHECK_URL || exit 1

ENTRYPOINT [\"/usr/bin/cadvisor\", \"-logtostderr\"]  " > /root/go/src/github.com/google/cadvisor/deploy/Dockerfile_perf

#5b. change out perf.json in testing directory (add in key perf events) 
cd /root/go/src/github.com/google/cadvisor/
docker build  --no-cache --pull -t cadvisor:$(git rev-parse --short HEAD) --build-arg https_proxy=http://proxy-chain.intel.com:912 --build-arg http_proxy=http://proxy-chain.intel.com:911 -f deploy/Dockerfile_perf .

docker run   --volume=/:/rootfs:ro   --volume=/var/run:/var/run:ro   --volume=/sys:/sys:ro   --volume=/var/lib/docker/:/var/lib/docker:ro   --volume=/dev/disk/:/dev/disk:ro   --volume=/root/go/src/github.com/google/cadvisor/perf/testing:/etc/configs/perf   --publish=8080:8080   --tty   --interactive   --privileged   --name=cadvisor1   cadvisor:$(git rev-parse --short HEAD) -perf_events_config=/etc/configs/perf/perf.json
