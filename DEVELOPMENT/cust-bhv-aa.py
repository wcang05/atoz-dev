from __future__ import division
#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################################################################################################
## Author SY
## Start Date: 11-Aug-2017
## Last Modified: 07-Nov-2017
## Version: 2.5
##
## Customer Behavior Advance Analysis.
## 1. Understand customer purchasing behavior and perform several analysis.
## 2. Analysis output for every specific customer:
##    2.1 Average spending power based on historical data.
##    2.2 Average buying product quantity.
##    2.3 Average oder placed by month, quarter, year.
##    2.4 Current, Target and Potential spending power on target year.
##    2.5 Report analysis for overall products categories, and each specific product categories.
##    2.6 Report customer spending power based on 5 categories, Low, Medium, Average, Good, Very High.
## 3. Take email as unique key, if no email, take firstname as unique key.
##    3.1 Take information of First Name, Tel, Postcode as customer information.
##
## Dev:
## python cust-bhv-aa.py cust-bhv-dev2.csv 2017 cust-bhv-aa all
## python cust-bhv-aa.py cust-bhv-dev2.csv 2017 cust-bhv-aa I
##
## Usage :
## python cust-bhv-aa.py <source data> <target-year> <output folder> <filtered-category>
## <output folder>  - cust-bhv-aa.xls 
## 
## Usage Example:
## python cust-bhv-aa.py 05082017-extract_orders.csv 2017 cust-bhv-aa
## python cust-bhv-aa.py cust-bhv-dev2.csv 2017 cust-bhv-aa
## python cust-bhv-aa.py finfo 31102017-extract_orders.csv
##
##
## Version History:
## 11-Aug   Initialize.
## 16-Aug   Completed fundamental data read-in to data ductionaries structure.
## 17-Aug   Completed average, min, max spend gap month bhv info. 
## 22-Aug   Completed average spending info.
## 17-Sep   Implement analysis category filtering mechanism.
## 18-Sep   Start - 2.4 Current, Target and Potential spending power on target year. - On-hold
## 27-Oct   Resolving gap analysis for 0.5 month to 1 year gap months bhv info. -- Enhancement.
## 30-Oct   Complete gap analysis for 0 - 0.25 ==> Less than 1 week, 0.25 - 0.5 ==> Less than 2 weeks, 0.5 - 1.0 ==> Less than 1 month
## 31-Oct   Change gap date calculation method using delta day between 2 dates.
## 06-Nov   Output each customer, purchased product brand / manufacturer.
## 07-Nov   Add an output field for obtain latest purchased manufacturer for order item in output.
##          Add dataset_year field for output.
## 
####################################################################################################################################################

## Imports packages
import os
import sys
import csv
import copy
import xlwt
import math
import operator
import string
from pprint import pprint
from dateutil import parser
from collections import Counter

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

DAY_OF_MONTH = 30                   ## Define the day of a month for gap analysis calculation.

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
IDX_PT = 37                         ## Define the index of product total.
IDX_MANU = 46                       ## Define the index of product manufacturer name field.
IDX_ACC = 49                        ## Define the index of analysis_cateogry_code field.

## Code for data.
CODE_CPNY = "CPNY"                  ## Code to indicate company customer - CPNY
CODE_IND = "IND"                    ## Code to indicate individual customer - IND
CODE_CUST_LVL_LOW = "LOW"           ## Code to indicate customer spending level at LOW.
CODE_CUST_LVL_MED = "MED"           ## Code to indicate customer spending level at MEDIUM.
CODE_CUST_LVL_AVG = "AVG"           ## Code to indicate customer spending level at AVERAGE.
CODE_CUST_LVL_GD = "GD"             ## Code to indicate customer spending level at GOOD.
CODE_CUST_LVL_VH = "VH"             ## Code to indicate customer spending level at VERY HIGH.

