#!/usr/bin/env python

from __future__ import print_function
from argparse import ArgumentParser
from time import strptime, mktime, strftime, gmtime
import os, re, sys
import csv, json
import collections

script_path=os.path.dirname(os.path.realpath(__file__))
#temporary output :time series dump of raw events 
output_file=script_path+"/results/tmp_perf_out.csv"
#temporary output:trasposed view of perf-collect output
time_dump_file=script_path+"/results/time_dump.csv"
#final output of post-process
out_metric_file=script_path+"/results/metric_out.csv"
#formula file
metric_file=script_path+"/events/metric.json"

#globals
#assumes sampling interval or dump interval is 1s
CONST_INTERVAL=1.0
CONST_TSC_FREQ=0.0
CONST_CORE_COUNT=0.0
CONST_HT_COUNT=0.0
CONST_SOCKET_COUNT=0.0
CONST_IMC_COUNT=0.0
CONST_CHA_COUNT=0.0
PERF_EVENTS=[]

#get the PMU names from metric expression
def get_metric_events(formula):
    f_len=len(formula)
    start=0
    metric_events=[] 	
    while start<f_len:
        s_idx=formula.find("[", start)
	e_idx=formula.find("]", start)
	if s_idx!=-1 and e_idx!=-1:
		metric_events.append(formula[s_idx+1:e_idx])
	else:
		break
	start=e_idx+1
    return metric_events

#get event index based on the groupid
def get_event_index(group_id, event, event_dict):
	offset=0
	for i in range(group_id):
		offset+=len(event_dict[i])
	idx=offset+event_dict[group_id].index(event)
	return idx

#evaluate metric expression
def evaluate_expression(formula, const_dict, value_list, event_dict):
	metric_events=get_metric_events(formula)
	formula=formula.replace("[","")
	formula=formula.replace("]","")
        
	#assign consts in the expression and create a list for collected events
	collected_events=[]
	for event in metric_events:
		if event in const_dict:
			formula=formula.replace(event, str(const_dict[event]))
		else:
			collected_events.append(event)

	grouped=False
	for group,events in event_dict.iteritems():
		#check if all events needed for the metric are in the same group
		if (all(event in events for event in collected_events)):
			grouped=True
			for event in collected_events:
				idx=get_event_index(group, event, event_dict)+1 #add 1 to account for the time column
				formula=formula.replace(event, str(value_list[idx]))
			break

	#pick first matching event from the event list if not grouped
	if not grouped:
		for event in collected_events:
			for group,events in event_dict.iteritems():
				if event in events:
					idx=get_event_index(group, event, event_dict)+1
					formula=formula.replace(event, str(value_list[idx]))
					break
	result=""
	try:
		result=str('{:.8f}'.format(eval(formula)))
	except ZeroDivisionError:
		print ("Divide by Zero evaluating", formula)
		sys.exit()
	except SyntaxError:
		print ("Syntax error evaluating ", formula)
		sys.exit()
	except:
		print("Unknown error evaluating ", formula)
		sys.exit()
		
	#print("expression ", formula, result)
	return result

#get events from perf event file
def get_perf_events():
	event_list=[]
	event_dict=collections.OrderedDict()
	group_id=0
	for line in PERF_EVENTS:
			if (line != '\n') and (line.startswith("#") == False):
				new_group=False
				if line.strip().endswith(";"):
					new_group=True

				line=line.strip()[:-1]
				event=line
				if "name=" in line:
					event=(line.split('\''))[1]
				event_list.append(event)
				if event_dict.get(group_id)==None:
					event_dict.setdefault(group_id,[event])
				else:
					event_dict[group_id].append(event)
				if new_group:
					group_id+=1
	return event_list,event_dict

#get the filenames for miscellaneous outputs
def get_extra_out_file(out_file, t):
	dirname=os.path.dirname(out_file)
	filename=os.path.basename(out_file)
	t_file=""
	text = "average" if t=='a' else "raw"
	parts=os.path.splitext(filename)
	if len(parts) == 1:
		t_file=text+"."+filename
	else:
		t_file=parts[-2]+"."+text+parts[-1]
	return (os.path.join(dirname,t_file))
		
