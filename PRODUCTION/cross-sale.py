#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################################
## Author SY
## Start Date: 28-Feb-2018
## Last Modified: 28-Feb-2018
## Version: 1.0
##
## cross-sale.py - Generate data for calculating cross-sale dashboard.
## 
##
## Usage Example:
## python cross-sale.py 31122017-extract_orders.csv ALL all_cust_bhv_lod_aa.csv
##
## Version History:
## 28-Feb-2017      Start - define usage and command line. Complete module, basic data read in skelaton.
## 
######################################################################################################################

## Imports packages
import os
import sys
import csv
import copy
import datetime
import platform
from pprint import pprint
from dateutil import parser

####################################################################################################################################################
## Program Configuration Parameters
####################################################################################################################################################
## Code for data.
CODE_CPNY = "CPNY"                  ## Code to indicate company customer - CPNY
CODE_IND = "IND"                    ## Code to indicate individual customer - IND

## Customer Level Dictionary Keys holding info.
## Dictionary Variable : dict_cust_data
CUST_KEY_INFO = "CUST_INFO"         ## Customer dictionary key for holding customer info. Holding a list.
                                    ## List of items = [Firstname, Lastname, Tel, Postcode, CPNY/IND]
CUST_KEY_ORDER = "CUST_ORD"         ## Customer dictionary key for holding the list of ORDER DICTIONARY.

IDX_OID = 1                         ## Define the index of order-id field.
IDX_FN = 7                          ## Define the index of first name field.
IDX_LN = 8                          ## Define the index of last name field.
IDX_E = 9                           ## Define the index of email field.
IDX_TEL = 10                        ## Define the index of telephone field.
IDX_PCODE = 13                      ## Define the index of postcode field.
IDX_TTL = 20                        ## Define the index of order total field.
IDX_YR = 29                         ## Define the index of year field.
IDX_ADDDATE = 26                    ## Define the index of date added field.
IDX_QTR = 27                        ## Define the index of quarter field.
IDX_MTH = 28                        ## Define the index of month field.
IDX_TTL_QTY = 31                    ## Define the index of total quantity field.
IDX_PRD_NAME = 33                   ## Define the index of product name.
IDX_PRD_MDL = 34                    ## Define the index of product model.
IDX_PRD_QTY = 35                    ## Define the index of product quantity.
IDX_PRD_P = 36                      ## Define the index of product price.
IDX_PRD_TTL = 37                    ## Define the index of product total.
IDX_PRD_SUB_CAT = 44                ## Define the index of product sub category name.
IDX_MANU = 46                       ## Define the index of product manufacturer name field.
IDX_ACC = 49                        ## Define the index of analysis_cateogry_code field.

## Order level Dictionary Keys holding info.
## Dictionary Variable : dict_order, dict_order_detail
## dict_order holding the order-id as key, attached with dict_order_detail
KEY_ORD_TTL = "ORDER_TOTAL"         ## Holding the information of product total per order in a dictionary instance.
KEY_ORD_YR = "ORDER_YEAR"           ## Holding the information of order year in a dictionary instance.
KEY_ORD_QT = "ORDER_QUATER"         ## Holding the information of order quarter in a dictionary instance.
KEY_ORD_MT = "ORDER_MONTH"          ## Holding the information of order month in a dictionary instance.
KEY_ORD_DAY = "ORDER_DAY"           ## Holding the information of order day in a dictionary instance.
KEY_ORD_ADDDT = "ORDER_ADDDATE"     ## Holding the information of order added date in a dictionary instance.
KEY_ORD_QTY = "ORDER_TTL_QTY"       ## Holding the information of order total quantity in a dictionary instance.
KEY_ORD_CAT = "ORDER_CAT"           ## Holding a list that contains all purchased items categories in the order.
KEY_ORD_MANU = "ORDER_MANU"         ## Holding the information of order manufacturing in the order.
KEY_ORD_ITEMS = "ORDER_ITEMS"       ## Holding the information of order items in a specific order.

