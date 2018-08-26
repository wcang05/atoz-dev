#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 13-Jul-2017
## Last Modified: 13-Jul-2017
## Version: 1.0
##
## Customer history advance analysis.
## 1. Capture data of customer base and sale orders.
## 2. Analysis yearly customers that made order, total, from 2014 - 2016 - current.
## 3. Find out what is repeat customer, missing customers, potential sale, new customer.
## 4. Able to output the missing and new customer list for target-year.
##
## Usage :
## python cust-his-aa <source data> <target_year,quarter> <output folder>
## <output folder>  - cust-ret-aa-rpt.csv
##                  - [cat][target-year]-missing.csv (listing of email address, cat = ALL + categories)
##                  - [cat][target-year]-new.csv (listing of email address, cat = ALL + categories)
##                  - [cat][target-year]-return.csv (listing of email address, cat = ALL + categories)
##                  - [cat]-all-years-cust-filter.csv (cat = ALL + categories)
##                  - [cat]-all-years-quarter-cust-filter.csv (cat = ALL + categories)
##
## Header : [cat]-all-years-cust-filter.csv
## Email, 2013, 2014, 2015, 2016, 2017
## 
## Header : [cat]-all-years-quarter-cust-filter.csv
## Email, Q1-13, Q2-13, Q3-13, Q4-13, Q1-14, Q2-14, Q3-14, Q4-14, 
## Q1-15, Q2-15, Q3-15, Q4-15, Q1-16, Q2-16, Q3-16, Q4-16, Q1-17, Q2-17, Q3-17
## 
## Usage Example:
## python cust-his-aa.py 16072017-extract_orders.csv 2017 16072017-cust-his-aa-out
## python cust-his-aa.py cust-hist-test.csv 2017 test-cust-his-aa-out
##
## 
## 13-Jul   Initialize.
## 19-Jul   Implementation for [cat][target-year]-missing.csv
##          Implementation for [cat][target-year]-new.csv
##          Implementation for [cat][target-year]-return.csv
## 22-Jul   Skip investigate records that having empty email address.
##          Complete implement all categories new, return and missing customer.
##          Implemention for all category, all years excel filtering data for each specific customer.
## 23-Jul   Implement direct output to excel file.
## 02-Aug   Modify output to only number of order, but not occurrance of order for each product.
## 07-Aug   Continue with unit, dev test.
##  
######################################################################################################

## Imports packages
import os
import sys
import csv
import copy
import xlwt

#####################################################################################################
## Function defination
#####################################################################################################
def release_list(a):
    del a[:]
    del a
    
    return


