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
# Name	  : ReConfigureMSA.py
# Date	  : 12/04/2024
# Revision: 1.0
# Purpose : Configure the Multi System access
#
# Usage	  : NR App Coverage

from Spotfire.Dxp.Data.DataOperations import DataSourceOperation
from Spotfire.Dxp.Application import DocumentMetadata
from Spotfire.Dxp.Data.DataOperations import DataOperation
from Spotfire.Dxp.Application.Visuals import HtmlTextArea
from Spotfire.Dxp.Framework.Library import LibraryManager, LibraryItemType, LibraryItem, LibraryItemRetrievalOption
lm = Application.GetService(LibraryManager)
from Spotfire.Dxp.Data import *
from Spotfire.Dxp.Data.Import import *
from Spotfire.Dxp.Data.DataOperations import *
from System import Array,Guid,String,Object, DateTime
from Spotfire.Dxp.Data.Transformations import *
from Spotfire.Dxp.Data.DataOperations import *
from System.Collections.Generic import List
from Spotfire.Dxp.Framework.ApplicationModel import *
from System.Collections.Generic import Dictionary,List
from System import Guid
service = Application.GetService[LibraryManager]()
service1 = Application.GetService[LibraryManager]()
dm=Application.GetService(DataManager)
import sys
import re
from Spotfire.Dxp.Application import DocumentMetadata
from Spotfire.Dxp.Framework.Library import LibraryManager, LibraryItemRetrievalOption, LibraryItemType, LibraryItem
dmd = Application.DocumentMetadata
libraryManager = Application.GetService[LibraryManager]()
from Spotfire.Dxp.Application.Scripting import ScriptDefinition
from System.Collections.Generic import Dictionary
import clr




def validate_ds_name(ds2):
	"""Validate folder created with data source name for MSA configuration
	Arguments:
		table_properties {string} -- data source name given as input
	Returns:
		table_properties {integer} -- returns integer value (valid or invalid) 1 or 0 
	"""
	ericsson_library = "Ericsson Library"
	analysis_path = []
	is_valid = 0
	path = str(dmd.LoadedFromLibraryPath)
	sub = path.rfind("/") + 1 
	length = len(path) 
	analysis = path[sub:length]
	
	dxps = libraryManager.Search("type:dxp",LibraryItemRetrievalOption.IncludePath,LibraryItemRetrievalOption.IncludeProperties)
	for dxp in dxps:
		if analysis in dxp.Title and ericsson_library in dxp.Path: 
			analysis_path.append(dxp.Path)
	for p in analysis_path:
		if ds2 in p:
			is_valid = 1
	return is_valid

def create_ds2_tables(tbl,op,list_tables,new_il_paths,list_ds2_tables,ds2_itr):
	"""
	This gives the GUID of table/Info Link
	"""
	if tbl.Name not in table_list:
		list_tables.append(tbl.Name)
	
	if type(op[0]).__name__ == 'DataSourceOperation' or type(op[0]).__name__ == 'InformationLinkOnDemandOperation':
		if type(op[0]).__name__ == 'DataSourceOperation':
			t=op[0].GetDataFlow().DataSource
		elif type(op[0]).__name__ == 'InformationLinkOnDemandOperation':
			t = InformationLinkDataSource(op[0].InformationLinkId)
		if(type(t).__name__	 == "InformationLinkDataSource"):
			found=t.FindAll("id::"+str(t.Id))
			path = found.First.Path
			dt_il_len = path.rfind("/")+1
			length = len(path)
			dt_il_name = path[dt_il_len:length]		
			infolink_path = path[0:dt_il_len]
			if "MSA" in infolink_path:
				path_part = infolink_path.split("MSA")[0]
				new_il_path = path_part + "MSA/"+ ds2_itr + "/Information Package/Information Links/"+dt_il_name
				new_il_paths.append(new_il_path)
				dt_il_ds2_name = tbl.Name + "_" + ds2_itr
				list_ds2_tables.append(dt_il_ds2_name)
			else:
				Document.Properties["errorMsg"] = "Ensure you are in MSA library folder path."
			
	
	
