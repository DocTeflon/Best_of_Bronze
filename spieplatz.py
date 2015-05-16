import sys
from ChampDic import championDic

count = 0

for i in range(0,500):
	try:
		sys.stdout.write(championDic[i])
		sys.stdout.write(",")
		count += 1
	except KeyError as k:
		sys.stdout.write("")
		
print ""
print count