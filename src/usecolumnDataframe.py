#!/usr/bin/python

from Bio import SeqIO, SeqUtils
import pandas as pd
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh.io import curdoc, show, output_file
from bokeh.layouts import layout
import os
import sys
import random

# declaring new lists


def calculateSkew(fullPath):

	df = pd.DataFrame(columns=["id","x","y"])
	df_index = 0

	with open (fullPath, "r") as handle:
	    
		for record in SeqIO.parse(handle, "fasta"):

			skew = [0]
			gc = SeqUtils.GC_skew(record.seq, 1000)
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
	'''
	creates the figure object "plot". Then, for each unique ID in source,
	corresponding data is extracted,
	then a line object containing the ID data is added to plot. 

	'''

	plot = figure()	
	for uniqID in source.id.unique():
		ID = ColumnDataSource(source[source["id"]==uniqID])

		plot.title.text = strain
		plot.line(x = "x", y = "y", source = ID, color = randomColor())
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

plot = plotBokeh(source)

#output_file=("line.html")

strain_select.on_change("value", plotUpdate)

#show(plot)
controls = layout([strain_select])

curdoc().add_root(controls)
curdoc().add_root(plot)