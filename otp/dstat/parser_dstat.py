import csv
import os, sys
from time import strptime, mktime, strftime, gmtime

def parse_bois():
	with open(sys.argv[1] + '_dstat.csv', mode='w+') as out_file:
		out_file = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		output = open('dstat_metrics.csv', 'r').readlines()
		epoch = get_time(output[3].split()[3:7])

		### GET COLUMNS ###
		tmp_col = output[6].split(",")
		columns = []
		for x in range(len(tmp_col)):
			header = tmp_col[x]
			change = header.replace('"', '')
			change = change.replace('\n', '')
			if change == 'int':
				change = 'Interrupts/Second'
			elif change == 'csw':
				change = 'Context Switches/Second'
			columns.append(change)

		### GET METRIC TYPE ###
		met_type = []
		tmp_type = output[5].split(",")
		for i in range(len(tmp_type)):
			level = tmp_type[i].replace('"', '')
			if level == '' or level == '\n':
				level = met_type[i - 1]
			if 'memory' in level and '%' not in level:
				level += ' %'
			elif 'io' in level:
				level = 'IOPS'
			elif 'dsk' in level:
				level = 'disk throughput (MB/s)'
			elif 'net' in level:
				level = 'network throughput (MB/s)'
			met_type.append(level)

		### COMBINE METRICS/COLUMNS ###
		comb_metrics = []
		for i in range(len(tmp_type)):
			if i == 0:
				comb_metrics.append('time')
			metric = met_type[i]
			column = columns[i]
			comb_metrics.append(metric + ' ' + column)
		out_file.writerow(comb_metrics)
		
		
		### DATA PARSING ###
		time_delta = 0
		for line in output[7:]:
			line = line.split(",")
			time = epoch + time_delta
			values = [time]
			for value in range(len(line)):
				tag = comb_metrics[value + 1]
				num = float(line[value])

				if 'IOPS' in tag:
					num = float(num)

				elif 'disk' in tag or 'network' in tag:
					num = float(float(num) / 1000000)
					num = '%.3f' % float(num)
					total_memory = float(line[7]) + float(line[4])

				elif 'memory' in tag:
					if 'used' in tag:
						num = (float(num) / total_memory) * 100
					elif 'buff' in tag:
						num = (float(num) / total_memory) * 100
					elif 'cach' in tag:
						num = (float(num) / total_memory) * 100
					elif 'free' in tag:
						num = (float(num) / total_memory) * 100
					else:
						raise Exception("Error with Memory Parsing")
					num = '%.3f' % float(num)

				values.append(str(num))
			time_delta += 1
			out_file.writerow(values)

		print('Successfully Parsed, dumped to ' + sys.argv[1] + '_dstat.csv')


def get_time(timeline):
	month = str(strptime("".join(timeline[1]), '%b').tm_mon)
	if len(month) == 1:
		month = '0' + month
	year = timeline[2]
	clk_time = timeline[3]
	day = ''
	for char in timeline[0]:
		if char in '0123456789':
			day += char
	timestamp = year + '-' + month + '-' + day + ' '+ clk_time
	os.environ['TZ'] = 'UTC'
	epoch = int(mktime(strptime(timestamp, '%Y-%m-%d %H:%M:%S')))
	return epoch


if len(sys.argv) == 1:
	print('')
	print('ERROR')
	print('USAGE: python parser_dstat.py NODENAME')
	print('')
	sys.exit()
else:
	parse_bois()
