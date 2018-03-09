# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from bokeh.plotting import figure
from bokeh.io import output_file, show
from Bio import SeqIO, SeqUtils
import random

TOOLS = ["hover", "wheel_zoom", "crosshair", "pan"]

# declaring new lists
infile = []
outfile = []

# open input file, hardcoded.
with open ("./data/e.coliMix.fasta","r") as handle:
    
    # parse input
    for record in SeqIO.parse(handle, "fasta"):

        # calculate gc content using SeqUtils
        gc = SeqUtils.GC_skew(record.seq, 100)

        # create new list with id and gc
        infile.append([record.id, gc])
        
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

# declare bokeh output file object
output_file("Line.html")

# declare figure object
f = figure(width=1200, height=800, tools=TOOLS)

# crate line object depending on number of input sequences.

for i in range(len(outfile)):
    randomColor = random.sample(range(1, 220), 3)
    col = tuple(randomColor)
    
    f.line(outfile[i][0], outfile[i][1], legend = outfile[i][2], color = col)

show(f)

