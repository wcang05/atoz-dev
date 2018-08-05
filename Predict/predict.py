#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################################################################################################################################################
## Author SY
## Filename: predict.py
## Start Date: 08-Dec-2017
## Last Modified: 10-Jan-2018
## Version: 2.5
##
## Used to generate & calculate the value for Predict, Forecast and Current sale values for each major category.
## Program will output average total sale history by month from previous years.
## 
## Usage: 
## python predict.py <Predict Type> <Input File> <Output File>
## <Predict Type>
## - Y : Generate next 12 months of monthly data from latest dataset date.
## - T<yyyy> : Target year of 12 months forecast & predict data.
## - H : Generate next 6 months of monthly data from latest dataset.
##
## Example:
## python predict.py [Y | H | T<yyyy>] 31102017-extract_orders.csv 2018-predict.csv
## python predict.py Y 31102017-extract_orders.csv 2018-predict.xls
## python predict.py Y 19122017-extract_orders.csv 2018-predict-19122017-Data.xls
## python predict.py Y predict-dev.csv predict-dev.xls
## python predict.py Y predict-dev2.csv 2018-predict.csv
## python predict.py Y predict-dev-test-I1.csv predict-dev-test-I1.xls
## python predict.py Y predict-dev-test-I2.csv predict-dev-test-I2.xls
## python predict.py Y predict-dev-test-T1.csv predict-dev-test-T1.xls
## python predict.py Y predict-dev-test-IT.csv predict-dev-test-IT.xls
##
## Output:
## Predict, Forecast Sale Values for each category.
## 
## Version History:
## 08-Dec-2017      Start - define usage and command line. Complete module, basic data read in skelaton.
## 11-Dec-2017      Complete module skelaton.
## 13-Dec-2017      Adding processing comments, completed 1st development skelaton.
## 14-Dec-2017      Start implementing output average sale number for each category.
## 15-Dec-2017      Complete implementation of order items in order details.
## 16-Dec-2017      Complete average history sale number generation, all algo, code skelaton.
## 17-Dec-2017      Complete time-gap related analysis implementation.
## 18-Dec-2017      Complete the all implemetation + output modules, testing start. Complete debug and test production data.
## 19-Dec-2017      Testing with latest data. Tweaking Reactivation potential algo. Fixing some bugs.
## 20-Dec-2017      Start dev test data. Constructed dev test data and validated forecast also.
## 10-Jan-2017      Start produce data from 2015-2017, 2016-2017. 3-years and 2-years.
##
############################################################################################################################################################################################################

## Imports packages
import os
import sys
import csv
import copy
import xlwt
import math
import operator
import string
import datetime
import random
from pprint import pprint
from dateutil import parser
from collections import Counter


####################################################################################################################################################
## Program Configuration Parameters
####################################################################################################################################################
## HIS_START_YEAR = 2013
HIS_START_YEAR = 2015
HIS_END_YEAR = 2017

PREDICT_YEAR = 2018
START_PRED_MTH = 1                  ## Start month that all prediction start to generate value into.
END_PRED_MTH = 12                   ## End month that all prediction end to generate value into.

## Configurable prediction simulation parameters.
LOWER_UP_SALE_PV = 0.25             ## Lower scale of potential upsale value scaled at 25% to the average speding amount.
UPPER_UP_SALE_PV = 0.50             ## Upper scale of potential upsale value scaled at 25% to the average speding amount.
CROSS_SALE_PV = 0.35                ## Holding of potential cross-sale rate to the average spending amount.
REACTIVATE_PV = 0.40                ## Holding of potential re-activation rate to the average spending amount.

## Last order day from current day.
LOD_CROSS_SALE = 365                ## Consider only customer has performed order in last 180 days. For Cross-sale case.
LOD_UP_SALE = 365                   ## Consider only customer has performed order in last 180 days. For Up-sale case.
RA_MARK_DAY = 365                   ## Consider customer last order performed 1 year ago.

## Configuration for new customer forecast.
LOWER_NC = 5                        ## Monthly new customer lower number.
UPPER_NC = 10                       ## Monthly new customer upper number.
LOWER_NC_SPT = 200                  ## Lower range of value of new customer spend.
UPPER_NC_SPT = 1500                 ## Upper range of value of new customer spend.

## Category weightage of spending distribution.
DICT_SPT_CAT_WEIGHT = {'P': 0.03, 'I':0.21, 'T':0.18, 'PA':0.14, 'TECH':0.12, 'S':0.10, 'OE':0.09, 'B':0.07, 'C':0.06}

