#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 08-Nov-2017
## Last Modified: 08-Nov-2017
## Version: 1.0
##
## Functional Description :
## 1. Changing the file names in the list, take the content, re-define the output header and fields.
## 2. Output to a argument defined filename.
## 3. Happen in the same directory.
##
######################################################################################################

## Imports packages
import os
import sys
import csv
import copy

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

###############################################################################################
## Function defination
###############################################################################################
def define_cust_bhv_gap_aa_header():
    return [
            ["Rcd_Idx", "Cust_ID", "Firtname", "Lastname", "Tel", "PCode", "Cpny/Ind", 
             "Min Spt Gap", "Latest Manu", "Dataset Year"]
           ]


def process_cust_bhv_gap_aa(lst_output, lst_bhv_gap_in):
    
    IDX_CUST_ID = 0
    IDX_FN = 1
    IDX_LN = 2
    IDX_TEL = 3
    IDX_PCODE = 4 
    IDX_CPNY_IND = 5
    IDX_MIN_SPT_GAP = 6
    IDX_LATEST_MANU = 14
    IDX_DATASET_YEAR = 15

    index_rcd = len(lst_output)
    
    for rcd in lst_bhv_gap_in[1:]:
        lst_output.append([
                           str(index_rcd), 
                           rcd[ IDX_CUST_ID ],
                           rcd[ IDX_FN ],
                           rcd[ IDX_LN ],
                           rcd[ IDX_TEL ],
                           rcd[ IDX_PCODE ],
                           rcd[ IDX_CPNY_IND ],
                           rcd[ IDX_MIN_SPT_GAP ],
                           rcd[ IDX_LATEST_MANU ],
                           rcd[ IDX_DATASET_YEAR ]
                          ])
        index_rcd = index_rcd + 1
    
    return

###############################################################################################
## Main program started.
###############################################################################################
## Clear console screen for operations
os.system('cls')

## Real operation start.
lst_input_files = []
lst_input_files.append("[All]-cust-bhv-aa.csv")
lst_input_files.append("[2015-2017]-cust-bhv-aa.csv")
lst_input_files.append("[2016-2017]-cust-bhv-aa.csv")
lst_input_files.append("[2017-Latest]-cust-bhv-aa.csv")

output_filename = "b_cust_bhv_gap_aa.csv"

## Gather all the records for output and attached with an index.            
lst_output = define_cust_bhv_gap_aa_header()

## Read in all configured filename
for fn in lst_input_files:
    print "Read in [%s]..." % (fn)
    with open(fn, 'r') as f_order:
        reader = csv.reader(f_order)
        lst_rcd = list(reader)
    ttl_rcd = len(lst_rcd)
    last_idx = ttl_rcd - 1
    print "Successfully read in %s with lines %s" % (fn, str(ttl_rcd))

    ## Checking current output counter.
    print "Current output list record lines %s" % (str(len(lst_output)))
    
    ## Putting ID and combined output operation.
    process_cust_bhv_gap_aa(lst_output, lst_rcd)
    print "Successfully combined %s with current total record lines %s\n\n" % (fn, str(len(lst_output)))
    

## Output list into file.
save_list_to_file(lst_output, output_filename)

print "Completed output to file : %s\n" % output_filename

print("Operation completed!")