## Order item dictionary keys for holding information.
## Dictionary Variable: dict_order_item.
## dict_order_item will be appended in a KEY_ORDER_ITEMS list, attached in dict_order_detail.
KEY_PRD_NAME = "PRD_NAME"           ## Holding the information of order item, product name.
KEY_PRD_QTY = "PRD_QTY"             ## Holding the information of order item, product quantity purchased.
KEY_PRD_P = "PRD_PRICE"             ## Holding the product sale price.
KEY_PRD_TTL = "PRD_TTL"             ## Holding the product total price, product price x quantity.
KEY_PRD_MANU = "PRD_MANU"           ## Holding the product manufacturer information.
KEY_PRD_SUB_CAT = "PRD_SUB_CAT"     ## Holding the product sub category.
KEY_PRD_MDL = "PRD_MODEL"           ## Holding the product model.
KEY_PRD_ACC = "PRD_ACC"             ## Holding the product analysis_category_code.

## Data structure to hold customer Last Order Days (LOD)
## Taking Customer-Level Info Key (Email / Tel) as dictionary key.
## LOD related keys defination.
KEY_LOD = "LOD"                     ## Holding the Last Order Days, the number of days from current date.

####################################################################################################################################################
## Global constant
####################################################################################################################################################
## Debuging flag
## DF = True
DF = False
LOG_DF = True

SCRIPT_FN = os.path.basename(__file__)
GENERAL_DEBUG_LOG = SCRIPT_FN + "-debug.log"
LST_GENERAL_DEBUG = []

FULL_CAT = ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']
ALL_CAT = "ALL"


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
## Function to filter the analysis category.
## Skip the record only if empty email and empty telephone number.
## Input : Source order records, target year.
## Output : History order record list, target year record list.
####################################################################################################################################################
def filter_analysis_cat(lst_src_order, tar_cat):
    lst_tar = []
    
    print "Start filter the history record set..."
    for rcd in lst_src_order[1:]:
        if (not rcd[IDX_E].strip() and not rcd[IDX_TEL].strip()): continue       ## Skip the empty email and empty telephone record element.

        if (rcd[IDX_ACC] == tar_cat or tar_cat.upper() == ALL_CAT):
            lst_tar.append(rcd)

    ttl_tar_rcd = len(lst_tar)   
    empty_email_rcd = len(lst_src_order) - 1 - (ttl_tar_rcd)
    print "Completed filtering target-category sale order records. Filtered records : %d ..." % (ttl_tar_rcd)
    print "Total empty email + skip records : %d" % empty_email_rcd
    print ""

    return lst_tar


####################################################################################################################################################
## For extracting the day information from order added date time field.
## Input  : order_date from record line.
## Output : order day. 
####################################################################################################################################################
def extract_day_in_order(order_date):
	
	## Checking input date.
	## print order_date
	dt = parser.parse(order_date)
	
	return dt.day


####################################################################################################################################################
## For determining it is company or individual, based on firstname and lastname indicator.
## Input  : Firstname, Lastname
## Output : Company code or Individual code. 
####################################################################################################################################################
def determine_cpny_ind(fname, lname, email_add):

    ## By default, it is infividual case.
    my_code = CODE_IND

    ## If email is not empty
    if( not email_add ):
        if( not ("HOTMAIL" in email_add.upper()) or 
            not ("GMAIL" in email_add.upper()) or
            not ("YAHOO" in email_add.upper()) ):
                my_code = CODE_CPNY

    if ("SDN" in fname.upper() or "SDN" in lname.upper() or
        "BHD" in fname.upper() or "BHD" in lname.upper() ):
        my_code = CODE_CPNY

    return my_code


