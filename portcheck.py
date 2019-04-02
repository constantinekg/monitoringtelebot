#!/usr/bin/env python3

import subprocess
import os, sys


def portchecker():
	#------------------------------------------------------------------------Load from file
	points = {}
	result = []
	status = 'ok'
	for line in open(os.path.dirname(sys.argv[0])+'/servers.txt'):
		line = line.split('\n') # из строки получаем список
		line = line[0] # избавляемся от последнего элемента (\n)
		line = line.split(' ') # разделяем данные
		if line[0] != '':
			points[line[0]] = line[1:] # добавляем в словарь
									   #первый элемент список - как ключ
									   # остальные - значение
		else:
			pass
	#------------------------------------------------------------------------Port checker
	prestatus=[]
	for key, val in points.items():
		direct_output = subprocess.check_output('nmap -sT -Pn -p '+val[0]+' '+key, shell=True) #could be anything here.
		if 'open' not in direct_output.decode('utf-8').split():
			print ('port '+val[0]+' ( '+val[1]+' )'+' is CLOSED')
			result.append(('port '+val[0]+' ( '+val[1]+' )'+' is CLOSED'))
			prestatus.append('bad')
		elif 'open' in direct_output.decode('utf-8').split():
			# print ('port '+val[0]+' ( '+val[1]+' )'+' is OPEN')
			#result.append(('port '+val[0]+' ( '+val[1]+' )'+' is OPEN'))
			prestatus.append('ok')
		else:
			pass
	if 'bad' in prestatus:
		status='bad'
	elif 'bad' not in prestatus:
		status='ok'
	else:
		pass
	return (result, status)
