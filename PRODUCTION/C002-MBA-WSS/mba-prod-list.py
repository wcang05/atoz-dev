#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 13-Feb-2018
## Last Modified: 13-Feb-2018
## Version: 1.0
## Filename: mba-prod-list.py
##
## Example:
## python mba-prod-list.py P WSS_Censored_Data.csv wss-mba-source.csv
## python mba-prod-list.py C WSS_Censored_Data.csv wss-mba-source.csv
## python finfo mba-prod-list.py
##
## Product Item list per order in a list for MBA - Data source: WSS Advert.
## 22-Feb-18    Construct read in data.
##
## 
## 
## 
######################################################################################################

## Imports packages
import os
import sys
import csv
import copy

####################################################################################################################################################
## Global constants
####################################################################################################################################################
## Debuging flag
## DF = True
DF = False
LOG_DF = True

SCRIPT_FN = os.path.basename(__file__)
GENERAL_DEBUG_LOG = SCRIPT_FN + "-debug.log"
LST_GENERAL_DEBUG = []

IDX_OID = 1             ## Define the index of order-id field.
IDX_PRD_NAME = 4        ## Define the index of product name.
IDX_PRD_CODE = 5        ## Define the index of product code.
IDX_PRD_QTY = 6         ## Define the index of product quantity.

OUT_TYPE_P = "P"        ## Output type P - Product Name
OUT_TYPE_C = "C"        ## Output type C - Product Code


###############################################################################################
## Function defination
###############################################################################################

####################################################################################################################################################
## For displaying the file info, fields index, and the sample data of 1 record.
## Input  : The source filename.
## Output : None. To Console for information display. 
####################################################################################################################################################
def disp_finfo(src_file):

    print "Read in [%s]..." % (src_file)
    with open(src_file, 'r') as f_order:
        reader = csv.reader(f_order)
        lst_order_rcd = list(reader)
    ttl_rcd = len(lst_order_rcd)
    last_idx = ttl_rcd - 1
    print "Successfully read in %s with lines %s\n" % (src_file, str(ttl_rcd))

    ## Test print and access element.
    print "Header input = %s\n" % (lst_order_rcd[0])
    print "Line no. %d = %s\n" % (ttl_rcd, lst_order_rcd[last_idx])
    print "Line no. %d = %s, Item no.2 : %s" % (ttl_rcd, lst_order_rcd[last_idx], lst_order_rcd[last_idx][1])
    print ""

    ## Output Field numbers mapped to each header.
    print "%6s - %27s - %s" % ("Index", "Header", "Sample Data")
    print "%6s - %27s - %s" % ("-----", "------", "-----------")
    for idx, fn in enumerate(lst_order_rcd[0]): 
        print "%6d - %27s - %s" % (idx, fn, lst_order_rcd[last_idx][idx])

    return


####################################################################################################################################################
## For deciding and return the configured output item type in list item.
## Input  : record list, configured output type.
## Output : return the list item match with the configured output type.
####################################################################################################################################################
def output_item(lst_rcd, output_type):
    return {
        OUT_TYPE_P : lst_rcd[ IDX_PRD_NAME ],
        OUT_TYPE_C : lst_rcd[ IDX_PRD_CODE ],
    }[output_type]

###############################################################################################
## Main program started.
###############################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: mba-prod-list.py <sale-data-source_csv> <output_list_csv>"
    print ">> Type 'mba-prod-list help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> Produce product list for WSS data source ..."
        print ">> Usage: mba-prod-list.py <sale-data-source_csv> <output_list_csv>"

    elif (sys.argv[1]=='test'):
        ## Testing area.
        print("Testing area completed!")
    
    elif (sys.argv[1]=='finfo'):
        ## To display the fields info of the source file.
        ## Read in ... order source records 
        source_order_csv = str(sys.argv[2])
        disp_finfo(source_order_csv)
       
        print "\n"
        print("File Info display completed!")


    else:
        ## Real operation start.        
        output_type = str(sys.argv[2])
        source_order_csv = str(sys.argv[3])
        output_csv = str(sys.argv[4])

        ## Defining variables.
        lst_order_rcd = []         ## Original read in order record list.

        ## Command inputs validation ...
        print "--- Inputs Command Validation ---" 
        print "Output Type set : %s" % (output_type)
        print "Source file : %s" % (source_order_csv)
        print "Output file : %s" % (output_csv)
        
        print "\n"
        print "Read in [%s]..." % (source_order_csv)
        with open(source_order_csv, 'r') as f_order:
            reader = csv.reader(f_order)
            lst_order_rcd = list(reader)
            ttl_rcd = len(lst_order_rcd)
        last_idx = ttl_rcd - 1
        print "Successfully read in %s with lines %s\n" % (source_order_csv, str(ttl_rcd))

        ## Putting source in Order Records Data Structure.
        dict_order = {}
        
        ## Initialize process counter.
        proc_ctr = 1        
        
        ## Skip the header element.
        for rcd in lst_order_rcd[1:]:                   
            order_id = rcd[ IDX_OID ]
            prd_qty = int( rcd[ IDX_PRD_QTY ] )
            curr_item = output_item( rcd, output_type )

            if( not (order_id in dict_order.keys()) ):
                dict_order[order_id] = []
            
            if ( curr_item ):
                lst_tmp = [curr_item] * prd_qty
                dict_order[order_id].extend(lst_tmp)
            
            proc_ctr = proc_ctr + 1
            op_pp = float(proc_ctr*100) / float(len(lst_order_rcd))
            print "Processing source records to order [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_order_rcd), op_pp),
    
        ## Complete processing
        print "\n"
        print "Successfully processed %s number of oders. \n" % (str(len(dict_order.keys())))

        
        print("Operation completed!")