####################################################################################################################################################
## For processing a record content to register an order and populate the order details to attach with it.
## For each order items, record it in dict_order_items, append it in KEY_ORD_ITEMS in dict_order_detail.
## Input  : Sale record, dict_order
## Output : None. Output via reference by updating dict_order, dict_order_detail in 
####################################################################################################################################################
def process_dict_order(rcd, my_dict_order):
    
    order_id = rcd[ IDX_OID ]

    ## Create the order-item records.
    dict_order_item = {}
    dict_order_item[ KEY_PRD_NAME ] = rcd[ IDX_PRD_NAME ]
    dict_order_item[ KEY_PRD_QTY ] = rcd[ IDX_PRD_QTY ]
    dict_order_item[ KEY_PRD_TTL ] = rcd[ IDX_PRD_TTL ]
    dict_order_item[ KEY_PRD_P ] = rcd[ IDX_PRD_P ]
    dict_order_item[ KEY_PRD_MANU ] = rcd[ IDX_MANU ]
    dict_order_item[ KEY_PRD_SUB_CAT ] = rcd[ IDX_PRD_SUB_CAT  ]
    dict_order_item[ KEY_PRD_MDL ] = rcd[ IDX_PRD_MDL ]
    dict_order_item[ KEY_PRD_ACC ] = rcd[ IDX_ACC ]

    ## If order_id already exist in records, then append the order purchased category
    if(order_id in my_dict_order.keys()):

        ## Append order detail items.
        ## Not to add if Analysis category is empty.
        if(dict_order_item[ KEY_PRD_ACC ].strip()):
            
            ## Not to add if order are not from FULL_CAT.
            if( dict_order_item[ KEY_PRD_ACC ] in FULL_CAT ):
                my_dict_order[order_id][KEY_ORD_ITEMS].append(dict_order_item)

                ## Check if the category has already in list.
                if( not ( rcd[IDX_ACC] in my_dict_order[order_id][KEY_ORD_CAT] )):
                    my_dict_order[order_id][KEY_ORD_CAT].append(rcd[IDX_ACC])
    
    else:
        ## If order_id is new, then initialize dict_order_details.    
        ## Initialize dict_order_detail
        dict_order_detail = {}

        dict_order_detail[ KEY_ORD_TTL ] = rcd[ IDX_TTL ]        
        dict_order_detail[ KEY_ORD_YR ] = rcd[ IDX_YR ]
        dict_order_detail[ KEY_ORD_QT ] = rcd[ IDX_QTR ]
        
        ## Taking care of data. Check if empty month data, extract from ADDDATE.
        if(not rcd[ IDX_MTH ]):
            dict_order_detail[ KEY_ORD_MT ] = extract_month_in_order(rcd[ IDX_ADDDATE ])
        else:
            dict_order_detail[ KEY_ORD_MT ] = rcd[ IDX_MTH ]

        dict_order_detail[ KEY_ORD_DAY ] = extract_day_in_order(rcd[ IDX_ADDDATE ])     ## Extract day
        dict_order_detail[ KEY_ORD_ADDDT ] = parser.parse(rcd[ IDX_ADDDATE ])           ## Convert date string to datetime object.
        dict_order_detail[ KEY_ORD_QTY ] = rcd[ IDX_TTL_QTY ]

        ## Not to add if Analysis category is empty.
        dict_order_detail[ KEY_ORD_CAT ] = []
        if( rcd[IDX_ACC].strip() ):
            if( rcd[IDX_ACC] in FULL_CAT ):
                dict_order_detail[ KEY_ORD_CAT ].append(rcd[IDX_ACC])
        
        ## Record in item details for each product.
        ## dict_order_detail[ KEY_ORD_MANU ] = rcd[ IDX_MANU ]                      ## Obtain manufacturer / brand info.
        
        dict_order_detail[ KEY_ORD_ITEMS ] = []                                     ## Initialize the order items list.
        
        ## Not to add if Analysis category is empty.
        if(dict_order_item[ KEY_PRD_ACC ].strip()):
            ## Not to add if order are not from FULL_CAT.
            if( dict_order_item[ KEY_PRD_ACC ] in FULL_CAT ):
                dict_order_detail[ KEY_ORD_ITEMS ].append(dict_order_item)

        ## Attached in current
        my_dict_order[order_id] = dict_order_detail        

    return