## Customer Level Dictionary Keys holding info.
## Dictionary Variable : dict_cust_data
CUST_KEY_INFO = "CUST_INFO"             ## Customer dictionary key for holding customer info. Holding a list.
                                        ## List of items = [Firstname, Lastname, Tel, Postcode, CPNY/IND]
CUST_KEY_ORDER = "CUST_ORD"             ## Customer dictionary key for holding the list of ORDER DICTIONARY.
CUST_KEY_BHV_INFO = "CUST_BHV_INFO"     ## Customer dictionary key for holding Behavior Information dictionary.

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

## Customer Behavior Information Level of holding info.
## Dictionary Variable : dict_cust_bhv
KEY_CUST_LVL = "CUST_LVL"           ## Hold the information of customer level code after calculation.
KEY_BUYCAT = "BUYCAT"               ## Hold a list of purchased categories in dict_ord_info.
KEY_NOCAT  = "NOCAT"                ## Hold a list of not purchased categogies in dict_ord_info.
AVG_SPEND  = "AVGSPT"               ## Hold the average spending amount of the specific customer.
AVG_YR_SPEND = "AVG_YR_SPT"         ## Hold the yearly average spend of the specific customer.
AVG_SPT_GAP = "AVG_SPT_GAP"         ## Hold the number of average gap in month, max 12 months, 12 for only 1 spend.
MAX_SPT_GAP = "MAX_SPT_GAP"         ## Hold the number of maximum gap between order in month. For customer that only have 1 order, max=12 months
MIN_SPT_GAP = "MIN_SPT_GAP"         ## Hold the number of minimum gap between order in month. For customer that only have 1 order, min=12 months
POT_SPEND = "POT_SPT"               ## Hold the potential spending amount for the specific customer.
CURR_SPEND = "CURR_SPT"             ## Hold the current spending amount for the specific customer.
GAP_SPEND = "GAP_SPT"               ## Hold the gap spending amount for the specific customer.
POT_CR_CAT = "POT_CR_CAT"           ## Hold the potential cross-sale categories for the specific customer.
POT_UP_CAT = "POT_UP_CAT"           ## Hold the potential up-sale categories for the specific customer.
TTL_SPEND = "TTL_SPT"               ## Hold the total spend amount in lifetime for customer.
MANUFACTURER = "MANU"               ## Hold a list of counter for each purchased manufacturer.
LAST_MANU = "LAST_MANU"             ## Hold the latest purchased manufacturer.

####################################################################################################################################################
## Function defination
####################################################################################################################################################
def release_list(a):
    del a[:]
    del a
    
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
## Function to dump list into EXCEL file.
## Input : List, EXCEL file name.
####################################################################################################################################################
def save_list_to_excel_file(lst_to_save, excel_filename):
    book = xlwt.Workbook()
    sh = book.add_sheet("cust-bhv-aa")

    r = 0
    c = 0
    for rcd in lst_to_save:
        for e in rcd:
            sh.write(r, c, e)
            c = c + 1
        c = 0
        r = r + 1
    
    book.save(excel_filename)
    
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
    
    return lst_tar


####################################################################################################################################################
## Function to divide the source record list into HISTORY YEARS list and TARGET YEAR list.
## Skip the record only if empty email and empty telephone number.
## Input : source order records, target year.
## Output : history order record list, target year record list
####################################################################################################################################################
def split_his_target(lst_src_order, tar_year):
    lst_his = []
    lst_tar = []

    print "Start dissecting the history - target sale order records ..."    
    for rcd in lst_src_order[1:]:                   ## Skip the header element.
        if (not rcd[IDX_E].strip() and not rcd[IDX_TEL].strip()): continue       ## Skip the empty email and empty telephone element.
        if (rcd[IDX_YR] == tar_year):
            lst_tar.append(rcd)
        else:
            lst_his.append(rcd)

    ttl_tar_rcd = len(lst_tar)
    ttl_hist_rcd = len(lst_his)
    empty_email_rcd = len(lst_src_order) - 1 - (ttl_tar_rcd + ttl_hist_rcd)
    print "Completed dissecting target-history sale order records. Target records : %d, History records : %d" % (ttl_tar_rcd, ttl_hist_rcd)
    print "Total empty email skip record : %d" % empty_email_rcd

    return lst_his, lst_tar

