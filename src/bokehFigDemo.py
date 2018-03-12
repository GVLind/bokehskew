from bokeh.plotting import figure, output_file, show, curdoc

x = [1, 2, 3, 4, 5]

y = [6, 7, 2, 4, 5]

# create figure
p = figure(plot_width = 400, plot_height = 400)

# add a line renderer
p.line(x, y, line_width = 2)

output_file("line.html")

show(p)
