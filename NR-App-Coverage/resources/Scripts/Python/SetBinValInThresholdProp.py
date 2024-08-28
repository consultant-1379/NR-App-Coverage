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
# Name	  : SetBinValInThresholdProp.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Set the DL/UL Threshold document property based on the selection of DL/UL performance target dropdown in setting page
#
# Usage	  : NR App Coverage

from System.Collections.Generic import List
from Spotfire.Dxp.Data import DataValueCursor, IndexSet
import System
import Spotfire.Dxp.Application
from Spotfire.Dxp.Data import *
from System.Collections.Generic import HashSet
import System.String
from Spotfire.Dxp.Framework.ApplicationModel import *

control_name_list = ["DLRange1", "DLRange2" ,"DLRange3" ,"DLRange4" ,"DLRange5", "ULRange1", "ULRange2" ,"ULRange3" ,"ULRange4" ,"ULRange5"]

dropdown_doc_prop_dict = {'DLRange1':'DLThreshold1','DLRange2':'DLThreshold2','DLRange3':'DLThreshold3','DLRange4':'DLThreshold4','DLRange5':'DLThreshold5',
'ULRange1':'ULThreshold1','ULRange2':'ULThreshold2','ULRange3':'ULThreshold3','ULRange4':'ULThreshold4','ULRange5':'ULThreshold5'}

def set_bin_val_doc_prop(data_tablename,type,control_name):
	if Document.Data.Tables.Contains(data_tablename):
		table = Document.Data.Tables[data_tablename]
		user_input = Document.Properties[control_name]
		row_selection=table.Select('Min='+str(user_input)+'')
		cursor = DataValueCursor.CreateFormatted(table.Columns["Bin values"])
		cursor1 = DataValueCursor.CreateFormatted(table.Columns["Min"])
		bin_val = 0
		for	 _ in  table.GetRows(row_selection.AsIndexSet(),cursor,cursor1): # Will be one row only
			bin_val = cursor.CurrentValue
			
		Document.Properties[dropdown_doc_prop_dict[control_name]]  = bin_val

def main():
	for i in range(len(control_name_list)):
		control_name = control_name_list[i]
		data_tablename = 'DL_ThroughputMap' # default
		type = 'DL'

		if control_name.startswith('UL'):
			data_tablename = 'UL_ThroughputMap'
			type = 'UL'
		set_bin_val_doc_prop(data_tablename,type,control_name) 
		
	msa_clicked = Document.Properties["MSAButtonClicked"]
	if msa_clicked == 1:
		val = (Document.Properties["MSAOnChange"] + 1) % 2
		Document.Properties["MSAOnChange"] = val

def reset_to_empty():
	data_tables = ['DL_SelectedThresholds','UL_SelectedThresholds']
	for table in data_tables:
		dt_table = Document.Data.Tables[table]
		threshold_value = Document.Properties["ChosenDLThresholds"]
		if table.startswith('UL'):
			threshold_value = Document.Properties["ChosenULThresholds"]		 
		rows_to_include = IndexSet(dt_table.RowCount,True)
		cursor = DataValueCursor.CreateFormatted(dt_table.Columns["StringVal"])
		count = 0 
		for	 _ in  dt_table.GetRows(rows_to_include,cursor):
			if cursor.CurrentValue == threshold_value:
				count = count +1
		if count == 0:
			if table.startswith('DL'):
				Document.Properties["ChosenDLThresholds"] = ' '
				Document.Properties["DLRange"] = ' '
			else:
				Document.Properties["ChosenULThresholds"] = ' '
				Document.Properties["ULRange"] = ' '  

main()	  
reset_to_empty()	