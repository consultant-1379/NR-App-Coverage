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
# Name	  : Reset Filters and Markings.py
# Date	  : 08/04/2024
# Revision: 1.0
# Purpose : Reset the Filters,Marking,Slider and Axis.
#
# Usage	  : NR App Coverage

from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Application.Visuals import *
from Spotfire.Dxp.Application.Filters import *
from Spotfire.Dxp.Application.Visuals.Maps import *
from System import Array
from System.Collections.Generic import Dictionary
from Spotfire.Dxp.Application.Scripting import ScriptDefinition, ScriptParameterType as type
from System.Reflection import Assembly
from Spotfire.Dxp.Data.Collections import *
from System.Runtime.Serialization import ISerializable
from System.Collections import IComparer
from System.Collections.Generic import IComparer

CellPerformanceRankingArray= Array.CreateInstance(str,31,2)

CellPerformanceRankingArray[0,0]="NRSectorCarrier";				    CellPerformanceRankingArray[0,1]="False";
CellPerformanceRankingArray[1,0]="DATE_ID";							CellPerformanceRankingArray[1,1]="True";
CellPerformanceRankingArray[2,0]="HOUR_ID";							CellPerformanceRankingArray[2,1]="True";
CellPerformanceRankingArray[3,0]="Cell";							CellPerformanceRankingArray[3,1]="True";
CellPerformanceRankingArray[4,0]="NR_NAME";							CellPerformanceRankingArray[4,1]="True";
CellPerformanceRankingArray[5,0]="NRCellDU";						CellPerformanceRankingArray[5,1]="False";
CellPerformanceRankingArray[6,0]="Latitude(Converted)";				CellPerformanceRankingArray[6,1]="False";
CellPerformanceRankingArray[7,0]="Longitude(Converted)";			CellPerformanceRankingArray[7,1]="False";
CellPerformanceRankingArray[8,0]="Latitude(Final Converted)";		CellPerformanceRankingArray[8,1]="False";
CellPerformanceRankingArray[9,0]="Longitude(Final Converted)";		CellPerformanceRankingArray[9,1]="False";
CellPerformanceRankingArray[10,0]="latitude";						CellPerformanceRankingArray[10,1]="False";
CellPerformanceRankingArray[11,0]="longitude";						CellPerformanceRankingArray[11,1]="False";
CellPerformanceRankingArray[12,0]="failedDLSamplesT1";				CellPerformanceRankingArray[12,1]="False";
CellPerformanceRankingArray[13,0]="failedDLSamplesT2";				CellPerformanceRankingArray[13,1]="False";
CellPerformanceRankingArray[14,0]="failedDLSamplesT3";				CellPerformanceRankingArray[14,1]="False";
CellPerformanceRankingArray[15,0]="failedDLSamplesT4";				CellPerformanceRankingArray[15,1]="False";
CellPerformanceRankingArray[16,0]="failedDLSamplesT5";				CellPerformanceRankingArray[16,1]="False";
CellPerformanceRankingArray[17,0]="failedULSamplesT1";				CellPerformanceRankingArray[17,1]="False";
CellPerformanceRankingArray[18,0]="failedULSamplesT2";				CellPerformanceRankingArray[18,1]="False";
CellPerformanceRankingArray[19,0]="failedULSamplesT3";				CellPerformanceRankingArray[19,1]="False";
CellPerformanceRankingArray[20,0]="failedULSamplesT4";				CellPerformanceRankingArray[20,1]="False";
CellPerformanceRankingArray[21,0]="failedULSamplesT5";				CellPerformanceRankingArray[21,1]="False";
CellPerformanceRankingArray[22,0]="totalDLSamples";					CellPerformanceRankingArray[22,1]="False";
CellPerformanceRankingArray[23,0]="totalULSamples";					CellPerformanceRankingArray[23,1]="False";
CellPerformanceRankingArray[24,0]="SN";								CellPerformanceRankingArray[24,1]="False";
CellPerformanceRankingArray[25,0]="arfcnDL";						CellPerformanceRankingArray[25,1]="False";
CellPerformanceRankingArray[26,0]="arfcnUL";						CellPerformanceRankingArray[26,1]="False";
CellPerformanceRankingArray[27,0]="bSChannelBwDL";					CellPerformanceRankingArray[27,1]="False";
CellPerformanceRankingArray[28,0]="bSChannelBwUL";					CellPerformanceRankingArray[28,1]="False";
CellPerformanceRankingArray[29,0]="frequencyDL";					CellPerformanceRankingArray[29,1]="False";
CellPerformanceRankingArray[30,0]="frequencyUL";					CellPerformanceRankingArray[30,1]="False";



