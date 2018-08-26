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

###############################################################################################
## Function defination
###############################################################################################



###############################################################################################
## Main program started.
###############################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: all-cat <sale-data-source_csv> <output_list_csv>"
    print ">> Type 'all-cat help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ All Categories Product Analysis ..."        
        print ">> Usage: all-cat <sale-data-source_csv> "

    elif (sys.argv[1]=='test'):        
        ## Testing area.
        print("Testing area completed!")

    else:
        ## Real operation start.
        

        print("Operation completed!")



