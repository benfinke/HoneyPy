# HoneyPy Copyright (C) 2013-2015 foospidy
# https://github.com/foospidy/HoneyPy
# See LICENSE for details
# HoneyPy log triage module

def triage(line):
	parts = line.split()
	# TCP
	#	parts[0]: date
	#	parts[1]: time_parts
	#	parts[2]: plugin
	#	parts[3]: session
	#	parts[4]: protocol
	#	parts[5]: event
	#	parts[6]: local_host
	#	parts[7]: local_port
	#	parts[8]: service
	#	parts[9]: remote_host
	#	parts[10]: remote_port
	#	parts[11]: data
	# UDP
	#	parts[0]: date
	#	parts[1]: time_parts
	#	parts[2]: plugin string part
	#	parts[3]: plugin string part
	#	parts[4]: session
	#	parts[5]: protocol
	#	parts[6]: event
	#	parts[7]: local_host
	#	parts[8]: local_port
	#	parts[9]: service
	#	parts[10]: remote_host
	#	parts[11]: remote_port
	#	parts[12]: data
	
	# only process actual events
	if len(parts) > 10:
		if '[-]' != parts[2]:
			# time_parts[0]: time
			# time_parts[1]: millisecond
			# time_parts[2]: time zone
			time_parts = parts[1].split(',')
		
			if 'Yes' == honeypy_config.get('twitter', 'enabled'):
				from lib.honeypy_twitter import post_tweet
			
				if 'TCP' == parts[4]:
					post_tweet(honeypy_config, parts[8], parts[9])
				else:
					# UDP splits differently (see comment section above)
					post_tweet(honeypy_config, parts[9], parts[10])

			if 'Yes' == honeypy_config.get('honeydb', 'enabled'):
				from lib.honeypy_honeydb import post_log
				
				if 'TCP' == parts[4]:
					if 11 == len(parts):
						parts.append('') # no data for CONNECT events
	
					post_log(honeypy_config.get('honeydb', 'url'), honeypy_config.get('honeydb', 'secret'), parts[0], time_parts[0], parts[0] + ' ' + time_parts[0], time_parts[1], parts[3], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10], parts[11])
				else:
					# UDP splits differently (see comment section above)
					if 12 == len(parts):
						parts.append('') # no data sent

					post_log(honeypy_config.get('honeydb', 'url'), honeypy_config.get('honeydb', 'secret'), parts[0], time_parts[0], parts[0] + ' ' + time_parts[0], time_parts[1], parts[4], parts[5], parts[6], parts[7], parts[8], parts[9], parts[10], parts[11], parts[12])

def triageConfig(config):
	global honeypy_config
	honeypy_config = config