####################################################################################################################################################
## For obtain customer email as key dictionary. Initiate order information dict to be attached.
## For specific customer, obtain all the unique orders in records to be registered under a specific customer key.
## Obtain also information for the unique order to be register under the order-id as key.
## 
## Process Customer Level Dictionary information.
## Attach with Order Level Dictionary information.
## 
## Input : dict_cust - Dictionary
## Output : None. Output via reference by changing information in dictionary input. 
####################################################################################################################################################
def process_dict_cust_level(lst_order, my_dict):
    
    print "Start processing all sale records & registering CUSTOMER-Level info and ORDER-Level info ..."

    ## Initialize process counter.
    proc_ctr = 0

    for rcd in lst_order:
        curr_key = ""
        cust_email = rcd[IDX_E]
        cust_email.replace(" ", "")

        ## Check if empty email case (Lazada record), taking Telephone Number as Cust dict key.
        if(not cust_email):
            curr_key = rcd[IDX_TEL]
        else:
            curr_key = cust_email

        if (curr_key not in my_dict.keys()):
            ## Register new customer details for output lookup purpose.
            ## Initialize other keys for Customer-lelvel dict and Order-level dict.
            ## Initialize dict_cust_data.

            ## Initialize dict_order by processing current order record
            dict_order = {}
            process_dict_order(rcd, dict_order)

            dict_cust_data = {}
            dict_cust_data[ CUST_KEY_INFO ] = [rcd[IDX_FN], rcd[IDX_LN], rcd[IDX_TEL], rcd[IDX_PCODE], determine_cpny_ind(rcd[IDX_FN], rcd[IDX_LN], cust_email)]
            dict_cust_data[ CUST_KEY_ORDER ] = dict_order

            ## Register customer 
            my_dict[curr_key] = dict_cust_data

        else:
            ## If key already exist in customer dictionary, that's mean customer already registered.
            ## Then check if it is same order-id.
            dict_cust_data = my_dict[curr_key]
            process_dict_order(rcd, dict_cust_data[ CUST_KEY_ORDER ])

        
        proc_ctr = proc_ctr + 1
        op_pp = float(proc_ctr*100) / float(len(lst_order))
        print "Processing all sale records & registering CUSTOMER-Level info and ORDER-Level info [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_order), op_pp),

    return


####################################################################################################################################################
##  For calculating Customer Last Order Days (LOD) information. Calculating from the current system date.
##  For every customer email key in dict_cust_lod, attach another level of LOD dict for storing LOD related info.
##
## Input : dict_cust - Dictionary
## Output : None. Output via reference by changing information in input dictionary - dict_cust_lod. 
####################################################################################################################################################
def produce_lod(cust_dict, dict_lod):

    print "Start processing CUSTOMER-Level info and calculating Last Order Days related info ..."

    ## Getting today date.
    today_date = datetime.datetime.now()

    ## Loop through every customer, to access records, ke == customer email address as key.
    for ke in dict_cust.keys():
        dict_order = dict_cust[ke][CUST_KEY_ORDER]
        lst_ord_day = 0

        key_order = dict_order.keys()
        key_order.sort()     
        oid = key_order[len(key_order)-1]
        curr_dt = dict_order[oid][KEY_ORD_ADDDT]

        lst_ord_day = (today_date - curr_dt).days
        ## print "oid=%s, curr_dt=%s, lst_ord_day=%s" % (oid, curr_dt, lst_ord_day)
        
        ## Register info in output dict information.
        dict_cust_lod_info = {}                         ## Initialize 2nd level LOD related info attached to dict_cust_lod.
        dict_cust_lod_info[KEY_LOD] = lst_ord_day
        dict_lod[ke] = dict_cust_lod_info

    return