####################################################################################################################################################
## Calculate month day gap given 2 day, months and years.
## ## Input  : day1, month1, year1, day2, month2, year2
## Input  : datetime1, datetime2
## Output : gap in month, decimal point indicate gap in days.
####################################################################################################################################################
## def calc_month_day_gap(day1, month1, year1, day2, month2, year2):
def calc_month_day_gap(datetime1, datetime2):

    gap = 0.0
    ## ttl_month_day = 28
    
    ## If 2 orders happened in same year, then calculate the month different.
    ## if( year1 == year2 ):
        ## Gap = 0 means 2 orders happened in same month. Customer performed 2 orders at the same month.
        ## gap = abs(month1 - month2)
        ## gap_day = abs(day1 - day2) / ttl_month_day

        ## If gap = 0, means different in days.
        ## if( gap == 0.0 ):            
            ## if (gap_day > 1): gap = 1.0 else: gap = gap_day

        ## If gap not equal to 0, meaning different in month.
        ## Calculate also different in day.
        ## else:
            ## gap = gap + gap_day

    ## else:
        ## assigned 12 if more than 1 year.
        ## if ( abs(year1 - year2) > 1 ):
            ## Calculate actual gap of months according to year gap.
            ## gap = 12 * abs(year1 - year2)
        
        ## Only gap 1 year, might be less than 12 month. Check it out.
        ## else:
            ##if( year2 > year1 ):
                ## gap = (12-month1) + month2

            ## else:
                ## gap = (12-month2) + month1

    delta = datetime2 - datetime1
    ## print delta

    gap = delta.days / DAY_OF_MONTH    
    ## print "In calc_month_day_gap : %f" % gap

    return gap


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
## For bought category and non-bought category
## Input  : dict_order dictionary.
## Output : Update data in dict_cust[ CUST_KEY_BHV_INFO ][ KEY_BUYCAT ] and dict_cust[ CUST_KEY_BHV_INFO ][ KEY_NOCAT ]
####################################################################################################################################################
def process_dict_bhv_ord_cat(my_dict_bhv_info, dict_order):

    for o in sorted(dict_order, key=dict_order.get):
        for c in dict_order[o][KEY_ORD_CAT]:
            if( not (c in my_dict_bhv_info[ KEY_BUYCAT ]) ):
                my_dict_bhv_info[ KEY_BUYCAT ].append(c)
    
    my_dict_bhv_info[KEY_NOCAT] = list(set(FULL_CAT) - set(my_dict_bhv_info[ KEY_BUYCAT ]))

    return


####################################################################################################################################################
## For process a list of purchased order manufacturer & obtain the latest purchased manufacturer.
## Input  : dict_order dictionary.
## Output : Update data in dict_cust[ CUST_KEY_BHV_INFO ][ MANUFACTURER ] & dict_cust[ CUST_KEY_BHV_INFO ][ LAST_MANU ]
####################################################################################################################################################
def process_dict_bhv_ord_manu(my_dict_bhv_info, dict_order):

    tmp = []
    for o in sorted(dict_order, key=dict_order.get):
        tmp.append(dict_order[o][KEY_ORD_MANU])

    ## Obtain last purchased manufacturer.
    ## Sorted oder default to ascending, hence latest order-id is the last item to be appended.
    my_dict_bhv_info[ LAST_MANU ] = tmp[-1]

    my_dict_bhv_info[ MANUFACTURER ] = Counter(tmp)
        
    return

