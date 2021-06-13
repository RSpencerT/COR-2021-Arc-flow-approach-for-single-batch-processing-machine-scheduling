# -*- coding: utf-8 -*-

"""
Data arc-flow AMPL generator
This script is used to generate the input file for the Arc-flow model described in the article.
"""

import numpy
import sys, getopt
from sys import argv

# Default arguments values
fexport = 'DataArcFlow.dat'            # Name of the target file with AMPL format.
fsize = 'size.txt'                     # Name of the file with the size values of the jobs
fprocessing = 'processing.txt'         # Name of the file with the processing time values of the jobs
N = 10                                 # Number of jobs
Cap = 20                               # Batch capacity

# Read arguments options
try:
   opts, args = getopt.getopt(argv[1:],"p:o:s:h:b:n:",["pfile=","ofile=","sfile="])
except getopt.GetoptError:
   print 'test.py -b <batchCapacity> -n <jobsNumber>'
   sys.exit(2)

optmandatory1 = False
optmandatory2 = False

for opt, arg in opts:
   if opt == '-h':
      print 'test.py -b <batchCapacity> -n <jobsNumber>'
      sys.exit()
   elif opt in ("-s", "--sfile"):
      fsize = arg
   elif opt in ("-o", "--ofile"):
      fexport = arg
   elif opt in ("-p", "--pfile"):
      fprocessing = arg
   elif opt in ("-b", "--paramb"):
      Cap = int(arg)
      optmandatory1 = True
   elif opt in ("-n", "--paramn"):
      N = int(arg)
      optmandatory2 = True

if optmandatory1 == False or optmandatory2 == False :
   print 'test.py -b <batchCapacity> -n <jobsNumber>'
   sys.exit(2)

# Starts the time counter
import time
start_time = time.time()

# Reading the files
fid = open(fsize,'rt') 
fidp = open(fprocessing,'rt')

sizes = []                 # Stores the size values of the jobs
processingp = []           # Stores the processing time values of the jobs
instance = []              # Stores the pairs with the values (processing time, size) of each job.

maxS = 0
minS = sys.maxsize
for l in fid :             # Reads the file and stores the size of the jobs
   nums = l.split(':')
   njob = int(nums[0])
   sizej = int(nums[1])

   sizes.append(sizej)
fid.close()

maxP = 0
minP = sys.maxsize
for l in fidp :            # Reads the file and stores the processing time of the jobs.
   nums = l.split(':')
   njob = int(nums[0])
   processingj = int(nums[1])

   processingp.append(processingj)

   job = []
   job.append(processingj)
   job.append(sizes[njob-1])
   instance.append(job)    # Create the list with the pairs of values for each job.
fid.close()

# Creating some sets and values
C = set(sizes)                   # Creates a set of all unique job size values
P = set(processingp)             # Creates a set of all unique job processing time values.

maxS = numpy.max(sizes)          # Gets the maximum and minimum value of sizes and processing times
minS = numpy.min(sizes)
maxP = numpy.max(processingp)
minP = numpy.min(processingp)

arcsF = set()                    # Stores all job arcs
arcsFF = set()                   # Stores all loss arcs

S = Cap
nodos = numpy.zeros(S+1)         # Indicates if the node is used
nodos[0] = 1                     # The first and last node will always be used
nodos[S] = 1

# Creating the graph
for j in range(0, S):            # For each node
   if nodos[j] == 1:             # if it is previously activated
      for i in C:                # creates a new node for each unique job size.
         if j+i <= S:
            arcsF.add((j, j+i))
            nodos[j+i] = 1       # Activates arc destination node

for i in range(1,S):             # It creates loss nodes between all active nodes and the last node B.
   if nodos[i] == 1:
      arcsFF.add( (i, S) )

# Sorting jobs by processing time
instance.sort(key=lambda x: x[0])
PT = numpy.unique(processingp)
PT.sort()

NT = numpy.zeros((Cap+1, PT.size), int)
NTp = numpy.zeros((Cap+1, PT.size), int)
NJ = numpy.zeros(PT.size, int)

# Generating the last parameters
procPrev = instance[0][0]
indexP = 0
for j in instance:
   if procPrev != j[0]:
      procPrev = j[0]
      indexP += 1
   NT[j[1], indexP] += 1
   NJ[indexP] += 1
   for pp in range(indexP, PT.size):
      NTp[j[1], pp] += 1

# Write the target file with AMPL format
fidF = open(fexport,'wt')        # Creates the target file with AMPL format.

fidF.write("data;" +'\n'+'\n')

fidF.write("param NumberJobs  := " + str(N) + "; \n\n" )
fidF.write("param B  := " + str(Cap) + "; \n\n" )
fidF.write("param alpha  := " + str(PT.size) + "; \n\n" )
fidF.write("param MinP  := " + str(minP) + "; \n")
fidF.write("param MaxP  := " + str(maxP) + "; \n")
fidF.write("param MinS  := " + str(minS) + "; \n")
fidF.write("param MaxS  := " + str(maxS) + "; \n\n")

fidF.write("set ArcJ  :=\n")
for arc in arcsF :
   fidF.write("   (" + str(arc[0]) + "," + str(arc[1]) + ")" + '\n')
fidF.write(";\n\n")

fidF.write("set ArcL  :=\n")
for arc in arcsFF :
   fidF.write("   (" + str(arc[0]) + "," + str(arc[1]) + ")" + '\n')
fidF.write(";\n\n")

fidF.write("param P  :=\n")
index = 1
for value in PT :
   fidF.write(str(index) + " " + str(value) + '\n')
   index = index + 1
fidF.write(";\n\n")

fidF.write("param NT  :=\n")
for c in range(0, Cap+1):
   for j in range(0, PT.size):
      fidF.write(str(c) + " " + str(j+1) + " " + str(NT[c, j]) + "\n")
fidF.write(";\n\n")

fidF.write("param NTp  :=\n")
for c in range(0, Cap+1):
   for j in range(0, PT.size):
      fidF.write(str(c) + " " + str(j+1) + " " + str(NTp[c, j]) + "\n")
fidF.write(";\n\n")

fidF.write("param NJ  :=\n")
for j in range(0, PT.size):
   fidF.write(str(j+1) + " " + str(NJ[j]) + "\n")
fidF.write(";\n\n")

fidF.close()

# Print the execution time
print(fexport + ' Time: ' + str(time.time() - start_time) )