###############################################################################################
## Function to dump list into CSV file.
## Input : List, CSV file name.
###############################################################################################
def save_list_to_file(lst_to_save, csv_filename):
    
    with open(csv_filename, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in lst_to_save:
            writer.writerow(val)
    
    output.close()
    
    return


###############################################################################################
## Function to dump list into EXCEL file.
## Input : List, EXCEL file name.
###############################################################################################
def save_list_to_excel_file(lst_to_save, excel_filename):
    book = xlwt.Workbook()
    sh = book.add_sheet("sheet")

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


###############################################################################################
## Function to dump customer disctionary into list for CSV file output.
## Input : Customer dictionary, List.
###############################################################################################
def process_cust_output(cust_dist, lst_output):

    for k in cust_dist.keys():
        lst_output.append([
            k, 
            cust_dist[k][0], 
            cust_dist[k][1], 
            cust_dist[k][2], 
            cust_dist[k][3],
            cust_dist[k][4]
        ])

    return


###############################################################################################
## Function to act as core processing for each categories filtering.
## Input : Sale Order Source List, Processing Categories, Target Year, Output_Folder.
###############################################################################################
def main_core_process(lst_src_order, proc_cat, tar_year, output_folder):
    
    IDX_E = 9                   ## Define the index of email field.
    IDX_FN = 7                  ## Define the index of first name field.
    IDX_LN = 8                  ## Define the index of last name field.
    IDX_TEL = 10                ## Define the index of telephone field.
    IDX_CITY = 12               ## Define the index of city field.
    IDX_POSC = 13               ## Define the index of postcode field.
    IDX_QTR = 27                ## Define the index of quarter field.
    IDX_MTH = 28                ## Define the index of month field.
    IDX_YR = 29                 ## Define the index of year field.
    IDX_PT = 37                 ## Define the index of product total.
    IDX_ACC = 49                ## Define the index of analysis_cateogry_code field.

    lst_hist_rcd = []           ## Holding the original sale order history records
    lst_tar_rdc = []            ## Holding the original sale order target records.

    dict_cust_his_detail = {}       ## Register the customer details.
    dict_cust_new_detail = {}       ## Register the new customer details.
    dict_cust_ret_detail = {}       ## Register the return customer details.
    dict_cust_miss_detail = {}      ## Register the missing customer details.

    print "Start dissecting the history - target sale order records, based on Target Category : [%s] ..." % proc_cat
    if(proc_cat == ALL_CAT):
        for rcd in lst_src_order[1:]:                   ## Skip the header element.
            if (not rcd[IDX_E].strip()): continue       ## Skip the empty email element.
            if (rcd[IDX_YR] == tar_year):
                lst_tar_rdc.append(rcd)
            else:
                lst_hist_rcd.append(rcd)

    else:
        for rcd in lst_src_order[1:]:                   ## Skip the header element.
            if (not rcd[IDX_E].strip()): continue       ## Skip the empty email element.
            if (rcd[IDX_ACC] == proc_cat):
                if (rcd[IDX_YR] == tar_year):
                    lst_tar_rdc.append(rcd)
                else:
                    lst_hist_rcd.append(rcd)
    
    ttl_tar_rcd = len(lst_tar_rdc)
    ttl_hist_rcd = len(lst_hist_rcd)
    print "Completed dissecting target-history sale order records. Target records : %d, History records : %d" % (ttl_tar_rcd, ttl_hist_rcd)
    
    
    print "Start processing all historical sale records & registering customer info ..."
    ## Go through the history records, register the customer dictionary data first.
    proc_ctr = 0
    for rcd in lst_hist_rcd:
        cust_email = rcd[IDX_E]
        cust_email.replace(" ", "")
        if (cust_email not in dict_cust_his_detail.keys()):
            ## Register new customer details for output lookup purpose.
            dict_cust_his_detail[ cust_email ] = [rcd[IDX_FN],  rcd[IDX_LN], rcd[IDX_TEL], rcd[IDX_CITY], rcd[IDX_POSC]]
        
        proc_ctr = proc_ctr + 1
        op_pp = float(proc_ctr*100) / float(len(lst_hist_rcd))
        print "Processing historical source record [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_hist_rcd), op_pp),
    
    ## Complete processing
    print "Processing historical sale records [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(lst_hist_rcd), op_pp)
    
    
    ## Analyzing new, returning and missing customers.
    ## Going through target year sale records, detecting OVERALL new and returning customers.        
    print "Start processing target sale records & analyzing NEW and RETURNING ..."
    proc_ctr = 0
    for rcd in lst_tar_rdc:
        cust_email = rcd[IDX_E]
        cust_email.replace(" ", "")
        if (cust_email not in dict_cust_his_detail.keys()):
            ## This is considered new customer.
            if (cust_email not in dict_cust_new_detail.keys()):
                dict_cust_new_detail[ cust_email ] = [rcd[IDX_FN],  rcd[IDX_LN], rcd[IDX_TEL], rcd[IDX_CITY], rcd[IDX_POSC]]

        else:
            ## This is returning customer.
            if (cust_email not in dict_cust_ret_detail.keys()):
                dict_cust_ret_detail[ cust_email ] = [rcd[IDX_FN],  rcd[IDX_LN], rcd[IDX_TEL], rcd[IDX_CITY], rcd[IDX_POSC]]

        proc_ctr = proc_ctr + 1
        op_pp = float(proc_ctr*100) / float(len(lst_tar_rdc))
        print "Processing target sale records  [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_tar_rdc), op_pp),


    ## Complete processing
    print "Processing target sale records [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(lst_tar_rdc), op_pp)
    print "Detected NEW customer for case [%s] : [%d]\n" % (proc_cat, len(dict_cust_new_detail.keys()))
    print "Detected RETURN customer for case [%s] : [%d]\n" % (proc_cat, len(dict_cust_ret_detail.keys()))

    ## Revisiting historical data. If customer not exist in returning customer list, then considered missing customer.
    print "Start re-visiting historical records & analyzing MISSING customers ..."
    proc_ctr = 0
    for e in dict_cust_his_detail.keys():
        ## If email not exist in returning list, then must be missing.
        if (e not in dict_cust_ret_detail.keys()):
            if (e not in dict_cust_miss_detail.keys()):
                dict_cust_miss_detail[e] = dict_cust_his_detail[e]

        proc_ctr = proc_ctr + 1
        op_pp = float(proc_ctr*100) / float(len(dict_cust_his_detail.keys()))
        print "Processing re-visiting historical records  [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(dict_cust_his_detail.keys()), op_pp),

    ## Complete processing
    print "Processing re-visiting historical records [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(dict_cust_his_detail.keys()), op_pp)
    print "Detected MISSING customer for case [%s] : [%d]\n" % (proc_cat, len(dict_cust_miss_detail.keys()))


    ## Process reporting and output list.
    rpt_header = ["email", "firstname", "lastname", "tel", "city", "postcode"]
    lst_new_cust = [rpt_header]       ## Registering new customer for output purpose.
    lst_ret_cust = [rpt_header]       ## Registering returning customer for output purpose.
    lst_miss_cust = [rpt_header]      ## Registering missing customer for output purpose.

    ## Process NEW customer list output.
    new_cust_fn = output_folder + "\\[" + proc_cat + "][" + str(tar_year) + "]-new.csv"
    process_cust_output(dict_cust_new_detail, lst_new_cust)
    save_list_to_file(lst_new_cust, new_cust_fn)

    ## Process RETURN customer list output.
    ret_cust_fn = output_folder + "\\[" + proc_cat + "][" + str(tar_year) + "]-return.csv"
    process_cust_output(dict_cust_ret_detail, lst_ret_cust)
    save_list_to_file(lst_ret_cust, ret_cust_fn)

    ## Process MISSING customer list output.    
    miss_cust_fn = output_folder + "\\[" + proc_cat + "][" + str(tar_year) + "]-missing.csv"
    process_cust_output(dict_cust_miss_detail, lst_miss_cust)
    save_list_to_file(lst_miss_cust, miss_cust_fn)

    ## Construct return statistic
    ## Len of list to minus 1 for remove header record counting.
    lst_stat = [proc_cat, len(lst_new_cust)-1, len(lst_ret_cust)-1, len(lst_miss_cust)-1]

    return lst_stat


###############################################################################################
## Function to produce each quarter, each year of customer existance for excel filtering 
## data purpose.
## Input : Sale Order Source List, Processing Categories, Output_Folder.
###############################################################################################
def cust_excel_filter(lst_src_order, proc_cat, output_folder):

    IDX_OID = 1                 ## Define the index of order-id field.
    IDX_E = 9                   ## Define the index of email field.
    IDX_QTR = 27                ## Define the index of quarter field.
    IDX_MTH = 28                ## Define the index of month field.
    IDX_YR = 29                 ## Define the index of year field.
    IDX_PT = 37                 ## Define the index of product total.
    IDX_ACC = 49                ## Define the index of analysis_cateogry_code field.

    ## Define constant of quarter, year operation constant.
    IDX_QUARTER = [1,2,3,4]
    IDX_YEAR = [2013, 2014, 2015, 2016, 2017]

    lst_ft_src_order = []       ## Holding the filter sale order records according to processing category

    d_cust_yr_ft = {}           ## Store the year unique order-id records.
    d_cust_yr_qr_ft = {}        ## Store the year-quarter unique order-id records.    

    print "Excel filter operation - start filter sale order records, based on Target Category : [%s] ..." % proc_cat
    proc_ctr = 1
    for rcd in lst_src_order[1:]:                   ## Skip the header element.
        ## Skip the empty email element.
        if (not rcd[IDX_E].strip()): 
            proc_ctr = proc_ctr + 1
            continue       

        if (proc_cat == ALL_CAT):
            lst_ft_src_order.append(rcd)
        else:
            if (rcd[IDX_ACC] == proc_cat):
                lst_ft_src_order.append(rcd)
        
        proc_ctr = proc_ctr + 1
        op_pp = float(proc_ctr*100) / float(len(lst_src_order))
        print "Excel filter operation - processing sale records  [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_src_order), op_pp),

    ## Complete processing
    print "Excel filter operation - processing sale records [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(lst_src_order), op_pp)

    print "Excel filter operation - start registering YEAR and QUARTER-YEAR counter ..."
    proc_ctr = 0
    for rcd in lst_ft_src_order:        
        oid = rcd[IDX_OID]
        e = rcd[IDX_E]
        
        ## If it is new users, initiate the storage.
        if( e not in d_cust_yr_ft.keys()):
            ## Initialize 2nd level counter storage.
            d_year_ctr = {}
            d_year_quarter_ctr = {}

            ## User email not yet registered. Initiate the order-id record storage.
            ## for y in IDX_YEAR: d_year_ctr[str(y)] = 0
            for y in IDX_YEAR: d_year_ctr[str(y)] = []

            for y in IDX_YEAR:
                for q in IDX_QUARTER:
                    k = str(q)+str(y)   ## Construct key : quarter + year
                    ## d_year_quarter_ctr[k] = 0
                    d_year_quarter_ctr[k] = []
            
            d_cust_yr_ft[e] = d_year_ctr
            d_cust_yr_qr_ft[e] = d_year_quarter_ctr

        ## If not new users, then check to add coutner accordingly.
        ty = str(rcd[IDX_YR])       ## Current record year obtained.
        tq = str(rcd[IDX_QTR])      ## Current record quarter obtained.
        kk = tq + ty                ## Construct key : quarter + year
        
        ## Register for year filter case.
        ## if( ty not in d_cust_yr_ft[e] ):
        if( ty not in d_cust_yr_ft[e].keys() ):
            LST_GENERAL_DEBUG.append(["In case Cat:[%s], Year key : [%s] not detected in email: [%s]" % (proc_ctr, ty, e)])
        else:
            ## d_cust_yr_ft[e][ty] = d_cust_yr_ft[e][ty] + 1
            ## Registered order id if not found in current year filter list, else skip.
            if( oid not in d_cust_yr_ft[e][ty] ): d_cust_yr_ft[e][ty].append( oid )                

        ## Register for quarter-year filter case.
        ## if( kk not in d_cust_yr_qr_ft[e] ):
        if( kk not in d_cust_yr_qr_ft[e].keys() ):
            LST_GENERAL_DEBUG.append(["In case Cat:[%s], Quarter-Year key : [%s] not detected in email: [%s]" % (proc_ctr, kk, e)])
        else:
            ## d_cust_yr_qr_ft[e][kk] = d_cust_yr_qr_ft[e][kk] + 1
            if( oid not in d_cust_yr_qr_ft[e][kk] ): d_cust_yr_qr_ft[e][kk].append( oid )

        proc_ctr = proc_ctr + 1
        op_pp = float(proc_ctr*100) / float(len(lst_ft_src_order))
        print "Excel filter operation - start registering YEAR and QUARTER-YEAR counter [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_ft_src_order), op_pp),

    
    ## Complete processing
    print "Excel filter operation - start registering YEAR and QUARTER-YEAR counter [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(lst_ft_src_order), op_pp)

    ## Construct output report.
    year_cust_ft_fn = "[" + proc_cat +"]-years-cust-filter.xls" 
    year_quarter_cust_ft_fn = "[" + proc_cat + "]-years-quarter-cust-filter.xls"
    
    lst_yr_cust_ft = [["Email", "2013", "2014", "2015", "2016", "2017"]]
    lst_qr_yr_cust_ft = [[
        "Email", 
        "Q1-13", "Q2-13", "Q3-13", "Q4-13", 
        "Q1-14", "Q2-14", "Q3-14", "Q4-14", 
        "Q1-15", "Q2-15", "Q3-15", "Q4-15", 
        "Q1-16", "Q2-16", "Q3-16", "Q4-16", 
        "Q1-17", "Q2-17", "Q3-17", "Q4-17" ]]    
    
    ## Output Cust YEAR filter.
    for e in d_cust_yr_ft.keys():
        curr_rcd = [e]      ## For holding current constructed record.
        for y in IDX_YEAR: 
            ## curr_rcd.append(d_cust_yr_ft[e][str(y)])
            curr_rcd.append(len(d_cust_yr_ft[e][str(y)]))
        
        lst_yr_cust_ft.append(curr_rcd)
    
    print "Generate Year filter output file for category : [%s] ... %s" % (proc_cat, year_cust_ft_fn)
    save_list_to_excel_file(lst_yr_cust_ft, output_folder + "//" + year_cust_ft_fn)


    ## Output Cust Quarter-Year filter.
    for e in d_cust_yr_qr_ft.keys():
        curr_rcd = [e]      ## For holding current constructed record.
        for y in IDX_YEAR:
            for q in IDX_QUARTER:
                k = str(q)+str(y)
                ## curr_rcd.append(d_cust_yr_qr_ft[e][k])
                curr_rcd.append(len(d_cust_yr_qr_ft[e][k]))
        
        lst_qr_yr_cust_ft.append(curr_rcd)
    
    print "Generate Quarter-Year filter output file for category : [%s] ... %s" % (proc_cat, year_quarter_cust_ft_fn)
    save_list_to_excel_file(lst_qr_yr_cust_ft, output_folder + "//" + year_quarter_cust_ft_fn)

    print ""
    return


#####################################################################################################
## Global constant
#####################################################################################################
ALL_CAT = "all"
SCRIPT_FN = os.path.basename(__file__)
GENERAL_DEBUG_LOG = SCRIPT_FN + "-debug.log"
LST_GENERAL_DEBUG = []

#####################################################################################################
## Main program started.
#####################################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: cust-his-aa <source data> <target_year> <output folder>"
    print ">> Type 'cust-his-aa help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ Customer History Advance Analysis ..."        
        print ">> Usage: cust-his-aa <source data> <target_year> <output folder>"
        print ">> Output: Emails list in each file for all combination of cateogies."
        print ">> Current processed categories: ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']"
        print ">> Current target_year_quarter = 2017,3 (Default)"

    elif (sys.argv[1]=='test'):        
        ## Testing area.
        IDX_QUARTER = [1,2,3,4]
        IDX_YEAR = [2013, 2014, 2015, 2016, 2017]
        d_year_ctr = {}         ## Initiate new year counter.
        d_cust_yr_qr_ft = {}    ## Initiate new quarter-year counter.

        for y in IDX_YEAR: d_year_ctr[str(y)] = 0
        for y in IDX_YEAR:
            for q in IDX_QUARTER:
                k = str(q)+str(y)
                d_cust_yr_qr_ft[k] = 0
        
        for k in d_year_ctr.keys(): print k, d_year_ctr[k]
        for k in d_cust_yr_qr_ft.keys(): print k, d_cust_yr_qr_ft[k]

        save_list_to_excel_file([ ["c1", "c2", "c3"], [1, 2, 3], [11, 22, 33] ], "test.xls")


        print("Testing area completed!")

    ## Real operation start.
    else:        
        ## Debuging flag
        df = True
        ## df = False
            
        ## Getting the parameters ...
        source_order_csv = str(sys.argv[1])
        target_year = sys.argv[2]
        output_folder = str(sys.argv[3])        

        ## Start generating the records...
        print "--- Input files validation ---" 
        print "Product Desciption CSV : %s" % (source_order_csv)
        print "Analysis target_year : %s" % (target_year)
        print "Output folder : %s" % (output_folder)
        
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

        ## Start processing algorithm.
        ## Define the dictionary for all categories combination.
        ## Processing category identified.
        PC = [ALL_CAT, 'P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']
        ## PC = [ALL_CAT]
        
        ## START - Process customer analysis NEW, RET, MISS of ALL categories as overall.
        lst_stat_rpt = [["Category", "New Customer", "Return Customer", "Missing Customer"]]
        for cat in PC:
            ret_stat = main_core_process(lst_order_rcd, cat, target_year, output_folder)            
            lst_stat_rpt.append(ret_stat)
            
            print "Complete process %s New-Return-Missing Customer Analysis..." % cat
            print ret_stat
            print ""
        
        ## Dump statistic report.
        stat_rpt_fn = output_folder + "\\rpt-" + str(target_year) + "-New-Ret-Miss-Cust.csv"
        save_list_to_file(lst_stat_rpt, stat_rpt_fn)
        ## END - Process customer analysis NEW, RET, MISS of ALL categories as overall.

        
        ## START - Process customer analysis Quarter, Year excel filter output.        
        for cat in PC:
            cust_excel_filter(lst_order_rcd, cat, output_folder)
        ## END - Process customer analysis Quarter, Year excel filter output.


        print("Output debug log...")
        save_list_to_file(LST_GENERAL_DEBUG, GENERAL_DEBUG_LOG)

        print("Operation completed!")



