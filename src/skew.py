#!/usr/bin/python3

from Bio import SeqIO, SeqUtils
import os
import sys

# declaring new lists

def parseInput(infile):
# open input file, hardcoded.
	
	skewData = []

	with open (infile, "r") as handle:
	    
	    # parse input
	    for record in SeqIO.parse(handle, "fasta"):

	        # calculate gc content using SeqUtils
	        gc = SeqUtils.GC_skew(record.seq, 100)

	        # create new list with id and gc
	        skewData.append([record.id, gc])

	    return skewData

def calculateSkew(infile):

	skewList = []

	for i in infile:
	    
	    # expanding incoming list
	    id = i[0]
	    gc = i[1]
	    y = [0]

	    # create new list for x and y values
	    x = [x for x in range(len(gc))]
	    
	    # creating list with gc-skew
	    for i in gc:
	        y.append(y[-1] + i)
	    
	    # removing empty first element
	    y = y[1:]
	    
	    # appending x, y-coordinated to a list, complete with ID.
	    skewList.append([x, y, id])

	return skewList

def get_files(path = "../data/"):

	for filename in os.listdir(path):

		if filename.endswith(".fasta"):
			
			yield filename

def start():

	path = sys.argv[1]

	for file in get_files(path):

		fullPath = path + file

		skewData = parseInput(fullPath)
		skewList = calculateSkew(skewData)

		yield (file, skewList)

if __name__ == "__main__":
	start()