####################################################################################################################################################
## For processing to obtain average spent gap in month. Also record the min, max gap in spending in month.
## Input  : dict_order dictionary.
## Output : Update data in dict_cust[ CUST_KEY_BHV_INFO ][ AVG_SPT_GAP ]
####################################################################################################################################################
## def process_dict_cust_bhv_avggap(my_dict_bhv_info, dict_order):
def process_dict_cust_bhv_avggap(e, my_dict_bhv_info, dict_order):

    ## Loop through all the orders to obtain min, max and sum of month gap.
    sum_mth_gap = 0.0
    min_mth_gap = 0.0
    max_mth_gap = 0.0
    avg_mth_gap = 0.0

    if( len(dict_order.keys()) < 2 ):
        ## If customer only having 1 or no order record.
        min_mth_gap = 12.0
        max_mth_gap = 12.0
        avg_mth_gap = 12.0
    
    else:
        ## prev_mth = 0
        ## prev_year = 0
        ## prev_day = 0
        prev_dt = None
        gap = 0.0
        prev_ord_id = None
        curr_ord_id = None

        for o in sorted(dict_order, key=dict_order.get):
            ## First order, register first.
            ## if( prev_day == 0 and prev_mth == 0 and prev_year == 0):
            if( prev_dt == None):
                ## prev_day = int(dict_order[o][KEY_ORD_DAY])
                ## prev_mth = int(dict_order[o][KEY_ORD_MT])
                ## prev_year = int(dict_order[o][KEY_ORD_YR])
                prev_dt = dict_order[o][KEY_ORD_ADDDT]
                prev_ord_id = o
                
            else:
                ## gap = calc_month_day_gap(prev_day, prev_mth, prev_year, 
                ##                         int(dict_order[o][KEY_ORD_DAY]), int(dict_order[o][KEY_ORD_MT]), int(dict_order[o][KEY_ORD_YR]))
                curr_dt = dict_order[o][KEY_ORD_ADDDT]
                curr_ord_id = o
                gap = calc_month_day_gap(prev_dt, curr_dt)
                
                ## Further checking and dump the order if not performing 2 different valid orders at the same day.
                if(LOG_DF):
                    if ( gap == 0 ):
                        ## Only output if 2 orders total amount are same.
                        if( dict_order[prev_ord_id][KEY_ORD_TTL] == dict_order[curr_ord_id][KEY_ORD_TTL] ):                        
                            LST_GENERAL_DEBUG.append( [e, prev_ord_id, curr_ord_id, dict_order[curr_ord_id][KEY_ORD_TTL]] )

                sum_mth_gap += gap

                if( min_mth_gap == max_mth_gap ):
                    min_mth_gap = gap
                    max_mth_gap = gap

                else:
                    if( gap > max_mth_gap): max_mth_gap = gap
                    if( gap < min_mth_gap): min_mth_gap = gap
                    ## print prev_mth, prev_year, gap, avg_mth_gap, max_mth_gap, min_mth_gap
                
                ## prev_mth = int(dict_order[o][KEY_ORD_DAY])
                ## prev_mth = int(dict_order[o][KEY_ORD_MT])
                ## prev_year = int(dict_order[o][KEY_ORD_YR])
                prev_dt = curr_dt
                prev_ord_id = curr_ord_id
            
            ## print prev_mth, prev_year, gap, avg_mth_gap, max_mth_gap, min_mth_gap
        
        avg_mth_gap = sum_mth_gap / (len(dict_order.keys())-1)

        
    ## Registering customer behavior keys.
    ## print avg_mth_gap, max_mth_gap, min_mth_gap

    my_dict_bhv_info[ AVG_SPT_GAP ] = '%.4f' % avg_mth_gap
    my_dict_bhv_info[ MAX_SPT_GAP ] = '%.4f' % max_mth_gap
    my_dict_bhv_info[ MIN_SPT_GAP ] = '%.4f' % min_mth_gap

    return


