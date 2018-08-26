#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################################################################
## Author SY
## Start Date: 02-Jul-2017
## Last Modified: 02-Jul-2017
## Version: 1.0
##
## Specifically analyze and output the movement of customer between 2 specific combination of categories.
## Output the increment number, decrese number and output the move-in and move-out emails.
##
## Usage: 
## python cat-mv.py <source folder> <target folder> <analysis output folder>
## 
## Example:
## python cat-mv.py 11062017 12072017 mv-out-12072017
## python cat-mv.py 11062017_Sample 11072017_Sample MV-AA-OUPTUT
##
## Input:
## <source folder> - Source folder contain all files of combination of cateogies that contain emails.
## <target folder> - Target folder contain all files of combination of cateogies that contain emails.
## 
## Output:
## <analysis output folder> - Contain the output of the analysis
## analysis-output  - CSV file that hold the analysis content.
##                  - Header: cmb-cat_key, cat_move_in_no, new_no, move_out_no, new_total
## <files>          - mv-cmb-cat-rpt.csv Reporting summary
##                  - Each cmb-cat.csv : Listing all current target folder emails status.
##                  - email, move_from : [New | Old | <cmb-cat>]
## 
##
## Change history:
## 02Jul17     - Initial version.
## 03Jul17     - Checking code implemented.
## 04Jul17     - Middle in implementation.
## 06Jul17     - Complete implementation and testing.
## 08Jul17     - Testing with real data.
## 15Jul17     - Modify output report to prefix with target folder name.
## 
#############################################################################################################################

## Imports packages
import os
import sys
import csv
import copy

## For reporting constant
MOVE_IN_NO  = "move_in_no"
NEW_NO      = "new_no"
MOVE_OUT_NO = "move_out_no"
NEW_TOTAL   = "new_total"
NEW_EMAIL   = "NEW"
OLD_EMAIL   = "OLD"
NONE_CAT    = "null"


######################################################################################################################
## Function defination
######################################################################################################################
## Compare elements in 2 list, ragardless order.
def compare(s, t):
    return sorted(s) == sorted(t)

######################################################################################################################
## Function to return the source category if email is found in it, else return NONE_CAT
## Input : chk_email - Email to check, dict_source - Source category dictionary containing emails.
######################################################################################################################
def email_in_source_cat(chk_email, dict_source):
    ret = NONE_CAT
    for k in dict_source.keys():
        if( chk_email in dict_source[k] ):
            ret = k
            break
    
    ## print "Email : %s in " % chk_email; print dict_source[k];
    ## print "Return = %s" % ret
    return ret

