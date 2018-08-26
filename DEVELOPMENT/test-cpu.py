#!/usr/bin/python
# -*- coding: utf-8 -*-

######################################################################################################
## Author SY
## Start Date: 28-May-2017
## Last Modified: 11-Jun-2017
## Version: 1.1
##
## Specifically analyze all categories of products in AtoZ order sale data.
## Extracting email list based on different category.
##
## 28-May-2017 Start - Generate categories combination.
## 11-Jun-2017 Make input available to program.
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

def chk_prime(x):

    isPrime = False

    for i in range(2, x-1):
        if ((x % i) == 0):
            isPrime = True

    if(isPrime == True):
        print "%d is a PRIME number!"% x
    else:
        print "%d is NOT a PRIME number!"% x

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
        target = []
        data = ['P','I','T', 'TECH', 'PA', 'S', 'OE', 'B', 'C']
        combinations(target, data)


    else:
        ## Real operation start.
        chk_prime(20)
        chk_prime(5)
        for n in range(3, 2010301):
            chk_prime(n)

        print("Operation completed!")