#load metrics from json file and evaluate 
def load_metrics():
	event_list,event_dict=get_perf_events()
	metrics={}
	with open(metric_file, "r") as f_metric:
        	metrics=json.load(f_metric)
	        for i,metric in enumerate(metrics):
        	        metric_events=get_metric_events(metric['expression'].strip())
                	metrics[i]['add']=True
	                #check if metric can be computed from the current events
        	        for e in metric_events:
				if e.startswith("const"):
					continue
				if e not in event_list:
					metrics[i]['add']=False
	                #print (metric['expression'], metrics[i]['add'])
		f_metric.close()
	
	metric_row=["time"]
	for m in metrics:
		if m['add']==True:
			metric_row.append(m['name'])

        f_out=open(out_metric_file, 'wb')
	metriccsv=csv.writer(f_out, dialect='excel')
	metriccsv.writerow(metric_row)
	f_pmu=open(output_file, 'rb')
	pmucsv=csv.reader(f_pmu, delimiter=',')

	const_TSC=CONST_TSC_FREQ*CONST_CORE_COUNT*CONST_HT_COUNT*CONST_SOCKET_COUNT
	const_dict={'const_tsc_freq':CONST_TSC_FREQ, 'const_core_count':CONST_CORE_COUNT, 'const_socket_count':CONST_SOCKET_COUNT, 'const_thread_count':CONST_HT_COUNT, 'const_TSC':const_TSC}
	pmu_row_count=0
	metric_value=[""]*len(metric_row)
	average_row=[0.0]*len(metric_row)
	for row in pmucsv:
		if not row:
			continue
		if pmu_row_count>0:
			metric_value[0]=row[0]
			for metric in metrics:
				if metric['add']:
					result=evaluate_expression(metric['expression'], const_dict, row, event_dict)
					idx=metric_row.index(metric['name'])
					metric_value[idx]=result
					average_row[idx]+=float(result)
			metriccsv.writerow(metric_value)
		pmu_row_count+=1

	if pmu_row_count > 1:
		avg_file=get_extra_out_file(out_metric_file, 'a')
		f_avg=open(avg_file, 'wb')
		avgcsv=csv.writer(f_avg, dialect='excel')

		for i,val in enumerate(average_row):
			if not i:
				continue
			average_row[i]=val/(pmu_row_count-1)
			avgcsv.writerow([metric_row[i], average_row[i]])
		f_avg.close()

	f_out.close()
	f_pmu.close()

#get metadata from perf stat dump
def get_metadata():
	global CONST_TSC_FREQ
	global CONST_CORE_COUNT
	global CONST_HT_COUNT
	global CONST_SOCKET_COUNT
	global CONST_IMC_COUNT
	global CONST_CHA_COUNT
	global PERF_EVENTS

	start_events=False

	f_dat=open(dat_file, 'r')
	for line in f_dat:
		if start_events:
			if "PERF DATA" in line:
				break
			PERF_EVENTS.append(line)
			continue

		if line.startswith("TSC"):
			CONST_TSC_FREQ=float(line.split(',')[1])*1000000
		elif line.startswith("CPU"):
			CONST_CORE_COUNT=float(line.split(',')[1])
		elif line.startswith("HT"):
			CONST_HT_COUNT=float(line.split(',')[1])
		elif line.startswith("SOCKET"):
			CONST_SOCKET_COUNT=float(line.split(',')[1])
		elif line.startswith("IMC"):
			CONST_IMC_COUNT=float(line.split(',')[1])
		elif line.startswith("CHA"):
			CONST_CHA_COUNT=float(line.split(',')[1])
		elif "### PERF EVENTS" in line:
			start_events=True
	f_dat.close()

#write perf output from perf stat dump
def write_perf_tmp_output():
	global CONST_TSC_FREQ
	global CONST_CORE_COUNT
	global CONST_HT_COUNT
	global CONST_SOCKET_COUNT
	global CONST_IMC_COUNT
	global CONST_CHA_COUNT

	f_out=open(time_dump_file, 'wb')
	outcsv=csv.writer(f_out, dialect='excel')
	
        row0_event_name=[]
	row_data=[]
	percent_data=[]
	first_out_row=True
	prev_sample_time=0.0
	start_perf=False
	grab_date=False
	with open(dat_file, "r") as f_dat:
		incsv=csv.reader(f_dat, delimiter=',')
		row0_event_name.append("time")
		for it,row in enumerate(incsv):
			if not start_perf:
				if row and "PERF DATA" in row[0]:
					start_perf=True
					grab_date=True
				continue
			
			if grab_date:
				date_list = []
				for string in row:
					for char in string:
						date_list.append(char)
				grab_date=False
				double_list = ['1', '2', '3']
				if date_list[21] not in double_list:
					date_list[21] = '0'
				month = str(strptime("".join(date_list[17:20]), '%b').tm_mon)
				if len(month) == 1:
					month = '0' + month
                                	day = "".join(date_list[21:23])
                                	clk_time = "".join(date_list[24:32])
                                	year = "".join(date_list[33:37])
				timestamp = year+'-'+month+'-'+day+' '+clk_time
				#convert to epoch
				os.environ['TZ'] = 'UTC'
				epoch = int(mktime(strptime(timestamp, '%Y-%m-%d %H:%M:%S')))

			if row and start_perf and (len(row) > 3):
				#extract data , Note: relies on the perf output format
				time=int(float(row[0])) + epoch
				#time = str(strftime('%m/%d/%Y %H:%M:%S',  gmtime(time)))
				value=float(row[1])/CONST_INTERVAL
				name=row[3].strip()
				percent=row[5]
				
				#finished parsing one timestamp - write to output
				if prev_sample_time != time:
					if (len(row_data)>0) and first_out_row:
						#extend label with pecent sample
						tmp_list=row0_event_name[1:]
						for e in tmp_list:
							row0_event_name.append(e+" %sample")
						outcsv.writerow(row0_event_name)
						first_out_row=False

					row_data.extend(percent_data)
					outcsv.writerow(row_data)

					#prep for new row
					row_data=[]
					percent_data=[]
					row_data.append(time)

                                if first_out_row:
					row0_event_name.append(name)

				row_data.append(value)
				percent_data.append(percent)
				prev_sample_time=time
		if len(row_data)>0:
			outcsv.writerow(row_data)
		f_dat.close()
	f_out.close()

