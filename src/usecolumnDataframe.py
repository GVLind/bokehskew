#!/usr/bin/python
'''
Author: Victor Lindh 2018-03-12

#####################

A script for visualizing GC-skew in a bacterial genome.
Outputs html page at default url: http://localhost:5006. 

Strains used is hardcoded and must be present in ../data/

runs like:

bokeh serve [scriptname]

#####################

suggested improvements:

1) add feature for selecting strains analyzed.
2) add feature for uploading data for analysis. 

'''
from bokeh.models import Select, LinearAxis, Range1d, ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import layout
from Bio import SeqIO, SeqUtils
import pandas as pd
import random

def calculateSkew(fullPath):
	'''
	reads file specified by function argument, records is parsed by using SeqIO
	, gc skew is calculated with SeqUtils.GC_skew. for every 10000 nucleotides 
	the sequence ID, nucleotide index, cumulative average GC-skew, 
	and average nucleotide score is added to a pandas dataframe and returned.

	The average gc-skew av nucleotide score is used as a compromise between 
	computational load and accuracy.

	'''

	df = pd.DataFrame(columns = ["id", "x", "y", "z"])
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
	'''
	reutrning tuple of rgb colors, used in line objects.
	'''
	randomColor = random.sample(range(1, 220), 3)
	return tuple(randomColor)

def plotBokeh(source):
	'''
	creates the figure object "plot". a second y axis is added for
	fitting the nucleotide score in the same graph.
	Then, for each unique ID in source, corresponding data is extracted.
	A line object representing the skew data data is added to plot.
	A Second line object representing the nucleotide score

	'''
	plot = figure()

	plot.extra_y_ranges = {"ncScore" : Range1d(start = -0.1, end = 0.1)}

	plot.add_layout(LinearAxis(y_range_name = "ncScore"), "right")

	for uniqID in source.id.unique():
		ID = ColumnDataSource(source[source["id"] == uniqID])
		col = randomColor()

		plot.title.text = strain
		plot.line(x = "x", y = "y", source = ID, color = col)
		plot.line(x = "x", y = "z", source = ID, color = col, line_alpha = .15, y_range_name = "ncScore")

	return plot

def plotUpdate(attrname, old, new):
	'''
	quite hacky solution that takes the input from the web browser drop-down list
	and re-runs the skew calculations, wipes the webpage and updates all information

	'''
	strain = strain_select.value
	src = calculateSkew(strains[strain]["path"])
	plot = plotBokeh(src)

	plot.title.text = strain
	controls = layout([strain_select])

	# clearing previous browser
	curdoc().clear()

	# adding new content to browser
	curdoc().add_root(controls)
	curdoc().add_root(plot)

# declaring a dataset representing the strains.
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

# adding selection object
strain_select = Select(value = strain, title = "Strain", options = sorted(strains.keys()))

# calculating sorce data
source = calculateSkew(strains[strain]["path"])

# redering plot
plot = plotBokeh(source)

# adding a rule for chaging item in the browser drop down list
strain_select.on_change("value", plotUpdate)

# declaring layout for drop down list
controls = layout([strain_select])

# adding controls and plot as elements in the webpage.
curdoc().add_root(controls)
curdoc().add_root(plot)