def get_table_transformations(ds1_table_name,c):
	"""
	Get Calculate New Value Transofrmation
	"""
	
	table_ds1 = Document.Data.Tables[ds1_table_name]
	sourceview=table_ds1.GenerateSourceView()
	
	
	for op in sourceview.OperationsSupportingTransformations:
		for t in op.GetTransformations():
			if t.Name == "Calculate new column":
				c = c +1
				ds2_result_column_name.append(t.ResultColumnName)
				ds2_expression.append(t.Expression)
	return c

def add_table_transformations(ds2_table_name,ds2_result_column_name,ds2_expression,c):
	"""
	Add the calculated column
	"""
	table_ds2 = Document.Data.Tables[ds2_table_name]
	i=0
	while c >0:
		calc_column =  AddCalculatedColumnTransformation(ds2_result_column_name[i],ds2_expression[i])
		calc_column.ResultColumnName = ds2_result_column_name[i]
		calc_column.Expression = ds2_expression[i]
		table_ds2.AddTransformation(calc_column)
		i = i +1
		c = c - 1
	
def add_table_relations(ds1_table_name, ds2_table_name,ds2_itr):
	"""
	Add Relations for secondary data sources
	"""
	table_ds1 = Document.Data.Tables[ds1_table_name]
	existing_relations=dm.Relations.FindRelations(table_ds1)
	relation_len = len(existing_relations)
	i = 0
	while relation_len > 0:
		for _ in existing_relations:
			relation = existing_relations[i]
			relation_expr= relation.Expression
			relation_left_table = relation.LeftTable.Name
			relation_right_table = relation.RightTable.Name
			relation_left_table_ds2 = relation_left_table + "_" + ds2_itr
			relation_right_table_ds2 = relation_right_table + "_" + ds2_itr
			relation_expr_ds2 = relation_expr.replace(relation_left_table, relation_left_table_ds2)
			relation_expr_ds2 = relation_expr_ds2.replace(relation_right_table, relation_right_table_ds2)
			table_left = Document.Data.Tables[relation_left_table_ds2]
			table_right = Document.Data.Tables[relation_right_table_ds2]
			if dm.Relations.FindRelation(table_left,table_right) == None:
				Document.Data.Relations.Add(table_left, table_right,relation_expr_ds2)
		i = i +1
		relation_len = relation_len -1
	

def add_rows(ds1_table_name,ds2_table_name):
	"""
	Copy rows to new data table
	"""
	table_ds1 = Document.Data.Tables[ds1_table_name]
	table_ds2 = Document.Data.Tables[ds2_table_name]
	row_col_collection_array_ext = []
	row_col_collection_array = []
	
	data_source=DataTableDataSource(table_ds2)
	col1_collection = table_ds1.Columns
	for col in col1_collection:
		row_col_collection_array_ext.append(col.Properties.ExternalName)
		row_col_collection_array.append(str(col.Properties.Name))
	
	rowsettings=AddRowsSettings(table_ds1,data_source)#,'Origin','addRowSourceCol')
	table_ds1.AddRows(data_source,rowsettings)
		

def col_check(ds1_table_name,ds2_table_name):
	table_ds1 = Document.Data.Tables[ds1_table_name]
	table_ds2 = Document.Data.Tables[ds2_table_name]
	tabl1_col_collection = table_ds1.Columns
	tabl2_col_collection = table_ds2.Columns
	col1_name = []
	col1_ext_name = []
	for col1 in tabl1_col_collection:
		if str(col1.Properties.ColumnType) == 'Imported' or str(col1.Properties.Name) == 'DataSource':
			col1_name.append(str(col1.Properties.Name))
			col1_ext_name.append(col1.Properties.ExternalName)
	i = 0
	for col2 in tabl2_col_collection:
		if str(col2.Properties.Name) == col1_ext_name[i] and col1_ext_name[i] != col1_name[i]:
			col2.Properties.Name = col1_name[i]
		i = i+1
		
 
