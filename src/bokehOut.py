#!/usr/bin/python3

from bokeh.plotting import figure
from bokeh.io import output_file, show
import random

TOOLS = ["hover", "wheel_zoom", "crosshair", "pan"]

def bokeh_html(outfile):

	output_file("Line.html")

	# declare figure object
	f = figure(width=1200, height=800, tools=TOOLS)

	# crate line object depending on number of input sequences.

	for i in range(len(outfile)):
	    randomColor = random.sample(range(1, 220), 3)
	    col = tuple(randomColor)
	    
	    f.line(outfile[i][0], outfile[i][1], legend = outfile[i][2], color = col)

	show(f)