####################################################################################################################################################
## Global Constants
####################################################################################################################################################
## Debuging flag
DF = True
## DF = False
LOG_DF = True

ALL_CAT = "ALL"
SCRIPT_FN = os.path.basename(__file__)
GENERAL_DEBUG_LOG = SCRIPT_FN + "-debug.log"
LST_GENERAL_DEBUG = []
DAY_OF_MONTH = 30                   ## Define the day of a month for gap analysis calculation.

FULL_CAT = ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']

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

## Standard key for holding categories.
KEY_I = "I"
KEY_T = "T"
KEY_P = "P"
KEY_PA = "PA"
KEY_TECH = "TECH"
KEY_S = "S"
KEY_OE = "OE"
KEY_B = "B"
KEY_C = "C"
LST_CAT_KEY = [ KEY_I, KEY_T, KEY_P, KEY_PA, KEY_TECH, KEY_S, KEY_OE, KEY_B, KEY_C ]
DICT_DISP_CAT_KEY = { "INK":KEY_I, "TONER":KEY_T, "PRINTER":KEY_P, 
                      "PAPER":KEY_PA, "STATIONARY":KEY_S, "TECHNOLOGY":KEY_TECH, 
                      "OFFICE EQUIPMENT":KEY_OE, "CLEANING":KEY_C, "BREAKROOM":KEY_B }

## Standard months for holding calculation values.
KEY_JAN = "JAN"
KEY_FEB = "FEB"
KEY_MAR = "MAR"
KEY_APR = "APR"
KEY_MAY = "MAY"
KEY_JUN = "JUN"
KEY_JUL = "JUL"
KEY_AUG = "AUG"
KEY_SEP = "SEP"
KEY_OCT = "OCT"
KEY_NOV = "NOV"
KEY_DEC = "DEC"
LST_MTH_KEY = [ KEY_JAN, KEY_FEB, KEY_MAR, KEY_APR, KEY_MAY, KEY_JUN, KEY_JUL, KEY_AUG, KEY_SEP, KEY_OCT, KEY_NOV, KEY_DEC ]
DICT_MTH_KEY = { 1:KEY_JAN, 2:KEY_FEB, 3:KEY_MAR, 4:KEY_APR, 5:KEY_MAY, 6:KEY_JUN, 7:KEY_JUL, 8:KEY_AUG, 9:KEY_SEP, 10:KEY_OCT, 11:KEY_NOV, 12:KEY_DEC }

## Define 2nd level - month dictionary data holding structure.
KEY_MTH = "MONTH"
KEY_CAT = "CAT"

## Define time-gap analysis dictionary data holding structure.
KEY_TG = "TIME_GAP"                     ## Holding time-gap value for each customer.
AVG_ORD_SPT = "AVG_ORD_SPT"             ## Holding the average order spent for each customer.
LAST_ORD_DAY = "LAST_ORD_DAY"           ## Holding the average of last order day counting from today date.
KEY_BUYCAT = "BUYCAT"                   ## Hold a list of purchased categories in dict_ord_info.
KEY_NOCAT  = "NOCAT"                    ## Hold a list of not purchased categogies in dict_ord_info.


####################################################################################################################################################
## Function defination
####################################################################################################################################################

####################################################################################################################################################
## Function to initialize CATEGORY and MONTHLY data structure for sale number dictionary.
## Input : Sale Number dictionary.
## Output: Intialize 1st and 2nd level of dictionaries for Category and Monthly data structure to attached to input sale number dictionary.
####################################################################################################################################################
def initialize_dict_cat_mth(dict_sn):
    
    ## Initialize Category Keys loop.
    for cat in LST_CAT_KEY:
        dict_sn[ cat ] = {}

        ## Initialize Monthly Keys loop.
        for mth in LST_MTH_KEY:
            dict_sn[ cat ][ mth ] = 0.0

    return


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
## For extracting the month information from order added date time field.
## Input  : order_date from record line.
## Output : order month. 
####################################################################################################################################################
def extract_month_in_order(order_date):
	
	## Checking input date.
	## print order_date
	dt = parser.parse(order_date)
	
	return dt.month


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
        ## dict_order_detail[ KEY_ORD_MANU ] = rcd[ IDX_MANU ]                             ## Obtain manufacturer / brand info.
        
        dict_order_detail[ KEY_ORD_ITEMS ] = []                                         ## Initialize the order items list.
        
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
    
    ## Complete processing
    print "Processing all sale records & registering CUSTOMER-Level info and ORDER-Level info [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(lst_order), op_pp)
    

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
## Calculate month day gap given 2 day, months and years.
## Input  : datetime1, datetime2
## Output : gap in month, decimal point indicate gap in days.
####################################################################################################################################################
def calc_month_day_gap(datetime1, datetime2):

    gap = 0.0    
    delta = datetime2 - datetime1
    gap = delta.days / DAY_OF_MONTH
    
    return gap


