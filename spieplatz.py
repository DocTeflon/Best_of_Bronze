import sys
from ChampDic import championDic

try:
	sys.stdout.write(championDic[144])
	sys.stdout.write(",")
except KeyError as k:
	sys.stdout.write("")