#!/usr/bin/python

from Bio import SeqIO, SeqUtils
import pandas as pd
from bokeh.models import ColumnDataSource, Select, LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.io import curdoc, show, output_file
from bokeh.layouts import layout
import os
import sys
import random

# declaring new lists


def calculateSkew(fullPath):

	df = pd.DataFrame(columns=["id","x","y","z"])
	df_index = 0

	with open (fullPath, "r") as handle:
	    
		for record in SeqIO.parse(handle, "fasta"):

			gc = SeqUtils.GC_skew(record.seq, 10000)

			count = 0
			skew = 0
			for nc in gc:

				count += 1 
				skew = skew + nc
				df.loc[df_index] = [record.id, count, skew, nc ]
				df.index += 1


	return df

def randomColor():
	randomColor = random.sample(range(1, 220), 3)


	return tuple(randomColor)

def plotBokeh(source):
	'''
	creates the figure object "plot". Then, for each unique ID in source,
	corresponding data is extracted,
	then a line object containing the ID data is added to plot. 

	'''

	plot = figure()

	plot.extra_y_ranges = {"GC": Range1d(start=-0.1, end=0.1)}

	plot.add_layout(LinearAxis(y_range_name="GC"), "right")

	for uniqID in source.id.unique():
		ID = ColumnDataSource(source[source["id"]==uniqID])

		col = randomColor()
		plot.title.text = strain
		plot.line(x = "x", y = "y", source = ID, color = col)
		plot.line(x = "x", y= "z", source = ID, color = col, line_alpha = .15, y_range_name = "GC")
	return plot

def plotUpdate(attrname, old, new):
	strain = strain_select.value
	

	src = calculateSkew(strains[strain]["path"])
	
	plot = plotBokeh(src)
	plot.title.text = strain
	

	controls = layout([strain_select])

	curdoc().clear()
	curdoc().add_root(controls)
	curdoc().add_root(plot)

	

strain = "e.coli"

strains = {
	"e.coliMix" : {
		"path" : "../data/e.coliMix.fasta"
	},
	"e.coli" : {
		"path" : "../data/e.coli.fasta"
	},
	"e.coli_2" : {
		"path" : "../data/e.coli2.fasta"
	}	
}

strain_select = Select(value = strain, title = "Strain", options = sorted(strains.keys()))

source = calculateSkew(strains[strain]["path"])

print (source)

plot = plotBokeh(source)

output_file=("../html/line.html")

strain_select.on_change("value", plotUpdate)

show(plot)
controls = layout([strain_select])

#curdoc().add_root(controls)
#curdoc().add_root(plot)