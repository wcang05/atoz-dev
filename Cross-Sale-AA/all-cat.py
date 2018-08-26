#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 28-May-2017
## Last Modified: 21-Jun-2017
## Version: 2.0
##
## Specifically analyze all categories of products in AtoZ order sale data.
## Extracting email list based on different category.
##
## Command example : 
## python all-cat [cmd] <source> <target folder>
## python all-cat.py -def def-cat.txt 11062017-extract_orders.csv 11062017
## python all-cat.py -def def-cat.txt 12072017-extract_orders.csv 12072017
## [cmd]
## -def     <defination files> <source> <target folder>
##
## Output:
## Folder: 
##      1st Level : Date-of-process
##      2nd Level : Files of each categories
##
## 28-May-2017 Start - Generate categories combination.
## 11-Jun-2017 Make input available into program.
## 16-Jun-2017 Make data source available into program + in correct data structure.
##             Output processed and register list of email and information to folder files.
##             Complete initial version. Test run full record source.
## 18-Jun-2017 Output a process report summary for each category
##             Complete verified algorithm with total unique customer number.
## 21-Jun-2017 Specific output sequence and key pattern - category combination key.
## 15-Jul-2017 Modify processing reports name.
## 
######################################################################################################

## Imports packages
import os
import sys
import csv
from itertools import combinations

###############################################################################################
## Function defination
###############################################################################################

