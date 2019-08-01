import csv
import sys

def output_parser():
	output = open(sys.argv[1] + '_ipmi.txt', 'r').readlines()
	tmp = input_parser()
	cmd_dict = tmp[0]
	cmd_list = tmp[1]
	line_count = 0
	cmd_count = 0
	time_flag = False
	with open(sys.argv[1] + '_ipmi.csv', mode='w+') as out_file:
		out_file = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		out_file.writerow(['time','metric_name','value'])
		while line_count < len(output):
			line = output[line_count]
			if 'Unable' in line:
				line_count += 1
				cmd_count += 1
				continue
			if '57 01 00' not in line:
				start_time = int(line)
				line_count += 1
				time_flag = True
			if cmd_count == len(cmd_list):
				cmd_count = 0
			command = cmd_list[cmd_count]
			tag = cmd_dict[command][1]
			if not time_flag and command != 'cpu_temps':
				line = line.split()
				hex_in = line[14] + line[13] + line[12] + line[11]
				time = str(int(hex_in, 16))
				value = int(line[4] + line[3], 16)
				out_file.writerow([time, tag, value])
				line_count += 2
				cmd_count += 1
			elif not time_flag and command == 'cpu_temps':
				line = line.split()
				cpu0_val = 99 - int(line[3], 16)
				cpu1_val = 99 - int(line[4], 16)
				out_file.writerow([start_time, 'CPU #0 Temp in [Celsius]', cpu0_val])
				out_file.writerow([start_time, 'CPU #1 Temp in [Celsius]', cpu1_val])
				cmd_count += 1
				line_count += 3
			time_flag = False
	print('Results for Ingestion into ELG Stack located in out_ipmi.csv')


def input_parser():
	in_file = open('otp_ipmi.sh', 'r')
	lines = in_file.readlines()
	out_dict = {}
	out_list = []
	for line in lines:
		if 'ipmitool' in line and '#' not in line:
			splitted = line.split()
			cmd_list = splitted[7:]
			req_id = cmd_list[0]
			if req_id == '0xc8': ### GET NODEMANAGER STATISTICS ###
				mode = cmd_list[4]
				if mode == '0x01':
					if cmd_list[5] == '0x00':
						out_dict['sys_pwr'] = (1, 'System Power in [Watts]')
						out_list.append('sys_pwr')
					elif cmd_list[5] == '0x01':
						out_dict['cpu_pwr'] = (1, 'CPU Power in [Watts]')
						out_list.append('cpu_pwr')
					else:
						raise Exception("PARSING ERROR: ADD POWER STATISTICS DOMAIN ID")
				elif mode == '0x02':
					out_dict['inlet'] = (1, 'Inlet Temp in [Celsius]')
					out_list.append('inlet')
				elif mode == '0x05':
					out_dict['outlet'] = (1, 'Outlet Temp in [Celsius]')
					out_list.append('outlet')
				else:
					raise Exception("PARSING ERROR: ADD ADDT'L C8 OPTION TO CASE STATEMENT")

			elif req_id == '0x4b': ### GET CPU/MEMORY TEMPS ###
				mode = cmd_list[4]
				if mode == '0x03':
					out_dict['cpu_temps'] = (1, 'CPU Temp in [Celsius]')
					out_list.append('cpu_temps')
				else:
					raise Exception("PARSING ERROR: ADD ADDT'L 4B OPTION TO CASE STATEMENT")
			else:
				raise Exception("PARSING ERROR: REQ_ID %s NOT RECOGNIZED") % req_id
		else:
			continue
	in_file.close()
	return (out_dict, out_list)


if len(sys.argv) == 1:
	print('')
	print('ERROR')
	print('USAGE: python parse_out.py NODENAME')
	print('')
	sys.exit()
else:
	output_parser()






