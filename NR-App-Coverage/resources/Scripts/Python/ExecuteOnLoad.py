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
# Name	  : ExecuteOnLoad.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : DL/UL Threshold document property update while opening the analysis
#
# Usage	  : NR App Coverage


import System
import Spotfire.Dxp.Application
from Spotfire.Dxp.Data import *
import System.String
from System.Collections.Generic import List
from Spotfire.Dxp.Data import DataValueCursor, IndexSet
from System.Collections.Generic import HashSet



def set_threshold_doc_property():
	if Document.Data.Tables.Contains(data_tablename):
		table = Document.Data.Tables[data_tablename]
		user_input = Document.Properties[control_name]
		row_selection=table.Select('Min='+str(user_input)+'')
		cursor = DataValueCursor.CreateFormatted(table.Columns["Bin values"])
		cursor1 = DataValueCursor.CreateFormatted(table.Columns["Min"])
		bin_val = 0
		for	 _ in	 table.GetRows(row_selection.AsIndexSet(),cursor,cursor1):
			bin_val = cursor.CurrentValue
		Document.Properties[dropdown_docprop_dict[control_name]]  = bin_val

	

dropdown_docprop_dict = {'DLRange1':'DLThreshold1','DLRange2':'DLThreshold2','DLRange3':'DLThreshold3','DLRange4':'DLThreshold4','DLRange5':'DLThreshold5',
'ULRange1':'ULThreshold1','ULRange2':'ULThreshold2','ULRange3':'ULThreshold3','ULRange4':'ULThreshold4','ULRange5':'ULThreshold5'}

control_name_list = ["DLRange1", "DLRange2" ,"DLRange3" ,"DLRange4" ,"DLRange5", "ULRange1", "ULRange2" ,"ULRange3" ,"ULRange4" ,"ULRange5"]

for i in range(len(control_name_list)):
	control_name = control_name_list[i]
	data_tablename = 'DL_ThroughputMap'
	type = 'DL'
	if control_name.startswith('UL'):
		data_tablename = 'UL_ThroughputMap'
		type = 'UL'	
	set_threshold_doc_property()	
		