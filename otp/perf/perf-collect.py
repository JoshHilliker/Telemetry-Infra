#! /usr/bin/python

from __future__ import print_function
import os, sys, subprocess, signal, socket
from argparse import ArgumentParser
from src import perf_helpers
from src import prepare_perf_events as prep_events

if __name__ == '__main__':

	script_path=os.path.dirname(os.path.realpath(__file__))
	result_dir=script_path+"/results"
	default_output_file=result_dir+"/" + socket.gethostname() + ".csv"
	from argparse import ArgumentParser

	parser=ArgumentParser(description='perf-collect: Time series dump of PMUs')
	parser.add_argument('-i', '--interval', type=int, default=1000, help='interval in ms for time series dump, default=1000')
	parser.add_argument('-o', '--outcsv', type=str, default=default_output_file, help='perf stat output in csv format, default=results/perfstat.csv') 
	parser.add_argument('-a', '--app', type=str, default=None, help='Application to run with perf-collect, perf collection ends after workload completion')
	parser.add_argument('-t', '--timeout', type=int, default=None, help='perf event collection time')
	parser.add_argument('--dryrun', help='test stat collection for 10sec, use it for checking event file correctness', action='store_true')

	required_arg=parser.add_argument_group('required arguments')
	required_arg.add_argument('-e', '--eventfile', type=str, default=None, help='Event file containing events to collect')

	if not len(sys.argv) > 1:
		parser.print_help()
		sys.exit()

	args=parser.parse_args()

	if not args.eventfile:
		exit("Please specify event file parameter")
	if args.app and args.timeout:
		exit("Please provide time duration or application parameter")

	# Check for superuser priviliges
	if os.geteuid() != 0:
		exit("Need supervisior privileges for perf collection\nPlease try again using 'sudo'. Exiting.")

	# Check if event file exists
	if not os.path.isfile(args.eventfile):
		raise SystemExit("event file not found")

        #create results dir
	if not os.path.exists(result_dir):
		os.mkdir(result_dir)

        #get perf events to collect
	collection_events=[]
	events, collection_events=prep_events.prepare_perf_events(args.eventfile)


	#start perf stat
	if args.timeout:
		cmd="perf stat -a -I %d -x , -e %s -o %s sleep %d" %(args.interval, events, args.outcsv, args.timeout)
	elif args.app:
		cmd="perf stat -a -I %d -x , -e %s -o %s %s" %(args.interval, events, args.outcsv, args.app)
	elif args.dryrun:
		cmd="perf stat -a -I %d -x , -e %s -o %s sleep 10" %(args.interval, events, args.outcsv)
	else:
		cmd="perf stat -a -I %d -x , -e %s -o %s" %(args.interval, events, args.outcsv)
		#exit("Incorrect usage model")

	try:	
		#print("Collecting perf stat")
		subprocess.call(cmd, shell=True)
		print("Collection complete! Calculating TSC frequency now")
	except KeyboardInterrupt:
	        print("Collection stopped! Calculating TSC frequency now")
	except:
		print("perf encountered errors")
	tsc_freq=str(perf_helpers.get_tsc_freq())

	with file(args.outcsv, 'r') as original: data = original.read()
	with file(args.outcsv, 'w') as modified: 
            modified.write("TSC Frequency(MHz),"+tsc_freq+",\n")
            modified.write("CPU count,"+str(perf_helpers.get_cpu_count())+",\n")
            modified.write("SOCKET count,"+str(perf_helpers.get_socket_count())+",\n")
            modified.write("HT count,"+str(perf_helpers.get_ht_count())+",\n")
            imc,cha=perf_helpers.get_imc_cha_count()
            modified.write("IMC count,"+str(imc)+",\n")
            modified.write("CHA count,"+str(cha)+",\n")
	    modified.write("### PERF EVENTS ###"+",\n")
	    for e in collection_events:
		modified.write(e+"\n")
	    modified.write("\n")
            modified.write("### PERF DATA ###"+",\n")
            modified.write(data)

	print ("perf stat dumped to %s" %args.outcsv)