####################################################################################################################################################
## For generating report list for output purpose.
## Input  : dict_cust, dict_lod - Dictionary
## Output : List contain lists to output to excel or csv including header.
####################################################################################################################################################
def process_dict_lod_output(cust_dict, dict_lod):
    ## Initialize list and assign with header.
    lst_ret = [[
                "Email", "Firtname", "Lastname", "Tel", "PCode", "Cpny/Ind",
                "Last Order Days"
              ]]

    ## Loop through all lod information, retriving keys for customer information and LOD related info.
    for e in dict_lod.keys():
        lst_ret.append([
            e,
            cust_dict[e][CUST_KEY_INFO][0],
            cust_dict[e][CUST_KEY_INFO][1],
            cust_dict[e][CUST_KEY_INFO][2],
            cust_dict[e][CUST_KEY_INFO][3],
            cust_dict[e][CUST_KEY_INFO][4],
            dict_lod[e][KEY_LOD]
        ])

    return lst_ret


####################################################################################################################################################
## For clearing console screen depend on current OS.
## Input  : N/A
## Output : N/A
####################################################################################################################################################
def clear_screen():
    ## Clear console screen for operations
    if( os.name == 'nt'): os.system('cls') 
    else: os.system('clear')


###############################################################################################
## Main program started.
###############################################################################################
## Clear output screen
clear_screen()

if (len(sys.argv) < 2):
    print ">> Usage: cross-sale <sale-data-source_csv> <output_list_csv>"
    print ">> Type 'cross-sale help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> Generate the Last Order Days by analyzing the sale data ..."        
        print ">> Usage: cross-sale <sale-data-source_csv> <output_list_csv>"

    elif (sys.argv[1]=='test'):
        ## Testing area.
        print("Testing area completed!")

    elif (sys.argv[1]=='finfo'):
        ## To display the fields info of the source file.
        ## Read in ... order source records 
        source_order_csv = str(sys.argv[2])

        print "Read in [%s]..." % (source_order_csv)
        with open(source_order_csv, 'r') as f_order:
            reader = csv.reader(f_order)
            lst_order_rcd = list(reader)
        ttl_rcd = len(lst_order_rcd)
        last_idx = ttl_rcd - 1
        print "Successfully read in %s with lines %s" % (source_order_csv, str(ttl_rcd))

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
        print "\n"
        print("File Info display completed!")

    ## Real operation start.
    else:
        ## Getting the parameters ...
        source_order_csv = str(sys.argv[1])
        target_cat = sys.argv[2]
        output_file_csv = str(sys.argv[3])

        ## Defining variables.
        lst_order_rcd = []         ## Original read in order record list.

        ## Start generating the records...
        print "--- Input files validation ---" 
        print "Product Desciption CSV : %s" % (source_order_csv)
        print "Analysis target category : %s" % (target_cat)
        print "Output file : %s" % (output_file_csv)
        print ""

        ## Read in ... order source records
        print "Read in [%s]..." % (source_order_csv)
        with open(source_order_csv, 'r') as f_order:
            reader = csv.reader(f_order)
            lst_order_rcd = list(reader)
        ttl_rcd = len(lst_order_rcd)
        last_idx = ttl_rcd - 1
        print "Successfully read in %s with lines %s" % (source_order_csv, str(ttl_rcd))
        print ""

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
        print "\n"

        ## Start processing algorithm.
        ## Perform filter category.
        lst_opr_rcd = filter_analysis_cat(lst_order_rcd, target_cat)

        ## Declaration of Dictionary variables.
        ## Define dictionary to store dict_cust_data, dict_order information.
        ## Every unique email is key. If email key empty, taking Telephone number as key.
        ## Every unique key attached with 2 dictionary info as defined above.
        dict_cust = {}
        process_dict_cust_level(lst_opr_rcd, dict_cust)
        if(DF): pprint (dict_cust)
        print("Completed putting records in data structure & initialized output data structure ...\n")

        ## Generate output file.
        rpt_fn = output_file_csv
        

        print("\nOperation completed!")