####################################################################################################################################################
## Function produce average history sale numbers for each category for customer records.
## Input  : Dictionary holding the cust records.
## Output : Dictionary holding average history output via reference.
####################################################################################################################################################
def produce_ah_sn(dict_cust, dict_ah_sn):
    ## For each customer, check each sale records, for specific category, total up the order

    ttl_his_yr = HIS_END_YEAR - HIS_START_YEAR + 1
    
    ## Loop through the historoical years.
    for y in range(HIS_START_YEAR, HIS_END_YEAR+1):
         ## print(y)
         ## Loop through every customer, to access records, ke == customer email address as key.
        for ke in dict_cust.keys():

            ## Loop through each order. ko == order-id as key.
            for ko in dict_cust[ke][CUST_KEY_ORDER].keys():

                ## If order is belonged to history year, total up sum based on product and category.
                if( int(dict_cust[ke][CUST_KEY_ORDER][ko][KEY_ORD_YR]) == y ):
                    ## print(dict_cust[ke][CUST_KEY_ORDER][ko][KEY_ORD_YR])

                    ## Each item in order, total up product total.
                    for oi in dict_cust[ke][CUST_KEY_ORDER][ko][KEY_ORD_ITEMS]:
                        curr_mth_key = DICT_MTH_KEY[ int(dict_cust[ke][CUST_KEY_ORDER][ko][KEY_ORD_MT]) ]
                        dict_ah_sn[ oi[KEY_PRD_ACC] ][ curr_mth_key ] += float(oi[ KEY_PRD_TTL ])
    

    ## Current dict_ah_sn is having the sum of total product sales number of each category.
    ## Divide the number with history year range for getting average.    
    for cat in LST_CAT_KEY:
        for mth in LST_MTH_KEY:
            dict_ah_sn[ cat ][ mth ] = dict_ah_sn[ cat ][ mth ] / ttl_his_yr

    return


####################################################################################################################################################
## For anlayzed the current order, bought category and non-bought category
## Input  : dict_order dictionary.
## Output : Two of the keys in time-gap dictionary. KEY_BUYCAT and KEY_NOCAT
####################################################################################################################################################
def process_buy_nobuy_cat(dict_order, dict_tg_info):

    for o in sorted(dict_order, key=dict_order.get):
        for c in dict_order[o][KEY_ORD_CAT]:
            if( not (c in dict_tg_info[ KEY_BUYCAT ]) ):
                dict_tg_info[ KEY_BUYCAT ].append(c)
    
    dict_tg_info[KEY_NOCAT] = list(set(FULL_CAT) - set(dict_tg_info[ KEY_BUYCAT ]))

    return


####################################################################################################################################################
## Function to initialize, and produce customer time-gap related parameters analysis.
## Contain analyzed information such as: Time-Gap, Average Order Spend, Last Order Day
## Input  : Dictionary holding the cust records.
## Output : Dictionary holding customer time-gap analysis : dict_cust_tg
####################################################################################################################################################
def produce_cust_tg(dict_cust, dict_cust_tg):
    ## Produce and initialize time gap analysis for each customer.
    
    ## Getting today date.
    today_date = datetime.datetime.now()
    
    ## Loop through every customer, to access records, ke == customer email address as key.
    for ke in dict_cust.keys():
        dict_order = dict_cust[ke][CUST_KEY_ORDER]
        avg_mth_gap = 0.0               
        lst_ord_day = 0
        curr_dt = None

        ## Average = Sum(Total Spending of All Orders) / Number of Orders
        avg_ttl_spt = 0.0

        if( len(dict_order.keys()) < 2 ):
            ## If customer only having 1 or no order record.
            oid = dict_order.keys()[0]
            avg_mth_gap = 12.0
            curr_dt = dict_order[oid][KEY_ORD_ADDDT]
            avg_ttl_spt = float(dict_order[oid][KEY_ORD_TTL])            
    
        else:
            prev_dt = None
            gap = 0.0
            sum_mth_gap = 0.0
            sum_spt_amt = 0.0
            
            ## Loop through all order items.
            for oid in sorted(dict_order, key=dict_order.get):
                if( prev_dt == None):
                    prev_dt = dict_order[oid][KEY_ORD_ADDDT]

                else:
                    curr_dt = dict_order[oid][KEY_ORD_ADDDT]
                    gap = calc_month_day_gap(prev_dt, curr_dt)
                    sum_mth_gap += gap
                    prev_dt = curr_dt                    
                
                ## Accumulate spending amount.
                sum_spt_amt +=  float(dict_order[oid][KEY_ORD_TTL])

            ## Calculate the average of spending gap days.
            avg_mth_gap = sum_mth_gap / (len(dict_order.keys())-1)

            ## Calculate the average of spending amount.
            avg_ttl_spt = sum_spt_amt / len(dict_order.keys())

        ## Last order date to current day
        ## print ke, len(dict_order.keys())
        lst_ord_day = (today_date - curr_dt).days

        ## Register month gap into dictionary.
        dict_tg_info = {}
        dict_tg_info[KEY_TG] = avg_mth_gap
        dict_tg_info[AVG_ORD_SPT] = avg_ttl_spt
        dict_tg_info[LAST_ORD_DAY] = lst_ord_day
        dict_tg_info[KEY_BUYCAT] = []
        dict_tg_info[KEY_NOCAT] = []

        ## Get buy and nobuy cat.
        process_buy_nobuy_cat(dict_order, dict_tg_info)

        dict_cust_tg[ke] = dict_tg_info
        ## End customer loop.

    return


