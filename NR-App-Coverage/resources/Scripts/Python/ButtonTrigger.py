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
# Name	  : ButtonTrigger.py
# Date	  : 04/04/2024
# Revision: 1.0
# Purpose : Update the document property of DSNameList to empty when no input given in the DSNameList text box
#
# Usage	  : NR App Coverage

value=Document.Properties["DSNameList"]

if value=="":
	Document.Properties["DSNameList"]=" "