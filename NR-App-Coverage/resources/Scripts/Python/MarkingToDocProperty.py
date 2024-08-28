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
# Name	  : MarkingToDocProperty.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Store the marked nodename value in a document property for cell site location map chart
#
# Usage	  : NR App Coverage

from System.Collections.Generic import List
from Spotfire.Dxp.Data import *

data_table = Document.Data.Tables["IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW"]
cursor = DataValueCursor.CreateFormatted(data_table.Columns["NR_NAME"])
cursor2 = DataValueCursor.CreateFormatted(data_table.Columns["NRCellDU"])


try:
	markings =Document.ActiveMarkingSelectionReference.GetSelection(data_table)
	marked_data = []
	marked_data_cell = [];

	for row in data_table.GetRows(markings.AsIndexSet(), cursor):
		value = cursor.CurrentValue
		if value != str.Empty:
			marked_data.Add(value)

	val_data = List [str](set(marked_data))
	store_nodes = ', '.join(val_data)
	
	for row in data_table.GetRows(markings.AsIndexSet(),cursor2):
		value = cursor2.CurrentValue
		if value != str.Empty:
			marked_data_cell.Add(value)

	val_data_cell = List [str](set(marked_data_cell))
	store_cells = ', '.join(val_data_cell)
	
	Document.Properties["NRList"] = store_nodes
	Document.Properties["CellList1"] = store_cells
	
except:
	Document.Properties["NRList"] = ""
	Document.Properties["CellList1"] = ""
