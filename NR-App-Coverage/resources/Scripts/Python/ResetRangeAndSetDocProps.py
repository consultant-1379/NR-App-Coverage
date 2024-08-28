# ********************************************************************
# Ericsson Inc.													SCRIPT
# ********************************************************************
#
#
# (c) Ericsson Inc. 2019 - All rights reserved.
#
# The copyright to the computer program(s) herein is the property
# of Ericsson Inc. The programs may be used and/or copied only with
# the written permission from Ericsson Inc. or in accordance with the
# terms and conditions stipulated in the agreement/contract under
# which the program(s) have been supplied.
#
# ********************************************************************
# Name	  : ResetRangeAndSetDocProps.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Reset the DL/UL threshold dropdown and bar chart based on selection of throughput type
#
# Usage	  : NR App Coverage

from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Data import *

def set_doc_props():
	if Document.Properties["ThroughputType"] == "Downlink":
		Document.Properties['TargetTitle'] = Document.Properties['ChosenDLThresholds']
	elif Document.Properties["ThroughputType"] == "Uplink":
		Document.Properties['TargetTitle'] = Document.Properties['ChosenULThresholds']

def reset_axis():
	for page in Document.Pages:
		if page.Title == "NR Cell Performance":
			for visualization in page.Visuals:
				if visualization.TypeId == VisualTypeIdentifiers.BarChart:
					if(visualization.Title=="Cell Failure Rate over Time (Hourly)"):
						current_chart = visualization.As[BarChart]();
						current_chart.YAxis.Range = AxisRange(0.0,1.0);

	for page in Document.Pages:
		if page.Title == "NR Cell Site Location":
			for visualization in page.Visuals:
				if visualization.TypeId == VisualTypeIdentifiers.BarChart:
					current_chart = visualization.As[BarChart]();
					current_chart.YAxis.Range = AxisRange(0.0,1.0);

set_doc_props()
reset_axis()
			