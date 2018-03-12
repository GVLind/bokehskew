#!/usr/bin/python

from Bio import SeqIO, SeqUtils
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import output_file, show
import os
import sys
import random

# declaring new lists


def calculateSkew(path, filename):

	fullPath = path + filename

	df = pd.DataFrame(columns=["id","x","y"])
	df_index = 0

	with open (fullPath, "r") as handle:
	    
		for record in SeqIO.parse(handle, "fasta"):

			skew = [0]
			gc = SeqUtils.GC_skew(record.seq, 1)
			for nc in gc:
				skew.append(skew[-1]+nc)
			skew = skew[1:]

			for i in enumerate(skew):
				df.loc[df_index] = [record.id, i[0], i[1]]
				df_index += 1

	return df

def randomColor():
	randomColor = random.sample(range(1, 220), 3)
	return tuple(randomColor)

def plotBokeh(source):

	id1 = ColumnDataSource(source[source["id"]=="id1"])
	id2 = ColumnDataSource(source[source["id"]=="id2"])
	id3 = ColumnDataSource(source[source["id"]=="id3"])

	output_file = ("out.html")

	plot = figure()

	plot.line(x = "x", y = "y", source = id1, color = randomColor())
	plot.line(x = "x", y = "y", source = id2, color = randomColor())
	plot.line(x = "x", y = "y", source = id3, color = randomColor())

	show(plot)

if __name__ == "__main__":
	source = calculateSkew("../data/","gc.fasta")
	plotBokeh(source)


