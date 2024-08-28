#
# The copyright to the computer program(s) herein is the property
# of Ericsson Inc. The programs may be used and/or copied only with
# the written permission from Ericsson Inc. or in accordance with the
# terms and conditions stipulated in the agreement/contract under
# which the program(s) have been supplied.
#
# ********************************************************************
# Name	  : MarkingToDocPropertyHist.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Store the marked nodename value and cell value in document property for cell performance page based on the marking done in cell performance chart.
#
# Usage	  : NR App Coverage

from System.Collections.Generic import List
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Data import DataManager 
from Spotfire.Dxp.Data import IndexSet 
from Spotfire.Dxp.Data import RowSelection 

data_table = Document.Data.Tables["IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW"]
cursor = DataValueCursor.CreateFormatted(data_table.Columns["NR_NAME"])
cursor2 = DataValueCursor.CreateFormatted(data_table.Columns["NRCellDU"])
try:
	markings =Document.ActiveMarkingSelectionReference.GetSelection(data_table)
	marked_data_node = [];
	marked_data_cell = [];

	for row in data_table.GetRows(markings.AsIndexSet(),cursor):
		value = cursor.CurrentValue
		if value != str.Empty:
			marked_data_node.Add(value)

	val_data_node = List [str](set(marked_data_node))
	store_nodes = ', '.join(val_data_node)

	for row in data_table.GetRows(markings.AsIndexSet(),cursor2):
		value = cursor2.CurrentValue
		if value != str.Empty:
			marked_data_cell.Add(value)

	val_data_cell = List [str](set(marked_data_cell))
	store_cells = ', '.join(val_data_cell)

	Document.Properties["NRList2"] = store_nodes
	Document.Properties["CellList2"] = store_cells

except:
	Document.Properties["NRList2"] = ""
	Document.Properties["CellList2"] = ""