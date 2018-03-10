#!/usr/bin/python3

import skew
import bokehOut

plots =[]

for skewData in skew.start():
	plots.append(bokehOut.bokeh_html(skewData))

