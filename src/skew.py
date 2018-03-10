#!/usr/bin/python3

from Bio import SeqIO, SeqUtils


# declaring new lists
infile = []
outfile = []

def parseInput():
# open input file, hardcoded.
	with open ("../data/e.coliMix.fasta","r") as handle:
	    
	    # parse input
	    for record in SeqIO.parse(handle, "fasta"):

	        # calculate gc content using SeqUtils
	        gc = SeqUtils.GC_skew(record.seq, 100)

	        # create new list with id and gc
	        infile.append([record.id, gc])

	    return infile

def calculateSkew(infile):

	for i in infile:
	    
	    # expanding incoming list
	    id = i[0]
	    gc = i[1]
	    
	    # create new list for x and y values
	    x = [x for x in range(len(gc))]
	    y = [0]
	    
	    # creating list with gc-skew
	    for i in gc:
	        y.append(y[-1]+i)
	    
	    # removing empty first element
	    y = y[1:]
	    
	    # appending x, y-coordinated to a list, complete with ID.
	    outfile.append([x, y, id])

	return outfile

def start():

	infile = parseInput()
	outfile = calculateSkew(infile)
	
	return outfile

