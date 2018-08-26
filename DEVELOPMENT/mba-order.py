#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 11-Jul-2017
## Last Modified: 11-Jul-2017
## Version: 1.0
##
## Market Basket Analysis - Per Order, No Date Sequence analysis in AtoZ sale records.
##
## Usage: 
## python mba-order <display flag> <category list> <output file>
## <Category list> - ['P','I','T', 'TECH', 'PA', 'S', 'OE', 'B', 'C']
## 
## Example:
## python mba.py 
##
## Input:
## 
## 
## Output:
## 1. Calculate the 
## 
##
## 28-May-2017 Start - Generate categories combination.
## 11-Jun-2017 Make input available into program.
## 
######################################################################################################

## Imports packages
import os
import sys
import csv
import copy

###############################################################################################
## Function defination
###############################################################################################

def combinations(target, data):
    for i in range(len(data)):
        new_target = copy.copy(target)
        new_data = copy.copy(data)
        new_target.append(data[i])
        new_data = data[i+1:]
        print new_target
        combinations(new_target, new_data)



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
        target = []
        data = ['P','I','T', 'TECH', 'PA', 'S', 'OE', 'B', 'C']
        combinations(target, data)

    ## Real operation start.
    else:
        ## Debuging flag
        ## df = True
        df = False
        
        ## Defining variables.
        lst_order_rcd = []         ## Original read in order record list.

        ## Getting the parameters ...
        source_order_csv = str(sys.argv[1])

        ## Start generating the records...
        print "--- Input files validation ---" 
        print "Product Desciption CSV : %s" % (source_order_csv)

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


        print("Operation completed!")