####################################################################################################################################################
## For generating report list for output purpose.
## Input  : dict_cust - Dictionary
## Output : List contain lists to output to excel or csv including header.
####################################################################################################################################################
def process_dict_cust_output(my_dict, dataset_year):

    ## Initialize list and assign with header.
    lst_ret = [[
                "Email / Cust_ID", "Firtname", "Lastname", "Tel", "PCode", "Cpny/Ind", 
                "Min Spt Gap", "Max Spt Gap", "Avg Spt Gap", "Ttl Spt Amt", "Ave Spt Amt",
                "Buy Cat", "No Buy Cat", "Manufacturer", "Latest Manu", "Dataset Year"
              ]]

    ## Loop through all customers, retriving information.
    for e in my_dict.keys():
        lst_ret.append([
            e,
            my_dict[e][CUST_KEY_INFO][0],
            my_dict[e][CUST_KEY_INFO][1],
            my_dict[e][CUST_KEY_INFO][2],
            my_dict[e][CUST_KEY_INFO][3],
            my_dict[e][CUST_KEY_INFO][4],
            my_dict[e][CUST_KEY_BHV_INFO][MIN_SPT_GAP],
            my_dict[e][CUST_KEY_BHV_INFO][MAX_SPT_GAP],
            my_dict[e][CUST_KEY_BHV_INFO][AVG_SPT_GAP],
            my_dict[e][CUST_KEY_BHV_INFO][TTL_SPEND],
            my_dict[e][CUST_KEY_BHV_INFO][AVG_SPEND],
            my_dict[e][CUST_KEY_BHV_INFO][KEY_BUYCAT],
            my_dict[e][CUST_KEY_BHV_INFO][KEY_NOCAT],
            my_dict[e][CUST_KEY_BHV_INFO][MANUFACTURER],
            my_dict[e][CUST_KEY_BHV_INFO][LAST_MANU],
            dataset_year
        ])
    
    return lst_ret


####################################################################################################################################################
## For processing to obtain average spent.
## Input  : dict_order dictionary.
## Output : Update data in dict_cust[ CUST_KEY_BHV_INFO ][ AVGSPT ]
####################################################################################################################################################
def process_dict_cust_bhv_avgspt(my_dict_bhv_info, dict_order):

    ## Loop through all the orders to obtain the sum of orders.
    sum_ttl_ord = 0.0
    ttl_num_ord = len(dict_order.keys())

    for o in dict_order.keys():
        sum_ttl_ord += float(dict_order[o][KEY_ORD_TTL])
    
    ## Assign average spend and total spend amount info.
    my_dict_bhv_info[ AVG_SPEND ] = format(sum_ttl_ord / ttl_num_ord, '.2f')
    my_dict_bhv_info[ TTL_SPEND ] = format(sum_ttl_ord, '.2f')

    return


####################################################################################################################################################
## For processing dict_cust_bhv content.
## Input  : dict_cust dictionary.
## Output : Update data in dict_cust[ CUST_KEY_BHV_INFO ]
####################################################################################################################################################
def process_dict_cust_bhv(my_dict_cust):
    
    ## Loop through every customer, process relevant customer behavior information.
    for e in my_dict_cust.keys():

        ## Process Average Spending Amount / Per-Order for every customer.        
        process_dict_cust_bhv_avgspt(my_dict_cust[e][CUST_KEY_BHV_INFO], my_dict_cust[e][CUST_KEY_ORDER])
        
        ## Process Average Spending Gap in month or each customer.
        ## process_dict_cust_bhv_avggap(my_dict_cust[e][CUST_KEY_BHV_INFO], my_dict_cust[e][CUST_KEY_ORDER])
        process_dict_cust_bhv_avggap(e, my_dict_cust[e][CUST_KEY_BHV_INFO], my_dict_cust[e][CUST_KEY_ORDER])

        ## Process Buy Cat and No Buy Cat for each customer.
        process_dict_bhv_ord_cat(my_dict_cust[e][CUST_KEY_BHV_INFO], my_dict_cust[e][CUST_KEY_ORDER])

        ## Process manufacturer list for each customer.
        process_dict_bhv_ord_manu(my_dict_cust[e][CUST_KEY_BHV_INFO], my_dict_cust[e][CUST_KEY_ORDER])

    return