######################################################################################################################
## Function to dump list into CSV file.
## Input : List, CSV file name.
######################################################################################################################
def save_list_to_file(lst_to_save, csv_filename):
    
    with open(csv_filename, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in lst_to_save:
            writer.writerow(val)
    
    output.close()
    
    return

######################################################################################################################
## Main program started.
######################################################################################################################
## Clear console screen for operations
os.system('cls')


if (len(sys.argv) < 2):
    print ">> Usage: cat-mv <source folder> <target folder> <analysis output folder>"
    print ">> Type 'cat-mv help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ All Categories Emails Movement Analysis"        
        print ">> Usage: cat-mv <source folder> <target folder> <analysis output folder>"


    elif (sys.argv[1]=='test'):
        srcdir_fc = len(os.listdir("DEVA"))
        tardir_fc = len(os.listdir("DEVB"))
        print srcdir_fc, tardir_fc 


    ## Real operation start.
    else:
        ## Debuging flag
        ## df = True
        df = False

        ## Reading input parameters
        source_folder = sys.argv[1]         ## Source folder input first in command line input argument.
        target_folder = sys.argv[2]         ## Source folder input later in command line input argument.
        analze_folder = sys.argv[3]         ## Final one is the analysis output folder.

        ## Verifying parameters information.
        print ">> Verifying parameters information."
        print "Source folder : %s" % source_folder
        print "Target folder : %s" % target_folder
        print "Analysis folder : %s" % analze_folder
        print ""
        
        ## Check existance of <source folder>, exit if error.         
        if not os.path.exists(source_folder):
            print "Folder : %s NOT EXIST!! Cannot proceed!" % (source_folder)
            sys.exit()

        ## Check existance of <target folder>, exit if error.
        if not os.path.exists(target_folder):
            print "Folder : %s NOT EXIST!! Cannot proceed!" % (target_folder)
            sys.exit()

        ## Check existance of <analysis output folder>, exit if error.
        if os.path.exists(analze_folder):
            print "Folder : %s EXIST!! Cannot proceed!" % (analze_folder)
            sys.exit()
        
        ## Check number of folders in <source> and <target> folder, exit if not equal.
        lst_src_fn = os.listdir(source_folder)
        lst_tar_fn = os.listdir(target_folder)
        srcdir_fc = len(lst_src_fn)
        tardir_fc = len(lst_tar_fn)
        print "Number of files in %s : %d" % (source_folder, srcdir_fc)
        print "Number of files in %s : %d" % (target_folder, tardir_fc)
        if (srcdir_fc <> tardir_fc):
            print "Total files are NOT THE SAME! Cannot proceed!"
            sys.exit()

        ## Create <analysis output folder>
        print "Creating analysis folder .... %s" % analze_folder
        os.mkdir(analze_folder)
        
        ## Process source folder files.
        ## Read in all folder names as combination category keys.
        ## Intialize source dictionary variables, each key holding a list of emails.
        ## Store the content for emails in dictionary for all catogry keys.
        ## dict_src['cmb-key'] = [Email list]
        dict_src = {}
        for fn in lst_src_fn:
            ## Taking filename only as the key.
            dict_key = fn.split('.')[0]
            dict_src[dict_key] = []

            with open(source_folder + "/" + fn, 'r') as f_email:
                reader = csv.reader(f_email)
                tmp = list(reader)
                for ei in tmp:
                    ## Just get the email element for process.
                    dict_src[dict_key].append(ei[0].strip())    
        
        print "Successfully read in all emails in files in source folder: %s" % (source_folder)
        if df: print "\nSource Dict :"; print dict_src
        

        ## Process target folder files
        ## Read in all folder names as combination category keys.
        ## Store the content of emails in dictionary for all category keys.
        dict_tar = {}
        for fn in lst_tar_fn:
            ## Taking filename only as the key.
            dict_key = fn.split('.')[0]
            dict_tar[dict_key] = []

            with open(target_folder + "\\" + fn, 'r') as f_email:
                reader = csv.reader(f_email)
                tmp = list(reader)
                for ei in tmp:
                    ## Just get the email element for process.
                    dict_tar[dict_key].append(ei[0].strip())

        print "Successfully read in all emails in files in target folder: %s" % (target_folder)
        if df: print "\nTarget Dict :"; print dict_tar
        print ""

        ## Check if all category names key are matched between source and target, not only number.
        ## Exit if not match.        
        if not compare(dict_src.keys(), dict_tar.keys()):
            print "Keys in Source folder DO NOT MATCH with Target folder!!! Cannot proceed!"
            sys.exit()

        ## Start movement analysis processes...
        ## Declare lst_curr_cat_remain - for keeping current cmb-cat remaining emails.
        ## Declare lst_curr_cat_in - for keeping new move in emails.
        ## Declare lst_curr_cat_out - for keeping move out emails.                
        dict_move_in = {}       
        dict_move_out = {}
        dict_remain = {}
        dict_cat_info = {}      ## For storing report information.
        
        ## Loop through all source keys.
        ## Since the SOURCE KEYS == TARGET KEYS, taking the SOURCE KEYS for looping.
        for src_cmb_key in dict_src.keys():
            ## Initialize storage
            dict_move_in[src_cmb_key] = []      ## To store new email that added in specific key.
            dict_move_out[src_cmb_key] = []     ## To store key that no longer exist in target folder for specific key.
            dict_remain[src_cmb_key] = []
            
            ## For every emails, check existance in target similar cmb-cat key dictionary.
            ## For specific cmb-cat key, loop through all the emails in it.
            for src_curr_key_email in dict_src[src_cmb_key]: 
                ## If the source email found in the target storage for specific key.
                if (src_curr_key_email in dict_tar[src_cmb_key]):
                    ## If source email exist, store in remain bin, remove target dict stored emails.
                    dict_remain[src_cmb_key].append(src_curr_key_email)

                    ## Remove the target dictionary emails for specific cmb-key. At last, remaining email is the one newly added one.
                    ## This will be stored as move-in category.
                    dict_tar[src_cmb_key].remove(src_curr_key_email)

                else:
                    ## If source email for specific key does not found in target storage for specific key, that's mean the email as move-out in target.
                    ## If source email not found, store email in move out bin.
                    dict_move_out[src_cmb_key].append(src_curr_key_email)
            
            ## If after looping, specifc cmb-cat key dict content is not empty, all emails in the cat is new move in.
            ## Either is NEW added or MOVE-IN from other category.
            ## Transfer to move-in dictionary.
            dict_move_in[src_cmb_key] = dict_tar[src_cmb_key]

            ## Storing processing information.
            ## Declaring new info tuple
            dict_curr_info_tuple = {}
            dict_curr_info_tuple[ NEW_NO ] = 0  ## Still not sure which email is a new one.
            dict_curr_info_tuple[ MOVE_IN_NO ] = len(dict_move_in[src_cmb_key])
            dict_curr_info_tuple[ MOVE_OUT_NO ] = len(dict_move_out[src_cmb_key])
            dict_curr_info_tuple[ NEW_TOTAL ] = len(dict_remain[src_cmb_key]) + dict_curr_info_tuple[ MOVE_IN_NO ]

            ## Storing info tuple for current cmb-cat.
            dict_cat_info[ src_cmb_key ] = dict_curr_info_tuple
        ## END OF - Loop through all source keys.
        
        ## Loop through all source keys.
        ## Storing tuple defined as (email, move_from : [NEW | OLD | <cmb-cat>])
        dict_catmv_email_output = {}    ## Store the output for every key, all the emails status.
        for src_cmb_key in dict_src.keys():
            ## Initialization
            dict_catmv_email_output[src_cmb_key] = [["Emails", "Status"]]

            ## Add in remaining emails in current cmb-cat first.
            ## Mark it's status as OLD.
            for e in dict_remain[src_cmb_key]:
                dict_catmv_email_output[src_cmb_key].append([e, OLD_EMAIL])

            ## For email marked as move-in, search emails from all source, to capture which category the move out from.
            new_e_ctr = 0
            for se in dict_move_in[src_cmb_key]:
                ## This is to search for specific email captured in move_in, from which category this email from.
                src_cat = email_in_source_cat(se, dict_src)

                if (src_cat == NONE_CAT):
                    dict_catmv_email_output[src_cmb_key].append([se, NEW_EMAIL])
                    new_e_ctr = new_e_ctr + 1
                else:
                    dict_catmv_email_output[src_cmb_key].append([se, src_cat])               
            
            ## Update processing information.
            (dict_cat_info[src_cmb_key])[NEW_NO] = new_e_ctr
            (dict_cat_info[src_cmb_key])[MOVE_IN_NO] = (dict_cat_info[src_cmb_key])[MOVE_IN_NO] - new_e_ctr

        ## END OF - Loop through all source keys.

        ## Data structure for reporting purpose.
        ## Constructing Header: cmb-cat_key, move_in_no, new_no, move_out_no, new_total
        lst_mv_rpt = [["cmb-cat", "cat_move_in_no", "new_no", "move_out_no", "new_total"]]
        for src_cmb_key in dict_src.keys():
            lst_mv_rpt.append([
                src_cmb_key,
                (dict_cat_info[src_cmb_key])[MOVE_IN_NO],
                (dict_cat_info[src_cmb_key])[NEW_NO],
                (dict_cat_info[src_cmb_key])[MOVE_OUT_NO],
                (dict_cat_info[src_cmb_key])[NEW_TOTAL]
            ])
        
        ## Output reporting file to analysis folder.
        save_list_to_file(lst_mv_rpt, analze_folder + "\\[" + target_folder + "]mv-cmb-cat-rpt.csv")
        print "Complete saving email category moment summary report, check total record : %d\n" % (len(lst_mv_rpt)-1)


        ## Output all emails movement status for each combination of category.
        for k in dict_catmv_email_output.keys():
            fpfn = analze_folder + "\\" + k + ".csv"
            save_list_to_file(dict_catmv_email_output[k], fpfn)
        print "Complete saving all %d categories emails with movement status!" % len(dict_catmv_email_output.keys())

        
        print("Operation completed!")



