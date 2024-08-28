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
# Name	  : updateVisualicationWithSelectedThreshold.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Update the target title and DL/UL range (used in calculation) document property with selected threshold
#
# Usage	  : NR App Coverage

from System.Collections.Generic import List
from Spotfire.Dxp.Data import DataValueCursor, IndexSet
import System
import Spotfire.Dxp.Application
from Spotfire.Dxp.Data import *
import System.String


data_tablename = 'DL_SelectedThresholds'# default
selected_threshold_string = Document.Properties['ChosenDLThresholds']
type = 'DL'

if controlName.startswith('ChosenUL'):
	data_tablename = 'UL_SelectedThresholds'
	selected_threshold_string = Document.Properties['ChosenULThresholds']
	type = 'UL'
Document.Properties['TargetTitle'] =  selected_threshold_string

def set_current_threshold_in_doc_prop():
	if Document.Data.Tables.Contains(data_tablename):
		table = Document.Data.Tables[data_tablename]
		user_input = selected_threshold_string
		data_values_cursor = DataValueCursor.CreateFormatted(table.Columns["StringVal"])
		input_cursor = DataValueCursor.CreateFormatted(table.Columns["Input"])
		input_in = ''
		for  _ in  table.GetRows(data_values_cursor,input_cursor): # Will be one row only
			if user_input == data_values_cursor.CurrentValue:
				input_in = input_cursor.CurrentValue
				
		if type == 'DL':
		  Document.Properties['DLRange'] =  input_in	
		else:
		  Document.Properties['ULRange'] =  input_in

set_current_threshold_in_doc_prop()

