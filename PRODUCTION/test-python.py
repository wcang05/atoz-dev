#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 28-Feb-2018
## Last Modified: 28-Feb-2018
## Version: 1.0
##
## Command example:
## python test-python.py test1 test2
##
## Program to test Python function that's working fine in server.
## 28-Feb-2018      Basic functions.
##
######################################################################################################

## Imports packages
import os
import sys
import csv
import copy
import platform

###############################################################################################
## Function defination
###############################################################################################



###############################################################################################
## Main program started.
###############################################################################################
if (len(sys.argv) < 2):
    print ">> Default Python Testing Program in Current Running OS."
    print ">> Type 'Python test-python.py test1 test2"

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
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]

        ## Clear console screen for operations
        if( os.name == 'nt'): os.system('cls') 
        else: os.system('clear')

        print "OS Name = %s" % os.name

        print ("Starting the normal operation ...")
        print "Input ARGV1 = %s, ARGV2 = %s" % (argv1, argv2)

        print("Operation completed!\n")