####################################################################################################################################################
## Function to produce forecast sale number for each category, for each customer, for each month.
## Input  : Dictionary holding the cust records.
## Output : Dictionary holding forecast sale number, output via reference.
##          Dictionary holding customer time-gap analysis : dict_cust_tg
####################################################################################################################################################
def produce_fc_sn(dict_cust, dict_cust_tg, dict_fc_sn):
    ## Algorithm Version :
    ## Version 2017 :
    ## For each customer, by analyzing history data, find out the time-gap analysis in performing purchase.
    ## Store the time-gap analysis info in share dictionary, for potential calculation usage.
    
    ## For customer time-gap >12months, NOT CONTRIBUTE value in forecast number.
    ## For customer time-gap >12months, CONSIDERED in RE-ACTIVATE potential number.

    ## For customer time-gap <12months, ceiling down time-gap value + CURR_FC_MTH, to add the value there.
    ## Check the customer purchase history cat, increase forecast value just for purchased gap.

    ## For customer time-gap >= 12, we not taking into consideration for forecast, but consider into potential.
    
    ## Time-gap Forecast Value Calculation:
        ## Forecast Value = Average of RECENT 24 months spending values.
        ## Average = Sum(Total Spending of All Orders) / Number of Orders
    ## ---------------------------------------------------------------------------------------------------------------------------------------------

    ## Loop through every customers, checking te time-gap data.
    for ke in dict_cust.keys():
        tg = int(math.floor(dict_cust_tg[ke][KEY_TG]))
        if ( tg < 12 ):

            ## Control the starting prediction month configured to add-in forecast value.
            ## Else every time-gap amount will add in the starting month.
            if( dict_cust_tg[ke][LAST_ORD_DAY] < DAY_OF_MONTH ):
                start_pred_month = START_PRED_MTH
            else:
                start_pred_month = START_PRED_MTH + tg

            ## Loop through the forecast required months to fill up values.
            if(tg == 0): tg = 1
            for fc_mth in range(start_pred_month, END_PRED_MTH+1, tg):

                ## Get the average forecast sale value.
                fc_sn = dict_cust_tg[ke][AVG_ORD_SPT]
                
                ## Only increase forecast value to customer purchased category.
                ## Only increase for the customer purchased category.
                for cat in dict_cust_tg[ke][KEY_BUYCAT]:
                    try:
                        dict_fc_sn[ cat ][ DICT_MTH_KEY[fc_mth] ] +=  fc_sn
                    except Exception, err:
                        print Exception, err
                        print "cat = %s" % cat
                        print "fc_mth = %s" % fc_mth
                        sys.exit()
                    
    ## End customer loop.

    return