def get_column_details(table_ds2,table3,map1):
	"""
	Get column details and check all columns are available
	"""
	col_ds2_array = []
	col_ds3_array = []
	col_ds2 = table_ds2.Columns
	for col in col_ds2:
		col_ds2_array.append(str(col))
	col_ds3 = table3.Columns
	for col in col_ds3:
		col_ds3_array.append(str(col))
	for val in map1 :
		col_ds3_array.remove(str(val.Value))
	result = all(elem in col_ds2_array for elem in col_ds3_array)
	
	return result
		
def insert_columns(ds1_table_name,ds2_table_name,ds2_itr):
	"""
	Insert Columns - Get insert columns info
	"""
	table_ds1 = Document.Data.Tables[ds1_table_name]
	table_ds2 = Document.Data.Tables[ds2_table_name]
	for operation in table_ds1.GenerateSourceView().GetAllOperations[AddColumnsOperation]():
		join_type = operation.AddColumnsSettings.JoinType
		map1 = operation.AddColumnsSettings.Map
		ls = operation.Inputs
		
		if type(ls[1]).__name__	 == "DataTableDataSourceOperation":
			dest_table_ds1 = ls[1].DataTable.Name
			dest_table_ds2 = dest_table_ds1 + "_" + ds2_itr
			table3 = Document.Data.Tables[dest_table_ds2]
			data_source=DataTableDataSource(table3)
		elif type(ls[1]).__name__ == "DataSourceOperation":
			t=ls[1].GetDataFlow().DataSource
			if(type(t).__name__	 == "InformationLinkDataSource"):
				found=t.FindAll("id::"+str(t.Id))
				path = found.First.Path
				length = len(path)
				dt_il_len = path.rfind("/")+1
				dest_table_ds1 = t.Name
				dest_table_ds2 = dest_table_ds1 + "_" + ds2_itr
				table3 = Document.Data.Tables[dest_table_ds2]
				dt_il_name = path[dt_il_len:length]
				info_link_path = path[0:dt_il_len]
				path_part = info_link_path.split("MSA")[0]
				new_il_path_src = path_part + "MSA/"+ ds2_itr + "/Information Package/Information Links/"+dt_il_name
				(found, item) = service1.TryGetItem(new_il_path_src, LibraryItemType.InformationLink, LibraryItemRetrievalOption.IncludeProperties)
				il_guid = str(item.Id)
				data_source = InformationLinkDataSource(Guid(il_guid))
		elif type(ls[1]).__name__ == "DataTransformationsOperation":
			continue
			
		result = get_column_details(table_ds2,table3,map1)
		add_column_to_table(table_ds2,table3,ds1_table_name,ds2_table_name,data_source,result,map1,join_type)		
		

def add_column_to_table(table_ds2,table3,ds1_table_name,ds2_table_name,data_source,result,map1,join_type):
	map_dict=Dictionary[DataColumnSignature,DataColumnSignature]()
	if result:
		print ("Columns already added")
	else:
		for kvp in map1 :
			map_dict.Add(DataColumnSignature(table_ds2.Columns[str(kvp.Key)]),DataColumnSignature(table3.Columns[str(kvp.Value)]))
		ignored_columns=List[DataColumnSignature]()
		new_settings=AddColumnsSettings(map_dict,join_type,ignored_columns)
		columns_changed_result = table_ds2.AddColumns(data_source,new_settings)
		col_check(ds1_table_name,ds2_table_name)
	map_dict.Clear()	   

