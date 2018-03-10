#!/usr/bin/python3

import skew
import bokehOut

for skewData in skew.start():
	bokehOut.bokeh_html(skewData)