def reset_sliders():
	for page in Application.Document.Pages:
			for visualization in page.Visuals:
				if visualization.TypeId == VisualTypeIdentifiers.BarChart:
					currentChart = visualization.As[BarChart]();
					if (currentChart.Title=="Worst Performing Cells (Ranked by Avg Failed User Sessions)"):
						currentChart.XAxis.ManualZoom = True;
						currentChart.XAxis.ZoomRange = AxisRange(None,None);
					else:
						currentChart.XAxis.ManualZoom = False;
					

def reset_marking_filtering():
	for dataTable in Document.Data.Tables:
		for marking in Document.Data.Markings:
			rows = RowSelection(IndexSet(dataTable.RowCount, False))
			marking.SetSelection(rows, dataTable)
	for filterScheme in Document.FilteringSchemes:
		filterScheme.ResetAllFilters()

def reset_map():	
	for page in Application.Document.Pages:
		if page.Title == "NR Cell Site Location":
			for visualization in page.Visuals:
					if visualization.TypeId == VisualTypeIdentifiers.MapChart2:
						currentChart = visualization.As[Maps.MapChart]();
						for m in currentChart.Layers:
							m.IncludeInResetViewExtent=False;
						currentChart.ResetViewExtent()
						for m in currentChart.Layers:
							if m.Title=="NR Cell Site Location":
								m.IncludeInResetViewExtent=True;

def show_filteritem_raw(filterPanel,title):
	for group in filterPanel.TableGroups:
		if group.Name == "IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW":
			for x in range (0,len(CellPerformanceRankingArray)/2):
				filterItem = group.GetFilter(CellPerformanceRankingArray[x,0])
				if filterItem != None:
					if CellPerformanceRankingArray[x,1]=="True":
						if CellPerformanceRankingArray[x,0] ==  "Cell" and title == "NR Network Overview":
							filterItem.Visible = False
						else:	
							filterItem.Visible = True
					else:
						filterItem.Visible = False
		else:
			hide_data_table(group)
			
def show_filteritem_day(filterPanel,title):
	for group in filterPanel.TableGroups:
		if group.Name == "IL_DC_E_NR_EVENTS_NRCELLDU_V_DAY":
			for x in range (0,len(CellPerformanceRankingArray)/2):
				filterItem = group.GetFilter(CellPerformanceRankingArray[x,0])
				if filterItem != None:
					if CellPerformanceRankingArray[x,1]=="True":
						if CellPerformanceRankingArray[x,0] ==  "Cell" and title == "NR Network Overview":
							filterItem.Visible = False
						else:	
							filterItem.Visible = True
					else:
						filterItem.Visible = False
		else:
			hide_data_table(group)
			
def hide_data_table(group):
	for filter in group.FilterHandles:
		filter.Visible = False

								
def default_filters():
	for page in Application.Document.Pages:
		if page.Title == "NR Cell Performance" or page.Title == "NR Network Overview" or page.Title == "NR Cell Site Location":
			filterPanel = page.FilterPanel
			show_filteritem_raw(filterPanel,page.Title)
		elif "Historical Trend" in page.Title:
			filterPanel = page.FilterPanel
			show_filteritem_day(filterPanel,page.Title)
			

def reset_document_properties():
	Document.Properties["NRlist"]=""


def reset_dropdown_slider():
	Document.Properties["ChosenDLThresholds"]=" "
	Document.Properties["ChosenULThresholds"]=" "
	Document.Properties["maxCells"]=10


default_filters()
reset_marking_filtering()
reset_sliders()
reset_map()
reset_document_properties()
reset_dropdown_slider()
