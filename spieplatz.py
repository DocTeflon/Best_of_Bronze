liste = [2]
print liste[0]
try:
	print liste[1]
except IndexError as I:
	print "INDEXERROR"