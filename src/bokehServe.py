#!/usr/bin/python
'''
docsting
'''

# imports my skew script
import skew

# imports bokeh libraries and random
from bokeh.io import curdoc, show,output_file
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.models.annotations import LabelSet
import random



def create_fig(strain,skew):
	# create figure object
	f = figure(width = 1200, height = 800, title = strain )

	# crate line object depending on number of input sequences.
	for i in range(len(skew)):

		# adding random color feature.
		randomColor = random.sample(range(1, 220), 3)
		col = tuple(randomColor)
		    
		# declares line based on outfile data.
		f.line(skew[i][0], skew[i][1], legend = skew[i][2], color = col)
	return f
	

def update_plot(attr, old, new):
	strain = strain_select.value

	infile = skew.parseInput(strains[strain]["path"])
	skew = skew.calculateSkew(infile)

	plot = create_fig(strain, skew)

	controls = layout([[strain_select]])

	
	curdoc().add_root(controls)
	curdoc().add_root(plot)

# calls functions from skew to calculate GC-skew
strain = "test"

strains = {
	"e.coli" : {
		"path" : "../data/gc.fasta",
	},
	"test" : {
		"path" : "../data/gc.fasta",
	}
}

#infile = skew.parseInput(strains[strain]["path"])
#skew = skew.calculateSkew(infile)


strain_select = Select(value = strain, title = "Strain", options =sorted(strains.keys()))
#plot = create_fig(strain, skew)

strain_select.on_change("value", update_plot)

controls = layout([[strain_select]])

#curdoc().add_root(plot)
curdoc().add_root(controls)