def check_msa_configured(dp_name): 
	"""
	Check MSA configured already or not and if not configured create a custom document property
	"""
	chk_duplicate_flag = 0 
	if Document.Data.Properties.ContainsProperty (DataPropertyClass.Document,dp_name):
		Document.Properties["errorMsg"] = 'MSA already configured for Data Source' 
		chk_duplicate_flag = 1
	else:
		prop   = DataProperty.CreateCustomPrototype(dp_name,DataType.String, DataProperty.DefaultAttributes) 
		Document.Data.Properties.AddProperty(DataPropertyClass.Document, prop) 
		Document.Properties[dp_name]  = "False"
	return chk_duplicate_flag	 

def check_create_ds2_tables(ds2,ds2_itr):
	"""
	Check tables to be created for secondary data sources
	"""
	list_tables =[]
	new_il_paths =[]
	list_ds2_tables =[]
	for tbl in Document.Data.Tables:
		source_view = tbl.GenerateSourceView();
		op=source_view.GetAllOperations[DataOperation]()
		if any(ds in tbl.Name for ds in ds2):
			print("Table exists")
		else:
			create_ds2_tables(tbl,op,list_tables,new_il_paths,list_ds2_tables,ds2_itr)
	return list_tables,new_il_paths,list_ds2_tables		  