####################################################################################################################################################
## For processing a record content to register an order and populate the order details to attach with it.
## Input  : Sale record, dict_order
## Output : None. Output via reference by updating dict_order, dict_order_detail in 
####################################################################################################################################################
def process_dict_order(rcd, my_dict_order):
    
    order_id = rcd[IDX_OID]

    ## If order_id already exist in records, then append the order purchased category
    if(order_id in my_dict_order.keys()):
        ## Check if the category has already in list.
        if( not ( rcd[IDX_ACC] in my_dict_order[order_id][KEY_ORD_CAT] )):
            my_dict_order[order_id][KEY_ORD_CAT].append(rcd[IDX_ACC])
    
    else:
        ## If order_id is new, then initialize dict_order_details.    
        ## Initialize dict_order_detail
        dict_order_detail = {}

        ## dict_order_detail[ KEY_ORD_TTL ] = rcd[ IDX_PT ]
        dict_order_detail[ KEY_ORD_TTL ] = rcd[ IDX_TTL ]        
        dict_order_detail[ KEY_ORD_YR ] = rcd[ IDX_YR ]
        dict_order_detail[ KEY_ORD_QT ] = rcd[ IDX_QTR ]
        dict_order_detail[ KEY_ORD_MT ] = rcd[ IDX_MTH ]
        dict_order_detail[ KEY_ORD_DAY ] = extract_day_in_order(rcd[ IDX_ADDDATE ])     ## Extract day
        dict_order_detail[ KEY_ORD_ADDDT ] = parser.parse(rcd[ IDX_ADDDATE ])           ## Convert date string to datetime object.
        dict_order_detail[ KEY_ORD_QTY ] = rcd[ IDX_TTL_QTY ]
        dict_order_detail[ KEY_ORD_CAT ] = [ rcd[IDX_ACC] ]
        dict_order_detail[ KEY_ORD_MANU ] = rcd[ IDX_MANU ]                             ## Obtain manufacturer / brand info.

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
            ## Where dict_cust_data will contain list of dict_order and dict_cust_bhv
            
            ## Initialize dict_cust_bhv
            dict_cust_bhv = {}
            dict_cust_bhv[ KEY_CUST_LVL ] = ""
            dict_cust_bhv[ KEY_BUYCAT ] = []
            dict_cust_bhv[ KEY_NOCAT ] = []
            dict_cust_bhv[ AVG_SPEND ] = 0.0
            dict_cust_bhv[ AVG_YR_SPEND ] = 0.0
            dict_cust_bhv[ AVG_SPT_GAP ] = 0
            dict_cust_bhv[ MAX_SPT_GAP ] = 0
            dict_cust_bhv[ MIN_SPT_GAP ] = 0
            dict_cust_bhv[ POT_SPEND ] = 0
            dict_cust_bhv[ CURR_SPEND ] = 0
            dict_cust_bhv[ GAP_SPEND ] = 0
            dict_cust_bhv[ POT_CR_CAT ] = []
            dict_cust_bhv[ POT_UP_CAT ] = []
            dict_cust_bhv[ TTL_SPEND ] = 0.0
            dict_cust_bhv[ MANUFACTURER ] = ""
            dict_cust_bhv[ LAST_MANU ] = ""

            ## Initialize dict_order by processing current order record
            dict_order = {}
            process_dict_order(rcd, dict_order)

            dict_cust_data = {}
            dict_cust_data[ CUST_KEY_INFO ] = [rcd[IDX_FN], rcd[IDX_LN], rcd[IDX_TEL], rcd[IDX_PCODE], determine_cpny_ind(rcd[IDX_FN], rcd[IDX_LN], cust_email)]
            dict_cust_data[ CUST_KEY_ORDER ] = dict_order
            dict_cust_data[ CUST_KEY_BHV_INFO ] = dict_cust_bhv

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
## For testing - Function to modify dictionary variable.
## Input : Dictionary
## Output : None. Output via reference by changing information in dictionary input. 
####################################################################################################################################################
def process_dict(my_dict):
    
    if (not my_dict.has_key("TEST1")): 
        print "Not having key: Test 1..Initialize list"
        my_dict["TEST1"] = ["Initiated"]

    if (not my_dict.has_key("TEST2")): 
        print "Not having key: Test 2..Initialize list"
        my_dict["TEST2"] = ["Initiated"]
    
    my_dict["TEST1"].append("Item Test 1")
    my_dict["TEST2"].append("Item Test 2")

    process_dict2(my_dict)

    return