## Compare elements in 2 list, ragardless order.
def compare(s, t):
    return sorted(s) == sorted(t)

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
## Main program started.
###############################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: all-cat.py <sale-data-source_csv> <output-folder>"
    print ">> Type 'all-cat.py help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ All Categories Product Analysis ..."        
        print ">> Usage: all-cat <sale-data-source_csv> "
        print ">> Output: Emails list in each file for all combination of cateogies."
        print ">> Current processed categories: ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']"
        print ">> P-Printer, I-Ink, T-Toner, PA-Paper, TECH-Technology, S-Stationary, OE-Office Equipments, B-Breakroom, C-Cleaning"

    elif (sys.argv[1]=='test'):                
        data = ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']
        list1 = ['P','I','T', 'PA']
        list2 = ['I','T', 'PA', 'P']
        list3 = ['P','I','PA', 'T']
        list4 = ['I']
        list5 = ['p']
        print compare(list1, list2)
        print compare(list2, list3)
        print compare(list3, list4)
        print compare(list4, list5)
        print compare(list1, list3)

    ## Real operation start.
    else:
        ## Debuging flag
        ## df = True
        df = False

        ## process command list case.
        lst_def_out = []
        src_arg_idx = 1
        out_arg_idx = 2
        if (sys.argv[1]=='-def'):
            def_out_fn = sys.argv[2]
            src_arg_idx = 3
            out_arg_idx = 4
            print "Using output defination case... Read in defination file : %s" % def_out_fn
            
            with open(def_out_fn, 'r') as f_def:
                reader = csv.reader(f_def)
                lst_def_out = list(reader)
                def_ttl_rcd = len(lst_def_out)
                last_idx = def_ttl_rcd - 1
            print "Successfully read in %s with lines %s" % (def_out_fn, str(def_ttl_rcd))
            print ">> Validate 1st line : %s" % lst_def_out[0]
            print ">> Validate last line : %s" % lst_def_out[last_idx]
        
        ## Checking source data input, checking target folder output.
        if (len(sys.argv) < src_arg_idx+1):
            print ">> Source data required. Cannot proceed!"
            sys.exit()
        
        if (len(sys.argv) < out_arg_idx+1):
            print ">> Target output directory required. Cannot proceed!"
            sys.exit()

        ## Defining variables.
        lst_order_rcd = []         ## Original read in order record list.        

        ## Getting the parameters ...
        source_order_csv = str(sys.argv[src_arg_idx])
        output_folder = str(sys.argv[out_arg_idx])
        proc_rpt_fn = "[" + output_folder + "]PROC_RPT.CSV"     ## Pre-defined process report output.

        ## Start generating the records...
        print "--- Input files validation ---" 
        print "Product Desciption CSV : %s" % (source_order_csv)
        print "Output folder : %s" % (output_folder)
        print "Access process report : %s\n" % (proc_rpt_fn)

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
        PC = ['P','I','T', 'PA', 'TECH', 'S', 'OE', 'B', 'C']           ## Processing category identified.
        ## PC = ['P','I','T', 'R', 'PA', 'TECH', 'S', 'OE', 'B', 'C']   ## Processing category identified.
        
        dict_allcat_email = {}      ## Initialize all-cat email dictionary.
        dict_cust_buy_cat = {}      ## Register every email and purchased categories dictionary.
        dict_cust_detail = {}       ## Register the customer details.
        lst_proc_rpt = []           ## To keep the statistic process report for all combination of categories.
        
        IDX_E = 9                   ## Define the index of email field.
        IDX_FN = 7                  ## Define the index of first name field.
        IDX_LN = 8                  ## Define the index of last name field.
        IDX_TEL = 10                ## Define the index of telephone field.
        IDX_CITY = 12               ## Define the index of city field.
        IDX_POSC = 13               ## Define the index of postcode field.
        IDX_QTR = 27                ## Define the index of quarter field.
        IDX_MTH = 28                ## Define the index of month field.
        IDX_YR = 29                 ## Define the index of year field.
        IDX_ACC = 49                ## Define the index of analysis_cateogry_code field.

        ## Get all the combination.
        all_cat = sum([map(list, combinations(PC, i)) for i in range(len(PC) + 1)], [])
        all_cat.remove([])
        print "Completed generate all combination of %d categories : %d combination!\n" % (len(PC), len(all_cat))

        ## Go through the source once time, dispatch every record emails and recorded purchased categories.        
        print "Start processing & registering customer purchase categories ..."
        proc_ctr = 1
        for rcd in lst_order_rcd[1:]:       ## Skip the header element.
            cust_email = rcd[IDX_E]
            if not (cust_email in dict_cust_detail.keys()):
                ## Register new customer details.
                dict_cust_detail[ cust_email ] = [rcd[IDX_FN],  rcd[IDX_LN], rcd[IDX_TEL], rcd[IDX_CITY], rcd[IDX_POSC]]
            
                ## Initialize customer buying dictionary.
                dict_cust_buy_cat[ cust_email ] = []

            ## Register customer current buying cateogry.
            ## If category code not exist in current customer purchase list, then add it in.
            if not (rcd[IDX_ACC] in dict_cust_buy_cat[ cust_email ]):
                dict_cust_buy_cat[ cust_email ].append(rcd[IDX_ACC])
            
            proc_ctr = proc_ctr + 1
            op_pp = float(proc_ctr*100) / float(len(lst_order_rcd))
            print "Processing source record [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(lst_order_rcd), op_pp),

        ## Complete processing
        print "Processing source record [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(lst_order_rcd), op_pp)
            
            
        ## Display processed information.
        print "Completed process all source records for registering customer purchased categories..."
        print "Registered %d unique customers." % len(dict_cust_detail.keys())

        ## Main processing to look for all emails that belonged to all categories.
        proc_ctr = 0
        for ac in all_cat:
            ## Initialize all combination of categories to a dictionary.
            key_cat = '-'.join(ac)
            dict_allcat_email[key_cat] = []
            
            ## Loop through the register customer purchase records, put in respective key cat.
            for cust_email in dict_cust_buy_cat.keys():
                ## If purchase categories combination same to the target combination.
                if compare(dict_cust_buy_cat[cust_email], ac):
                    rcd_tuple = [cust_email]                        ## Initialize tuple.
                    for item in dict_cust_detail[cust_email]: 
                        rcd_tuple.append(item)                      ## Add other information of customer to tuple.
                    dict_allcat_email[key_cat].append(rcd_tuple)    ## Add in dictionary.
            
            proc_ctr = proc_ctr + 1
            op_pp = float(proc_ctr*100) / float(len(all_cat))
            print "Processing source record [%s / %s], [%.2f%%] completed... \r" % (proc_ctr, len(all_cat), op_pp),
        
        ## Complete processing
        print "Processing source record [%s / %s], [%.2f%%] completed... \n" % (proc_ctr, len(all_cat), op_pp)

        print ""
        print "Completed process all combination, %d of categories register with respective emails ..." % len(dict_allcat_email)
        print "Checking & validating records ..."       
        print "Total dict_allcat_email.keys()count >>", len(dict_allcat_email)
        print "First all cat dict >> ", dict_allcat_email.keys()[0], dict_allcat_email.values()[0]
        print "Last all cat dict >> ", dict_allcat_email.keys()[len(dict_allcat_email)-1], dict_allcat_email.values()[len(dict_allcat_email)-1]
        

        ## Adding process report header.
        lst_proc_rpt.append(["Category Group", "Num.of.Cust"])

        ## Force report output in defination sequence got the key.
        out_rpt_ctr = 0        
        for rep_seq in lst_def_out:
            lst_target = rep_seq[0].split('-')            
            found_match = False
            for cat_key in dict_allcat_email.keys():
                lst_source = cat_key.split('-')    
                if compare(lst_source, lst_target):
                    found_match = True                    
                    out_rpt_ctr += 1         
                    lst_proc_rpt.append([cat_key, len(dict_allcat_email[cat_key])])
                    op_rpt_pp = float(out_rpt_ctr*100) / float(len(lst_def_out))
                    print "Processing output record [%s / %s], [%.2f%%] completed... \r" % (out_rpt_ctr, len(lst_def_out), op_rpt_pp),

            if not (found_match):
                print "Not Match Case at output report !!! >>", lst_target


        ## Output all files and email records in output folder.
        for cat_key in dict_allcat_email.keys():
            output_csv = output_folder + "\\" + cat_key + ".csv"
            save_list_to_file(dict_allcat_email[cat_key], output_csv)
        print "\nCompleted output all key files of emails."
        
        ## Output process report statistic for all combination of category.
        proc_rpt_csv = output_folder + "\\" + proc_rpt_fn
        save_list_to_file(lst_proc_rpt, proc_rpt_csv)
        print "\nCompleted output process report."
        
        print("\nOperation completed!")