def add_indiviual_doc_prop():
	"""
	Add individual document property as parameter for information link
	"""
	
	il_parameters = []										
	values = [Document.Properties['DLThreshold1']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("DLThreshold1", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['DLThreshold2']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("DLThreshold2", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['DLThreshold3']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("DLThreshold3", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['DLThreshold4']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("DLThreshold4", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['DLThreshold5']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("DLThreshold5", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['ULThreshold1']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("ULThreshold1", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['ULThreshold2']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("ULThreshold2", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['ULThreshold3']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("ULThreshold3", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['ULThreshold4']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("ULThreshold4", Array[object](values))
	il_parameters.append(il_parameter1)
	values = [Document.Properties['ULThreshold5']]
	il_parameter1 = InformationLinkParameter.CreateNamedParameter("ULThreshold5", Array[object](values))
	il_parameters.append(il_parameter1)
	
	return il_parameters

def add_doc_prop_to_il(ilpath,list_tables,new_il_paths,list_ds2_tables,counter_config):
	"""
	Add or replace document property as parameter for information link
	"""
	path = new_il_paths[ilpath]
	ds1_table_name = list_tables[ilpath]
	ds2_table_name = list_ds2_tables[ilpath]
	(found, item) = service.TryGetItem(path, LibraryItemType.InformationLink, LibraryItemRetrievalOption.IncludeProperties)
	if item is None:
		Document.Properties["errorMsg"] = "Ensure you are in MSA library folder path."
		sys.exit("")
	il_guid = str(item.Id)
	information_link_data_source = InformationLinkDataSource(Guid(il_guid))
	if Document.Data.Tables.Contains(ds2_table_name):
		if ('IL_DC_E_NR_EVENTS_NRCELLDU_V_DAY' in ds2_table_name or 'IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW' in ds2_table_name):
			counter_config = 1		
			il_parameters = add_indiviual_doc_prop()
			information_link_data_source.Parameters = il_parameters
			information_link_data_source.IsPromptingAllowed = True
			Document.Data.Tables[ds2_table_name].ReplaceData(information_link_data_source)
			Document.Data.Tables[ds2_table_name].RefreshOnDemandData()	  
		else:
			print ("Table exists")
	else:
		if 'IL_DC_E_NR_EVENTS_NRCELLDU_V_DAY' in ds2_table_name or 'IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW' in ds2_table_name:										
			il_parameters = add_indiviual_doc_prop()	
			information_link_data_source.Parameters = il_parameters
			information_link_data_source.IsPromptingAllowed = True
			Document.Data.Tables.Add(ds2_table_name, information_link_data_source)
			Document.Data.Tables[ds2_table_name].RefreshOnDemandData()
		else:
			Document.Data.Tables.Add(ds2_table_name, information_link_data_source)	
	return counter_config
	
def process_all_operation(chk_duplicate_flag,run_flag,ds2,ds2_itr,valid_ds):
	"""
	Process all the function inserting column, adding table relation, adding calculated column and add rows
	"""
	if ((chk_duplicate_flag == 0) or (chk_duplicate_flag == 1)):
		if run_flag == 1:	
			list_tables,new_il_paths,list_ds2_tables = check_create_ds2_tables(ds2,ds2_itr)
			length=len(new_il_paths)
			ds2_table_len = len(list_ds2_tables)
			counter_config = 0 
			for ilpath in range(length):
				counter_config = add_doc_prop_to_il(ilpath,list_tables,new_il_paths,list_ds2_tables,counter_config)					
			for table in range(ds2_table_len):						
				table_ds1 = list_tables[table]
				table_ds2 = list_ds2_tables[table]
				insert_columns(table_ds1,table_ds2,ds2_itr)
				add_table_relations(table_ds1,table_ds2,ds2_itr)
				ds2_expression = []
				ds2_result_column_name = []
				count = 0
				count = get_table_transformations(table_ds1,count)
				add_table_transformations(table_ds2,ds2_result_column_name,ds2_expression,count)
				if ('IL_DC_E_NR_EVENTS_NRCELLDU_V_DAY' in table_ds1 or 'IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW' in table_ds1) and counter_config == 0:
					add_rows(table_ds1,table_ds2)
				Document.Data.Tables[table_ds1].ReloadLinkedData()
				property_name = "addRows"+ds2_itr
				Document.Properties[property_name]	 = "True"
	if Document.Properties["addRows"+ds2_itr] == "True":
		Document.Properties["errorMsg"] = "MSA Configuration done for data Sources: " +	 str(valid_ds)
		# Setting flag(document property to check if the MSA configuration button is been clicked for the first time or not
		Document.Properties["MSAButtonClicked"] = 1
						   
def remove_sec_table_in_filter_panel():
	for page in Application.Document.Pages:
		filterPanel = page.FilterPanel
		for group in filterPanel.TableGroups:
			if group.Name != "IL_DC_E_NR_EVENTS_NRCELLDU_V_RAW" and group.Name != "IL_DC_E_NR_EVENTS_NRCELLDU_V_DAY" :
				for filter in group.FilterHandles:
					filter.Visible = False


def main():
	"""
	Starting of the script, Calls the main function
	"""
	no_of_data_sources = Document.Properties["noOfDataSources"]
	ds_name_list = Document.Properties["DSNameList"]
	ds2 = []
	exit_flag = 0
	count_operation = 0
	valid_ds = []
	if ds_name_list != " ":
		for x in ds_name_list.split('\n'):
			if x != '':
				ds2.append(x.strip())
		ds_length = len(ds2) 
		if ds_length == int(no_of_data_sources):
			for i in range(ds_length):
				if exit_flag == 0:			   
					flag = 0
					run_flag = 0		   
					if ds2[i] == '' or ds2[i].isalnum()!= True:
						Document.Properties["errorMsg"] = "Data Source name must be alpha numeric."
						exit_flag = 1
					else:
						flag = validate_ds_name(ds2[i])
						if flag == 0:
							Document.Properties["errorMsg"] = 'Invalid data source name!'
							exit_flag = 1
						else:
							run_flag = 1
							valid_ds.append(ds2[i])
							Document.Properties["errorMsg"] = ''
							dp_name	 = "addRows" + str(ds2[i])
							chk_duplicate_flag = check_msa_configured(dp_name)
							process_all_operation(chk_duplicate_flag,run_flag,ds2,ds2[i],valid_ds)
							
				else:
					Document.Properties["errorMsg"] = 'Invalid data source name!'
			remove_sec_table_in_filter_panel()		
		else:
			Document.Properties["errorMsg"] = 'Mismatch in number of data sources'
	else:
		Document.Properties["errorMsg"] = 'Enter the required data source name'
table_list = ['DL_ThroughputMap', 'UL_ThroughputMap', 'DL_SelectedThresholds', 'UL_SelectedThresholds']

main()
