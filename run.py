import os, sys, subprocess
from datetime import datetime

def kbest (k, values):
	error=(1,-1)
	values.sort()
	for i in range(len(values)-k):
		maximum = values[i+k-1]
		minimum = values[i]
		e = (maximum - minimum) / float(maximum) 
		if e < 0.05:
			return sum(values[i:i+k]) / float(k)
		if e < error[0]:
			error=(e,i)
	if error[1] != -1:
		return sum(values[error[1]:error[1]+k]) / float(k)
	return -1


funcs = ["ijk", "ikj", "jki", "ijk_t", "jki_t", "block", "block_omp", "cuda", "block_cuda"]
matrix = ["32","128","1024","2048"]
measures = ["time", "mrl1", "mrl2", "mrl3", "L3_TCM", "FP_INS"]
nreps = 8
k=3

total = len(funcs)*len(matrix)*len(measures)*nreps
count=1

now = str( datetime.now() )
fname = now[11:19] + "_" + now[:10] + ".csv"

table = open( fname, "w" )

table.write(",,time,mr L1,mr L2,mr L3,RAM_A(L3_TCM),Flops\n")

tmp=[]*len(measures)

for func in funcs:
	print func
	table.write(func)

	for m in matrix:
		print m
		table.write(","+m)

		for ms in measures:
			print ms
			tmp=[]
			for r in range(nreps):
				print count,"of",total,
				s=datetime.now()
				count+=1
				execution = subprocess.Popen(
					["./mat", m, func, ms],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				) 
				execution.wait()
				try:
					c_printf = execution.stdout.read().decode("ascii").strip()
					tmp.append(float(c_printf))
				except:
					print "Error 1"
				e=datetime.now()
				print "\ttest time:",e-s
			try:
				table.write("," + str( kbest(k,tmp) ) )
			except:
				table.write(",")
				print "Error 2"

		table.write("\n")
	table.write("\n")
table.close()

