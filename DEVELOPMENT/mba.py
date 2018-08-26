#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 22-Nov-2017
## Last Modified: 23-Nov-2017
## Version: 1.1
##
## Used to generate item list for each transaction order used for Market Basket Analysis usage.
## 
## Usage: 
## python mba.py <Output Type> <Input File> <Output File>
## <Output Type> : 
##      A - Output the Analysis Category Name instead of the Product Name.
##      M - Output the Product Main Category instead of the Product Name.
##      S - Output the Product Sub-category instead of the Producct Name.
##      P - Output the Product Name.
## 
## Example:
## python mba.py [A|M|S|P] 31102017-extract_orders.csv 31102017-A-mba-source.csv
## python mba.py finfo 31102017-extract_orders.csv
## python mba.py A 31102017-extract_orders.csv 31102017-A-mba-source.csv
## python mba.py S 31102017-extract_orders.csv 31102017-S-mba-source.csv
## python mba.py M 31102017-extract_orders.csv 31102017-M-mba-source.csv
## python mba.py P 31102017-extract_orders.csv 31102017-P-mba-source.csv
## python mba.py A dev-extract_orders.csv 31102017-A-mba-source.csv
##
##
## Output:
## Items list of each order, sperated with ",", each line for 1 order record.
## 
## Version History:
## 22-Nov-2017      Start - define usage and command line. Complete basic data read in skelaton.
## 25-Nov-2017      Fixing output itemlist that having empty items.
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

ALL_CAT = "ALL"
SCRIPT_FN = os.path.basename(__file__)
GENERAL_DEBUG_LOG = SCRIPT_FN + "-debug.log"
LST_GENERAL_DEBUG = []

FULL_CAT = ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']

OUT_TYPE_A = "A"                    ## Output type A - Analysis Category Name
OUT_TYPE_M = "M"                    ## Output type M - Product Main Category
OUT_TYPE_S = "S"                    ## Output type S - Product Sub-category
OUT_TYPE_P = "P"                    ## Output type P - Product Name


IDX_OID = 1                         ## Define the index of order-id field.
IDX_PRD_NAME = 33                   ## Define the index of product name.
IDX_PRD_QTY = 35                    ## Define the index of product quantity.
IDX_MAIN_CAT_NAME = 42              ## Define the index of product main category name.
IDX_SUB_CAT_NAME = 44               ## Define the index of product sub category name.
IDX_MANU_NAME = 46                  ## Define the index of product manufacturer name field.
IDX_ACC_NAME = 48                   ## Define the index of analysis_cateogry_name field.

###############################################################################################
## Function defination
###############################################################################################

####################################################################################################################################################
## Function to dump list into CSV file.
## Input : List, CSV file name.
####################################################################################################################################################
def save_list_to_file(lst_to_save, csv_filename):
    
    with open(csv_filename, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in lst_to_save:
            writer.writerow(val)
    
    output.close()
    
    return


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
        OUT_TYPE_A : lst_rcd[ IDX_ACC_NAME ],
        OUT_TYPE_M : lst_rcd[ IDX_MANU_NAME ],
        OUT_TYPE_S : lst_rcd[ IDX_SUB_CAT_NAME ],
        OUT_TYPE_P : lst_rcd[ IDX_PRD_NAME ],
    }[output_type]


###############################################################################################
## Main program started.
###############################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: all-cat <sale-data-source_csv>"
    print ">> Type 'all-cat help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ All Categories Product Analysis ..."        
        print ">> Usage: all-cat <sale-data-source_csv> "


    elif (sys.argv[1]=='test'):

        print("Test Operation completed!")

    
    elif (sys.argv[1]=='finfo'):
        ## To display the fields info of the source file.
        ## Read in ... order source records 
        source_order_csv = str(sys.argv[2])
        disp_finfo(source_order_csv)
       
        print "\n"
        print("File Info display completed!")


    ## Real operation start.
    else:
        ## Getting the parameters ...
        output_type = str(sys.argv[1])
        source_order_csv = str(sys.argv[2])
        output_csv = sys.argv[3]

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
        
        ## Output the list item.
        lst_output = []
        for e in dict_order.keys():
            if( len(dict_order[e]) > 0 ):
                lst_output.append(dict_order[e])

        ## Output to file.
        save_list_to_file(lst_output, output_csv)
        print "Successfully output list items to %s. \n" % (output_csv)
        
        print("Operation completed!")