####################################################################################################################################################
## Function to produce UP-SALE potential sale number for each category, for each customer, for each month.
## Input  : Dictionary holding the cust records.
##          Dictionary holding customer time-gap analysis : dict_cust_tg
## Output : Dictionary holding up-sale potential sale number, output via reference.
####################################################################################################################################################
def produce_us_pn(dict_cust, dict_cust_tg, dict_us_pn):
    ## Algorithm Version :
    ## Version 2017 :
    ## For each customer, if time-gap <12 months, for the month term that the customer purchase:
        ## Randomly increase:
            ## Increase number of quantity in an order.
            ## Increase total purchase value in an order by configured %.
            
    ## For customer that time-gap >= 12 months:
        ## Randomly increase update value according to scale, average out 12 months to be added to each month.
    
    ## Up-Sale only happen on customer purchased category.
    ## ---------------------------------------------------------------------------------------------------------------------------------------------

    ## Loop through every customers, checking te time-gap data.
    for ke in dict_cust.keys():
        tg = int(math.floor(dict_cust_tg[ke][KEY_TG]))
        lod = dict_cust_tg[ke][LAST_ORD_DAY]
        
        ## Customer time-gap <12 months and for active customer.
        if ( tg < 12 and lod <= LOD_UP_SALE ):
            ## Control the starting prediction month configured to add-in forecast value.
            ## Else every time-gap amount will add in the starting month.
            if( dict_cust_tg[ke][LAST_ORD_DAY] < DAY_OF_MONTH ):
                start_pred_month = START_PRED_MTH
            else:
                start_pred_month = START_PRED_MTH + tg

            ## Loop through the forecast required months to fill up values.
            if(tg == 0): tg = 1
            for us_mth in range(start_pred_month, END_PRED_MTH+1, tg):

                ## Get the average forecast sale value.
                us_sn = dict_cust_tg[ke][AVG_ORD_SPT] * random.uniform(LOWER_UP_SALE_PV, UPPER_UP_SALE_PV)
                
                ## Only increase upsale value to customer purchased category.
                ## Only increase for the customer purchased category.
                for cat in dict_cust_tg[ke][KEY_BUYCAT]:
                    dict_us_pn[ cat ][ DICT_MTH_KEY[us_mth] ] +=  round(us_sn, 2)
    
    ## End customer loop.

    return


####################################################################################################################################################
## Function to produce CROSS-SALE potential sale number for each category, for each customer, for each month.
## Input  : Dictionary holding the cust records.
##          Dictionary holding customer time-gap analysis : dict_cust_tg
## Output : Dictionary holding cross-sale potential sale number, output via reference.
####################################################################################################################################################
def produce_cs_pn(dict_cust, dict_cust_tg, dict_cs_pn):
    ## Algorithm Version :
    ## Version 2017 :
    ## For customer time-gap <12 months, for the month term that customer purchase:
        ## Check the customer NOT BUY CAT.
        ## Cross-sale value = (CROSS_SALE_PV + NOT_BUY_CAT rate) * average spending value.
    ## ---------------------------------------------------------------------------------------------------------------------------------------------

    ## Loop through every customers, checking te time-gap data.
    for ke in dict_cust.keys():
        tg = int(math.floor(dict_cust_tg[ke][KEY_TG]))
        lod = dict_cust_tg[ke][LAST_ORD_DAY]
        nobuy_rate = len(dict_cust_tg[ke][KEY_NOCAT])/len(FULL_CAT)

        ## Customer time-gap <12 months.
        if ( tg < 12 and lod <= LOD_CROSS_SALE ):
            ## Control the starting prediction month configured to add-in forecast value.
            ## Else every time-gap amount will add in the starting month.
            if( dict_cust_tg[ke][LAST_ORD_DAY] < DAY_OF_MONTH ):
                start_pred_month = START_PRED_MTH
            else:
                start_pred_month = START_PRED_MTH + tg
            
            ## Get the cross-sale value according to calculation.
            cs_sn = dict_cust_tg[ke][AVG_ORD_SPT] * (CROSS_SALE_PV + nobuy_rate)

            ## Loop through the forecast required months to fill up values.
            ## Only increase cross-sale value to customer not purchased category.
            if(tg == 0): tg = 1
            for cs_mth in range(start_pred_month, END_PRED_MTH+1, tg):
                for nocat in dict_cust_tg[ke][KEY_NOCAT]:
                    dict_cs_pn[ nocat ][ DICT_MTH_KEY[cs_mth] ] +=  round(cs_sn, 2)

    return


