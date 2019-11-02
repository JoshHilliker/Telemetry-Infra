#! /bin/bash

yum update -y

yum install epel-release ca-certificates @Development tools psmisc util-linux coreutils xfsprogs e2fsprogs findutils git wget bzip2 kernel-devel perf blktrace lsof redhat-lsb sysstat python-yaml ipmitool dstat zlib=devel ntp collectl tree screen nvme-cli -y

echo "ready to go"