def process_dict2(my_dict):
    if (not my_dict.has_key("LEVEL 2")): my_dict["LEVEL 2"] = ["Initiated"]

    my_dict["LEVEL 2"].append("Level 2 items")

    return

####################################################################################################################################################
## Main program started.
####################################################################################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: cust-bhv-aa <source data> <output folder>"
    print ">> Type 'cust-bhv-aa help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ Customer Term Advance Analysis ..."
        print ">> Usage: cust-bhv-aa <source data> <target-year> <output folder>"

    elif (sys.argv[1]=='test'):
        ## Testing area.
        dict_test = {}
        
        process_dict(dict_test)       
        
        print dict_test
        ## pprint (dict_test)

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
        target_year = sys.argv[2]
        output_folder = str(sys.argv[3])
        filter_cat = str(sys.argv[4])
        dataset_year = str(sys.argv[5])

        ## Start generating the records...
        print "--- Input files validation ---" 
        print "Product Desciption CSV : %s" % (source_order_csv)
        print "Analysis target_year : %s" % (target_year)
        print "Output folder : %s" % (output_folder)
        print "Dataset Year : %s" % (dataset_year)
        
        ## Check if output directory exist, stop processing!
        if os.path.exists(output_folder):
            print "Output folder ALREADY EXIST!! Cannot proceed!"
            sys.exit()

        else:
            os.mkdir(output_folder)
            print "Created output directory : %s ...\n" % output_folder

        ## Read in ... order source records 
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

        ## Perform filter category.
        lst_opr_rcd = filter_analysis_cat(lst_order_rcd, filter_cat)

        ## Declaration of Dictionary variables.
        ## Define dictionary to store dict_cust_data, dict_order, dict_cust_bhv information.
        ## Every unique email is key. If email key empty, taking Telephone number as key.
        ## Every unique key attached with 3 dictionary info as defined above.
        dict_cust = {}

        ## Start customer behavior analysis based on total record set.
        process_dict_cust_level(lst_opr_rcd, dict_cust)

        ## Process to fill up 
        process_dict_cust_bhv(dict_cust)
        if(DF): pprint (dict_cust)

        ## Dump statistic report.        
        rpt_fn = "cust-bhv-aa.csv"
        lst_report = process_dict_cust_output(dict_cust, dataset_year)
        save_list_to_file(lst_report, output_folder + "//" + rpt_fn)

        ## Start processing algorithm.
        ## lst_tar_rcd = []
        ## lst_his_rcd = []
        ## lst_his_rcd, lst_tar_rcd = split_his_target(lst_order_rcd, target_year)
        
        ## END - Process customer purchasing behavior analysis.
        
        if(len(LST_GENERAL_DEBUG) > 0):
            print("Output debug log ...")
            save_list_to_file(LST_GENERAL_DEBUG, output_folder + "//" + GENERAL_DEBUG_LOG)

        print("Operation completed!")