####################################################################################################################################################
## Function to produce RE-ACTIVATE potential sale number for each category, for each customer, for each month.
## Input  : Dictionary holding the cust records.
##          Dictionary holding customer time-gap analysis : dict_cust_tg
## Output : Dictionary holding re-activate potential sale number, output via reference.
##           
####################################################################################################################################################
def produce_ra_pn(dict_cust, dict_cust_tg, dict_ra_pn):
    ## Algorithm Version :
    ## Version 2017 :
    ## Just check for customer time-gap >= 12months OR customer last order day > RA_MARK_DAY :        
        ## Calculate the ra_value = REACTIVATE_PV * Customer Spending Average
        ## avg_ra_value = Average out 12 months, average out all categories.
        ## Randomize the REACTIVATE_PV for every month.
        ## Scale reactivation value according to category weight.
    ## ---------------------------------------------------------------------------------------------------------------------------------------------
    
    ## Loop through every customers, checking te time-gap data.
    for ke in dict_cust.keys():
        tg = int(math.floor(dict_cust_tg[ke][KEY_TG]))
        lod = dict_cust_tg[ke][LAST_ORD_DAY]

        ## Customer time-gap <12 months.
        if ( tg >= 12 or lod >= RA_MARK_DAY ):
            start_pred_month = START_PRED_MTH            
            
            ## Loop through the forecast required months to fill up values.
            ## Only increase cross-sale value to customer not purchased category.
            if(tg == 0): tg = 1
            for ra_mth in range(start_pred_month, END_PRED_MTH+1, tg):
                ## Get the reactivate sale value according to calculation.
                ## Average out 12 months, average out all categories.
                ra_sn = dict_cust_tg[ke][AVG_ORD_SPT] * random.uniform(0, REACTIVATE_PV) / 12

                for cat in FULL_CAT:
                    ra_cat_spd = float(DICT_SPT_CAT_WEIGHT[cat] * ra_sn)                    
                    dict_ra_pn[ cat ][ DICT_MTH_KEY[ra_mth] ] +=  round(ra_cat_spd, 2)

    return


####################################################################################################################################################
## Function to produce NEW CUSTOMER potential sale number for each category, for each customer, for each month.
## Input  : Dictionary holding the cust records.
## Output : Dictionary holding re-activate potential sale number, output via reference.
##           
####################################################################################################################################################
def produce_nc_pn(dict_cust, dict_nc_pn):
    ## Algorithm Version :
    ## Version 2017 :
    ##
    ##      Forecast monthly new customer. Forecast according to LOWER_NC, UPPER_NC
    ##      Forecast each new customer spending amount. Forecast according to LOWER_NC_SPT, UPPER_NC_SPT
    ##      Distribute spending amount each categories accoring to pre-defined weightage.
    ## 
    ## ---------------------------------------------------------------------------------------------------------------------------------------------

    ## Loop through the forecast required months to fill up values.    
    for nc_mth in range(START_PRED_MTH, END_PRED_MTH+1):
        
        ## Forecast monthly new customer number.
        ttl_nc =  random.randint(LOWER_NC, UPPER_NC)  # Random integer, endpoints included        
        for nc in range(ttl_nc):
            nc_spd = random.randint(LOWER_NC_SPT, UPPER_NC_SPT)

            for cat in FULL_CAT:
                cat_spd = float(DICT_SPT_CAT_WEIGHT[cat] * nc_spd)
                dict_nc_pn[ cat ][ DICT_MTH_KEY[nc_mth] ] += round(cat_spd, 2)

    return


####################################################################################################################################################
## Function to produce TOTAL POTENTIAL sale number for each category, for each customer, for each month.
## Input  : Dictionary holding all the potential sale number.
## Output : Dictionary holding total potential number.
####################################################################################################################################################
def produce_ttl_pn(dict_us_pn, dict_cs_pn, dict_ra_pn, dict_nc_pn, dict_tl_pn):
    ## Total up the sum of potential number and output dictionary.
    
    ## Loop through category keys.
    ## Loop through month keys.
    for cat in LST_CAT_KEY:
        for mth in LST_MTH_KEY:
            dict_tl_pn[ cat ][ mth ] = dict_us_pn[cat][mth] + dict_cs_pn[cat][mth] + dict_ra_pn[cat][mth] + dict_nc_pn[cat][mth]

    return


####################################################################################################################################################
## Function to produce TOTAL FORECAST + POTENTIAL sale number for each category, for each customer, for each month.
## Input  : Dictionary holding forecast and total potential sale number.
## Output : Dictionary holding total forecast + potential number.
####################################################################################################################################################
def product_ttl_sn(dict_fc_sn, dict_tl_pn, dict_fp_sn):
    ## Total up the forecast and potential value.

    ## Loop through category keys.
    ## Loop through month keys.
    for cat in LST_CAT_KEY:        
        for mth in LST_MTH_KEY:
            dict_fp_sn[ cat ][ mth ] = dict_fc_sn[cat][mth] + dict_tl_pn[cat][mth]

    return


