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
# Name	  : PageNavigateRefreshDocProperty.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Clear NRList when navigating to NR cell site loaction
#
# Usage	  : NR App Coverage

from System.Collections.Generic import List
from Spotfire.Dxp.Data import *


def clear_marking():					
	Document.Properties["NRList"] = ""
	Document.Properties["CellList1"] = ""
	dataTable = Document.Data.Tables["IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW"]
	marking=Application.GetService[DataManager]().Markings["NR"]
	selectRows = IndexSet(dataTable.RowCount, False)
	marking.SetSelection(RowSelection(selectRows),dataTable)

def	check_marking():
	if Document.Properties["NRList2"] == "":
		clear_marking()		
	else:
		count = 0
		cell_list_chart = ''
		cell_list_map = Document.Properties["CellList1"]
		cell_list_chart = Document.Properties["CellList2"]
			
		cell_list_map_tmp = cell_list_map.split(', ')
		cell_list_bar_tmp = cell_list_chart.split(', ')	   

		for cell in cell_list_map_tmp:
			if cell in cell_list_bar_tmp:
				count = count+1

		if count !=	len(cell_list_map_tmp):
			clear_marking()
	
def navigate_page():
	for page in Document.Pages:
		if (page.Title == 'NR Cell Site Location'):		
			Document.ActivePageReference=page	
				
check_marking()						
navigate_page()
			
		
			
			
				