#combine per cha/imc counters from tmp output to systemview
def write_system_view():
	f_out=open(output_file, 'wb')
	outcsv=csv.writer(f_out, dialect='excel')
	f_tmp=open(time_dump_file, 'rb')
	tmpcsv=csv.reader(f_tmp, delimiter=',')
	row_count=0
	out_row0=[]
	out_row=[]
	sum_row=[]
	for in_row in tmpcsv:
		if not in_row:
			continue
		if row_count==0:
			in_row0=in_row[:]

		for i,event in enumerate(in_row0):
			if event.endswith('%sample'):
				break
			#cumulative sum for uncore event counters
			if event.startswith("UNC"):
				id_idx_start=event.rfind('.')
				#save row0 event name from the first uncore event
				if row_count==0:
					if event[id_idx_start+1:].isdigit():
						if event.endswith(".0"):
							out_row0.append(event[:-2])
					else: #grouping disabled case: disaggregated uncore events will have the same name
						if event not in out_row0:
							out_row0.append(event)
				else:
					#FIX ME: assumes each uncore event occur only once in the event file
					if event[id_idx_start+1:].isdigit():
						unc_event=event[:id_idx_start]
						core_id=int(event[id_idx_start+1:])
						if core_id >= CONST_CORE_COUNT:
							continue
						idx=out_row0.index(unc_event)
						out_row[idx]+=float(in_row[in_row0.index(event)])
					else: #grouping disabled case
						idx=out_row0.index(event)
						out_row[idx]+=float(in_row[i])
			else:
				if row_count==0:
					out_row0.append(event)
				else: 
					if out_row0.count(event) > 1:
						for j,e in enumerate(out_row0):
							if e==event and out_row[j]==0:
								out_row[j]=in_row[i]
								break
					else:
						out_row[out_row0.index(event)]=in_row[i]

					#out_row[out_row0.index(event)]=in_row[in_row0.index(event)]
		if row_count==0:
			outcsv.writerow(out_row0)
			sum_row=[0.0]*len(out_row0)
		else:
			outcsv.writerow(out_row)
			for j in range(len(out_row0)-1):
				sum_row[j+1]+=float(out_row[j+1])
		out_row=[0]*len(out_row0)
		row_count+=1

	f_out.close()
	f_tmp.close()
	
	sum_file=get_extra_out_file(out_metric_file, 'r')
	f_sum=open(sum_file, 'wb')
	sumcsv=csv.writer(f_sum, dialect='excel')

	for i in range(len(sum_row)-1):
		sumcsv.writerow([out_row0[i+1], int(sum_row[i+1])])
	f_sum.close()


#cleanup temp files
def cleanup():
	if os.path.isfile(time_dump_file):
		os.remove(time_dump_file)
	if os.path.isfile(output_file):
		os.remove(output_file)

if __name__ == '__main__':
	
	from argparse import ArgumentParser

	parser=ArgumentParser(description='perf-postprocess: perf post process')
	parser.add_argument('-m', '--metricfile', type=str, default=metric_file, help='formula file, default=events/metric.json') 
	parser.add_argument('-o', '--outcsv', type=str, default=out_metric_file, help='perf stat outputs in csv format, default=results/metric_out.csv') 
	parser.add_argument('-i', '--interval', type=float, default=1000, help='interval used in perf-collect, default is 1sec')
	required_arg=parser.add_argument_group('required arguments')
	required_arg.add_argument('-r', '--rawfile', type=str, default=None, help='Raw CSV output from perf-collect')
	if not len(sys.argv) > 2:
		parser.print_help()
		sys.exit()

	# Check for superuser priviliges
	if os.geteuid() != 0:
		exit("Need supervisior privileges for perf processing\nPlease try again using 'sudo'. Exiting.")

	script_path=os.path.dirname(os.path.realpath(__file__))
	result_dir=script_path+"/results"
        #create results dir
	if not os.path.exists(result_dir):
		os.mkdir(result_dir)
	
	args=parser.parse_args()

	dat_file = args.rawfile
        if args.outcsv:
		out_metric_file=args.outcsv
	if args.metricfile:
		metric_file=args.metricfile
	if args.interval:
		CONST_INTERVAL=args.interval/1000
	if not os.path.isfile(dat_file):
	   raise SystemExit("perf dat file not found")
	if not os.path.isfile(metric_file) and do_metric:
	   raise SystemExit("metric file not found")

	get_metadata()
	write_perf_tmp_output()
	write_system_view()
	load_metrics()
	cleanup()