####################################################################################################################################################
## Function to write dictionary sale number into a section of excel sheet.
## Input  : Dictionary holding sale number, excel sheet.
## Output : None.
####################################################################################################################################################
def sn_excel_section_output(ir, sec_title, dict_sn, sh):
    
    ## Output category sequence.
    LST_OUT_CAT = ["INK", "TONER", "PRINTER", "PAPER", "STATIONARY", "TECHNOLOGY", "OFFICE EQUIPMENT", "CLEANING", "BREAKROOM"]
    
    r = ir
    sh.write(r, 0, sec_title)
    for mth in range(1, 13):
        sh.write(r+1, mth, DICT_MTH_KEY[mth])
        
    r = r+2;
    for cat in LST_OUT_CAT:
        sh.write(r, 0, cat)
        for mth in range(1, 13):           
            sh.write(r, mth, dict_sn[DICT_DISP_CAT_KEY[cat]][DICT_MTH_KEY[mth]] )
        r += 1

    return

####################################################################################################################################################
## Function to generate every month output value directly into pre-defined Excel format file by taking in sale number dictionary.
## Input  : Dictionary holding sale number, Excel filename.
## Output : Output directly to excel file.
####################################################################################################################################################
def construct_output_sn(dict_ah_sn, dict_fc_sn, dict_us_pn, dict_cs_pn, dict_ra_pn, dict_nc_pn, dict_tl_pn, dict_fp_sn, excel_fn):    

    ## Create excel sheet
    book = xlwt.Workbook()
    sh = book.add_sheet("sheet")
    
    ## Output title - Average History Sales.
    r = 0          
    sn_excel_section_output(r, "Average History Sales", dict_ah_sn, sh)

    ## Output title - Forecast Sales (REMINDER, Time-Gap)
    r += 12
    sn_excel_section_output(r, "Forecast Sales (REMINDER, Time-Gap)", dict_fc_sn, sh)
   
    ## Output title - Potential Sales - From UP-SALE Calculation
    r += 12
    sn_excel_section_output(r, "Potential Sales - From UP-SALE Calculation", dict_us_pn, sh)

    ## Output title - Potential Sales - From CROSS-SALE Calculation
    r += 12
    sn_excel_section_output(r, "Potential Sales - From CROSS-SALE Calculation", dict_cs_pn, sh)

    ## Output title - Potential Sales - From CROSS-SALE Calculation
    r += 12
    sn_excel_section_output(r, "Potential Sales - From RE-ACTIVATION Calculation", dict_ra_pn, sh)

    ## Output title - Potential Sales - From New Customer Calculation
    r += 12
    sn_excel_section_output(r, "Potential Sales - From New Customer Calculation", dict_nc_pn, sh)

    ## Output title - TOTAL Potential Sales
    r += 12
    sn_excel_section_output(r, "TOTAL Potential Sales", dict_tl_pn, sh)

    ## Output title - TOTAL Prediction (Forecast + Potential) Sales
    r += 12
    sn_excel_section_output(r, "TOTAL Prediction (Forecast + Potential) Sales", dict_fp_sn, sh)
    
    ## Save to excel file.
    book.save(excel_fn)

    return


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
        print ">> AtoZ All Categories Forecast & Prediction Analysis ..."        
        print ">> Usage: predict [Y | H | T<yyyy>] <sale-data-source_csv> "


    elif (sys.argv[1]=='test'):
        
        ## dict = {}
        ## dict["KEY1"] = 10
        ## print dict.keys()[0]

        ## today_date = datetime.datetime.now()
        ## target_date = parser.parse("2017-12-16 00:19:11")
        ## days = (today_date - target_date).days
        lst = ['']
        for c in lst:
            print "See what is C = %s" % c

        ## print today_date, target_date, days

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
        output_xls = sys.argv[3]

        ## Defining variables.
        lst_order_rcd = []         ## Original read in order record list.
        
        ## Distionaries holding output data generated from calculation.
        ## Holding prediction output number dictionaries.
        ## 1st level = Category
        ## 2nd level = Monthly
        dict_ah_sn = {}         ## Holding Average History (ah) sale number(sn), for each category, each month
        dict_fc_sn = {}         ## Holding Forecast (fc) sale number, for each category, each month.
        dict_us_pn = {}         ## Holding Up-Sale (us) potential number (pn), for each category, each month.
        dict_cs_pn = {}         ## Holding Cross-Sale (cs) potential number (pn), for each category, each month.
        dict_ra_pn = {}         ## Holding Re-Activate (ra) potential number, for each category, each month.
        dict_nc_pn = {}         ## Holding New Customer (nc) potential number, for each category, each month.
        dict_tl_pn = {}         ## Holding Total (tl) potential number, for each category, each month.
        dict_fp_sn = {}         ## Holding Forecast + Potential (fp) sale number, for each category, each month.
        dict_cust_tg = {}       ## Holding forecast customer time-gap analysis info.

        ## Command inputs validation ...
        print "--- Inputs Command Validation ---" 
        print "Output Type set : %s" % (output_type)
        print "Source file : %s" % (source_order_csv)
        print "Output file : %s" % (output_xls)

        ## Initializing dictionaries data structure.
        initialize_dict_cat_mth( dict_ah_sn )
        initialize_dict_cat_mth( dict_fc_sn )
        initialize_dict_cat_mth( dict_us_pn )
        initialize_dict_cat_mth( dict_cs_pn )
        initialize_dict_cat_mth( dict_ra_pn )
        initialize_dict_cat_mth( dict_nc_pn )
        initialize_dict_cat_mth( dict_tl_pn )
        initialize_dict_cat_mth( dict_fp_sn )
        ## if(DF): pprint (dict_fp_sn); sys.exit();
        ## if(DF): pprint (dict_fc_sn)

        print "\n"
        print "Read in [%s]..." % (source_order_csv)
        with open(source_order_csv, 'r') as f_order:
            reader = csv.reader(f_order)
            lst_order_rcd = list(reader)
            ttl_rcd = len(lst_order_rcd)
        last_idx = ttl_rcd - 1
        print "Successfully read in %s with lines %s\n" % (source_order_csv, str(ttl_rcd))

        ## Perform filter category.
        lst_opr_rcd = filter_analysis_cat(lst_order_rcd, ALL_CAT)

        ## Putting data records into data structure.
        ## Putting sale records into customer dictionary.
        ## Intialize output dictionary for every customer.

        ## Declaration of Dictionary variables.
        ## Define dictionary to store dict_cust_data, dict_order information.
        ## Every unique email is key. If email key empty, taking Telephone number as key.
        ## Every unique key attached with 2 dictionary info as defined above.
        dict_cust = {}
        process_dict_cust_level(lst_opr_rcd, dict_cust)
        if(DF): pprint (dict_cust)
        print("Completed putting records in data structure & initialized output data structure ...\n")

        ## Output time-gap related analysis for each customer.
        produce_cust_tg(dict_cust, dict_cust_tg)
        if(DF): pprint (dict_cust_tg)
        print("Completed Time-Gap related analysis for each customer ...\n")

        ## Output average history sales number for the past 12 months
        produce_ah_sn(dict_cust, dict_ah_sn)
        ## if(DF): pprint (dict_ah_sn)
        print("Complete output Average History sale numbers ...\n")

        ## Output forecast sales number for the next 12 months.        
        produce_fc_sn(dict_cust, dict_cust_tg, dict_fc_sn)
        ## if(DF): pprint (dict_fc_sn)
        print("Complete output Forecast sale numbers ...\n")

        ## Output potential number from UP-SALE calculation.
        produce_us_pn(dict_cust, dict_cust_tg, dict_us_pn)
        ## if(DF): pprint (dict_us_pn)
        print("Complate output Up-Sale potential number ...\n")

        ## Output potential number from CROSS-SALE calculation.
        produce_cs_pn(dict_cust, dict_cust_tg, dict_cs_pn)
        ## if(DF): pprint (dict_cs_pn)
        print("Complete output Cross-Sale potential number for next 12 months ...\n")

        ## Output potential number from RE-ACTIVATE calculation.
        produce_ra_pn(dict_cust, dict_cust_tg, dict_ra_pn)
        ## if(DF): pprint (dict_ra_pn)
        print("Complete output Re-Activate potential number for next 12 months ...\n")

        ## Output potential number from NEW CUSTOMER calculation.
        produce_nc_pn(dict_cust, dict_nc_pn)
        ## if(DF): pprint (dict_nc_pn)
        print("Complete output New Customers potential number for next 12 months ...\n")

        ## Output TOTAL POTENTIAL number for the next 12 months.
        produce_ttl_pn(dict_us_pn, dict_cs_pn, dict_ra_pn, dict_nc_pn, dict_tl_pn)
        ## if(DF): pprint (dict_tl_pn)
        print("Complete output Total Potential number for next 12 months ...\n")

        ## Output total sale number (forecast + potential) for the next 12 months.
        product_ttl_sn(dict_fc_sn, dict_tl_pn, dict_fp_sn)
        ## if(DF): pprint (dict_fp_sn)
        print("Complete output Total Sale number (Forecast + Potential) for the next 12 months ...\n")

        ## Output the list item.        
        construct_output_sn(dict_ah_sn, dict_fc_sn, dict_us_pn, dict_cs_pn, dict_ra_pn, dict_nc_pn, dict_tl_pn, dict_fp_sn, output_xls)
        print("Complete output all sale number to : %s\n" % output_xls)

        print("Operation completed!")