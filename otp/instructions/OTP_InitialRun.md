README for Initial Telemetry run - Project Name OTP (One Telemetry Package)
===========================================================================

OBJECTIVE
=========

Provide initial telemetry run for analysis via scripts. This process
will create three output files that we will leverage for analysis &
creation of graphs.

EXTRACT STEP (ET&L)
===================

Requirements
============

    1. perf
    2. ipmitool
    3. dstat
    Note: Ensure no other perf sampling is being done via another monitoring or telemetry tool

Install requirements
====================

    yum install perf ipmitool dstat -y 

Download the OTP Package
========================

    1.  create directory /home/otp
    2.  git clone http://github.com/JoshHilliker/InfraMgmt/otp 
    3.  chmod -R 775 otp.sh
    4.  chmod -R 775 ipmi/otp_ipmi.sh
    5.  If first run, ignore, if > 1, then remove all csv files from dstat, ipmi, & perf

Package includes
================

    1. otp.sh - kick off script 
    2. perf-collect.py - collection script
    3. ipmi script  - [includes:  system power, CUPs, inlet temp, cpu power, cpu temperature]
    4. dstat script - 
    5. platform metrics files

Execution
=========

    sudo nohup ./otp.sh &

Notes (to be removed)
=====================

*note this script runs for X amount of time based on otp.sh and then
kills ipmi & perf-collect processes *file names will be named based on [
hostname\_telemetry-type ]

OPEN questions from Josh \* what about haswell, broadwell, cascade lake?
for the reduced list - harshad/vaishali
