#!/usr/bin/python3

from bokeh.plotting import figure
from bokeh.io import output_file, save
import random

TOOLS = ["hover", "wheel_zoom", "crosshair", "pan"]

def bokeh_html(skewData):

	fileName = skewData[0]
	skew = skewData[1]


	output = "../html/" + fileName + ".html"
	
	output_file(output)

	# declare figure object
	f = figure(width = 1200, height = 800, tools = TOOLS, title = fileName )

	# crate line object depending on number of input sequences.
	for i in range(len(skew)):

		# adding random color feature.
	    randomColor = random.sample(range(1, 220), 3)
	    col = tuple(randomColor)
	    
	    # declares line based on outfile data.
	    f.line(skew[i][0], skew[i][1], legend = skew[i][2], color = col)

	print ("saving to: " + output)
	save(f)