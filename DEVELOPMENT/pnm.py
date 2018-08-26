#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################################### 
## Author SY
## Date: 23-Mar-2017
## Version: 1.0
##
## Specific name matching version for resolving AtoZ product name and id matching.
## Input  :  <product_desc_csv> <order_product_csv>
## Output :  <output_list>
## Header : product_desc_name, order_product_name, order_prod_id, prod_desc_id, matching_rate
##
## Execution Command:
## python pnm.py oc_product_description.csv oc_order_product_5K.csv atoz_cmp_list_5K.csv
## python pnm.py oc_product_description.csv oc_order_product_1500.csv atoz_cmp_list_1500.csv
## python pnm.py oc_product_description_test.csv oc_order_product_test.csv atoz_cmp_list_test.csv
## python pnm.py oc_product_description.csv oc_order_product_test.csv atoz_cmp_list_test.csv
## python pnm.py oc_product_description.csv oc_order_product_20K-1stBatch.csv atoz_cmp_list_20K-1stBatch.csv
## python pnm.py oc_product_description.csv oc_order_product_FULL.csv atoz_cmp_list_FULL.csv
##
## 23-Mar	Initialize version - Completed read in product_desc and order_product file list.
## 24-Mar   Completed sketch algorithms for overall matching program.
## 25-Mar   Completed sketch token matching algorithm.
##          Actual implementation started.
## 26-Mar   Completed implementation.
## 28-Mar   Completed tweaking and checking algorithm implementation details.
## 30-Mar   Completed first extention of algorithm. Result quite promissing.
## 31-Mar   Increasing minor and testing algorithms to increase accuracy.
##          Increasing category word list in weight scoring.
##          Fixing different between main algo vs test algo, in sync.
## 01-Apr   Complete adding in all keywords and fixing.
##          Continue 1st full run of all order-prod records - 20K records - 1st batch.
##          Discovered that 1 order-product-name comparison required ~3 sec. ==> 1 hour able to 
##              compare 1200 order-prod-name. 20K required ~20hours. 233K requried roughly 9 days.
##              Hence, distributed the total 233K order-product-records into 11batches, each batch
##              contain 20K records.
##          Distribute to 11 computers, 1 days (~20hours) to complete all batches.
## 03-Apr   Finalizing algorithm after reviewing 20K run.
##          Testing with 5K order-prod records overnight and prepare to execute to all batches.
## 13-Apr   Algorithm checking and enhance after 1st production run, remain yellow-records rework.
######################################################################################################

## Imports packages
import sys
import csv
import os
import re
from difflib import SequenceMatcher

## Program constant configuration
MODEL_FULL_MATCH_WEIGHT = 20    ## Model word weight setting.
MODEL_IN_MATCH_WEIGHT = 15      ## Model word weight setting.
CAT_MATCH_WEIGHT = 8            ## Category word weight setting.
BRAND_MATCH_WEIGHT = 10         ## Brand word weight setting.
COLOR_MATCH_WEIGHT = 12         ## Color word weight setting.
NUMBER_MATCH_WEGHT = 20         ## Number word weight setting.
SIZE_MATCH_WEIGHT = 5           ## Size word weight setting.


OUTPUT_THRESHOLD_RATING = 0     ## Initially set all result to be output.

LST_CAT_WORD = ["ink", "printer", "toner", "stamp", "marker", "clips", "files", "ribbon", "sheets", "glue",
                "magictape", "notebook", "aroma", "treasury", "binding", "biodegradable", "can", "paper",
                "scanner", "pen", "gel", "book", "calculator", "document", "holder", "bag", "pvc", "card", "board",
                "wire", "leather", "magnet", "desktop", "projector", "tape", "newspaper", "drum", "usb", "flim",
                "pencil", "headphone", "sharpening", "binder", "officejet", "pro", "inkjet", "eprinter", "omen",
                "laptop", "pagewide", "multifunction", "backlit", "probook", "procurve", "prodesk", "microtower",
                "prodisplay", "proone", "scanjet", "slimline", "spectre", "securio", "guillotines"]

LST_BRAND_NAME = ["epson", "hp", "oki", "brother", "samsung", "canon", "faber", "castell", "fuji", "xerox",
                  "papermate", "pentel", "philips", "pilot", "quaker", "printronix", "pny", "artline", "asus", 
                  "benq", "buffalo", "buncho", "campap", "cbe", "dell", "dettol", "double", "durex", "microfiber"
                  "duro", "faber", "castell", "garmin", "gaviscon", "gbc", "hsm", "huawei", "jabra", "mamee",
                  "kokuyo", "lenovo", "lex", "lexmark", "lg", "lion", "logitech", "magic", "max", "maggi"
                  "microsoft", "nec", "orico", "panasonic", "ricoh", "sampro", "sandisk", "scholl", "loytape",
                  "scotch", "sennheiser", "sharpie", "signzone", "sony", "stabilo", "stainless", "targus", "wd",
                  "yoobao", "uhu", "tgs", "abba", "acer", "acrylic", "ae", "huat", "cheong", "wick", "fabuloso",
                  "akasa", "ambi", "pur", "apacer", "apollo", "astar", "avast", "axion", "bobino", "boh", "glo",
                  "campap", "dettol", "east", "energizer", "everyday", "geha", "glade", "gear", "harpic", "iring",
                  "janitor", "jolly", "julie", "muscle", "munchy", "naga", "nakajima", "nescafe", "nokia", "olympic",
                  "olivetti", "panadol", "pernuma", "plus", "root", "premier", "quaker", "quart", "quartet", "rejoice",
                  "rex", "rexel", "ridsect", "ryval", "steel", "sdi", "sdisk", "senghin", "sharp", "shieldtox", 
                  "strepsils", "sunny", "syamal", "tally", "tempera", "link", "twisties", "umei", "vanish", "veet",
                  "velvet", "western", "wp", "yala", "zara", "pavilion", "balliner", "treasury", "frixion", "kristall"]

LST_SPECIAL_WORD = ["set", "combo", "free", "buy", "cube", "eol", "twin", "warranty", "reusable", "bottle"
                    "smiley", "keychain", "lunch", "container", "jacket", "towel", "fan"]

LST_COLOR_WORD = ["black", "cyan", "yellow", "magenta", "grey", "red", "blue", "dark", "light",
                  "orange", "green", "gold", "lemon", "silver", "white", "brown", "mono",
                  "metallic", "fluorescent", "clear", "pink", "chroma", "turqu", "purple", "violet", "maroon",
                  "beige", "brilliant", "ocean", "navy", "teal", "Limelight", "frost", "grape", "bronze"]

LST_SIZE_WORD = ["extra", "large", "small", "medium", "high", "duplex", "cool", "fresh", "original", "vivid",
                 "matte", "thick",  "hard", "new", "natural", "micro", "multifunctional"]

EXT_TOKEN_DICT = { "blk":["black"] , "bk":["black"], "sht":["sheet", "sheets"], "shts":["sheet", "sheets"],
                   "gry":["grey"], "bl": ["blue"], "gr":["green"],  "pr":["pro"], "tplink":["tp", "link"],
                   "detol":["dettol"], "l.":["light"], "philip":["philips"], "sam":["sampro"], "org":["orange"],
                   "wd": ["western", "digital"], "wdigital": ["western", "digital"], "wht":["white"],
                   "prof":["professional"], "profl":["professional"], "oj":["officejet"], "cartr":["cartridge"]}

###############################################################################################
## Function to check if it is MODEL words. Return 1 if YES, 0 if no.
## MODEL words contain Alpha-Numeric, not contain special wordings, no dot in between.
## Word is inside a ().
###############################################################################################
def has_number( inputString ):
    return any(char.isdigit() for char in inputString)

def has_char( inputString ):
    return any(char.isalpha() for char in inputString)

def is_model_word(token_word):

    is_model = False    ## Initialize it is not a model words.
    ## print "In is_model_word: %s" % token_word
    
    ## Check if word is inside a ()
    if ( token_word.startswith("(") and token_word.endswith(")") ):
        ## print "In ()"
        if (has_char(token_word) and has_number( token_word )): 
            is_model = True
        else:
            is_model = False

    else:
        ## Turn it into 1 when discovered it is model word, else remain.
        if (has_char(token_word) and has_number( token_word )): 
            is_model = True
        else:
            is_model = False
    
    ## print is_model    
    return is_model


###############################################################################################
## Function to clean every token.
###############################################################################################
def clean_token_list( lst_token ):
    
    new_lst = []
    
    for e in lst_token:
        ee = e.lstrip().rstrip()
        ee = ee.replace('(', '')
        ee = ee.replace(')','')
        ee = ee.replace("item", '')        
        if (ee == "no"): ee = ''
        if( len(ee) > 1 ):            
            if( '-' in ee ):                
                tmp = ee.replace('-', '')
                ## print "Debug: In clean_token_list: ee=%s, tmp=%s" % (ee, tmp)
                if( tmp.isdigit() == False ): 
                    ## After replace, it is not digit case.
                    ## Check if it is alpha only case.
                    if (tmp.isalpha() ): 
                        ## Replace with space if both side contain only characters.
                        ee = ee.replace('-', ' ')
                        
                        ## Split them and append to list.
                        for i in ee.split(): new_lst.append(i)
                        continue

                    else:
                        ## If it is alphanumeric case.
                        ee = tmp
                
            new_lst.append(ee)

    return new_lst

###############################################################################################
## Function to extend token words for product desc list.
###############################################################################################
def get_digit_part( words ):
    return ''.join(i for i in words if i.isdigit())

def get_char_part( words ):
    return ''.join(i for i in words if i.isalpha())

def extend_desc_token_list( lst_prod_desc ):
    
    lst_extend = list(lst_prod_desc)

    ## Check if token contain color word, break it.
    for e in lst_prod_desc:        
        for c in LST_COLOR_WORD:
            if ( (c != e) and (c in e) ):
                ## print "Debug: e=%s, c=%s" % (e, c)
                ee = e.replace(c, '')
                lst_extend.append(ee)
                lst_extend.append(c)
                lst_extend.remove(e)
                break
        ## End color word content checking.

    ## Extend model case in desc token list by removing special characters.
    for e in lst_prod_desc:
        if( is_model_word(e) ):
            s = special_trim(e)
            if( e!=s ): lst_extend.append(s)

    ## Extend model case by split number and characters as token words.
    for e in lst_prod_desc:
        if( is_model_word(e) ):
            dd = get_digit_part(e)
            cc = get_char_part(e)
            if (dd in e) : lst_extend.append(dd)
            if (cc in e) : lst_extend.append(cc)

    ## Extend token based on EXT_TOKEN_DICT
    for e in lst_prod_desc:
        for k, v in EXT_TOKEN_DICT.items():
            if( e==k ): 
                for i in v:
                    lst_extend.append(i)

    return lst_extend

###############################################################################################
## Function to break order-product name token if contain important words.
###############################################################################################
def extend_op_token_list(list_op_token):
    
    lst_extend = list(list_op_token)

    ## Check if token contain color word, break it.
    for e in list_op_token:        
        for c in LST_COLOR_WORD:
            if ( (c != e) and (c in e) ):
                ## print "Debug: e=%s, c=%s" % (e, c)
                ee = e.replace(c, '')
                lst_extend.append(ee)
                lst_extend.append(c)
                lst_extend.remove(e)
                break
        ## End color word content checking.

    return lst_extend

###############################################################################################
## Function to check if token is brand / color / cat name or not.
## Return True if it is a brand name, False otherwise.
###############################################################################################
def is_brand_word(token_word):
    return any(token_word in s for s in LST_BRAND_NAME)

def is_color_word(token_word):
    return any(token_word in s for s in LST_COLOR_WORD)

def is_cat_word(token_word):
    return any(token_word in s for s in LST_CAT_WORD)

def is_size_word(token_word):
    return any(token_word in s for s in LST_SIZE_WORD)

###############################################################################################
## Function to perform all kind of special trim before tokenized.
## 1. Remove space between '-'
## 2. Remove space after '(' and before ')'
## 3. Remove head, tail spaces.
## 4. Remove space between 'x'
## 5. Remove space between '/'
###############################################################################################
def special_trim( str_content ):
    
    instr = str_content.lstrip().rstrip()
    instr = instr.replace(" -", "-")    
    instr = instr.replace("- ", "-")
    instr = instr.replace(" - ", "-")   
    
    instr = instr.replace(" x", "x")
    instr = instr.replace(" x ", "x")
    
    instr = instr.replace(" / ", "/")
    instr = instr.replace(" /", "/")
    instr = instr.replace("/ ", "/")

    instr = re.sub("\(\s+", "(", instr)
    instr = re.sub("\s+\)", ")", instr)

    return  instr

###############################################################################################
## Function to remove all kind of special characters in product name before tokenized.
## 1. Remove all '*'
## 2. Remove all cases of 'Item No'
## 3. Remove all ':'
## 4. Remove all '#'
## 5. Remove all '"'
## 6. Remove 1 character word. -- Consider no use in information scoring.
###############################################################################################
def special_remove( str_content ):

    ## Remove special unicode characters.
    instr = re.sub(r'[^\x00-\x7f]', r'', str_content)

    instr = instr.replace("&quot;", '')
    instr = instr.replace("&amp;", '')    
    
    instr = instr.replace("*", '')
    instr = instr.replace("* ", '')
    instr = instr.replace(" *", '')

    instr = instr.replace('item no', '')
    instr = instr.replace('"', '')

    instr = instr.replace(":", '')
    instr = instr.replace(" : ", '')
    instr = instr.replace(": ", '')
    instr = instr.replace(" :", '')

    instr = instr.replace("#", '')
    instr = instr.replace(" # ", '')
    instr = instr.replace("# ", '')    
    instr = instr.replace(" #", '')    
    
    instr = instr.replace("+", '') 
    instr = instr.replace(" + ", '') 
    instr = instr.replace("+ ", '')
    instr = instr.replace(" +", '')

    ## Remove 1 character word besides is digit.
    instr = ' '.join(word for word in instr.split() if (len(word)>1 or (word.isdigit())))
    
    return instr

###############################################################################################
## Function to replace special characters to space or other characters to ease processing.
## 1. Replace '/' into space.
###############################################################################################
def special_replace( str_content ):

    instr = str_content.replace("/", " ")
    instr = instr.replace("'", ' ')
    instr = instr.replace(".", ' ')
    instr = instr.replace(",", ' ')     

    return instr

###############################################################################################
## Function to remove all kind of special words in pre-defined list.
###############################################################################################
def special_word_remove( str_content ):
    
    instr = str_content
    for w in LST_SPECIAL_WORD:
        instr = instr.replace(w, "")

    return instr

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
## Function : Scoring token weight mechanism.
## Input : Token word.
## Output : (int) Weight
###############################################################################################
def scoring_token(token_word, debug_flag):
    token_weight = 0

    ## If it is model number, token_weight = token_weight + MODEL_MATCH_WEIGHT
    if( is_model_word(token_word) == True ):        
        token_weight = token_weight + MODEL_FULL_MATCH_WEIGHT
        if(debug_flag): print "DEBUG: %s scoring IS_MODEL = %d" % (token_word, token_weight)

    elif( is_cat_word(token_word) == True ):
        token_weight = token_weight + CAT_MATCH_WEIGHT
        if(debug_flag): print "DEBUG: %s scoring IS_CAT = %d" % (token_word, token_weight)

    elif ( is_brand_word(token_word) == True ):
        token_weight = token_weight + BRAND_MATCH_WEIGHT
        if(debug_flag): print "DEBUG: %s scoring IS_BRAND = %d" % (token_word, token_weight)

    elif ( is_color_word(token_word) == True ):
        token_weight = token_weight + COLOR_MATCH_WEIGHT
        if(debug_flag): print "DEBUG: %s scoring IS_COLOR = %d" % (token_word, token_weight)

    elif( token_word.isdigit() ):
        token_weight = token_weight + NUMBER_MATCH_WEGHT
        if(debug_flag): print "DEBUG: %s scoring IS_NUMBER = %d" % (token_word, token_weight)
    
    elif( is_size_word(token_word) ):
        token_weight = token_weight + SIZE_MATCH_WEIGHT
        if(debug_flag): print "DEBUG: %s scoring IS_SIZE = %d" % (token_word, token_weight)    

    ## Else, token_weight = token_weight + 1
    else:
        token_weight = token_weight + 1
        if(debug_flag): print "DEBUG: %s scoring normal = %d" % (token_word, token_weight)
    
    return token_weight


###############################################################################################
## Function : Calculate total weight in a token list.
## Input : Token list.
## Output : (int) Weight
###############################################################################################
def calc_ttl_token_weight(token_list, debug_flag):
    ## Initiate total weight.
    ttl_weight = 0
    
    ## For every item in token list.
    for e in token_list:
        ttl_weight = ttl_weight + scoring_token(e, debug_flag)
        if(debug_flag): print "DEBUG: %s scoring normal = %d" % (e, ttl_weight)

    return ttl_weight


###############################################################################################
## Function : Calculation token rating.
## Input: prod-desc-token, order-product-token
## Output: Rating normalized to 0 - 1 range.
###############################################################################################
def match_rate(desc_token_list, prod_token_list, total_weight, debug_flag):
    ## Initiate rate = 0
    rate = 0.0

    ## Initiate score_rate
    scoring = 0
    desc_tmp_lst = desc_token_list[:]

    ## For every item token in prod_token_list
    for e in prod_token_list:
        ## For every item token in desc_token_list
        for d in desc_tmp_lst:
            ## If item matched tmp_curr_lst
            if( d == e ):
                ## Remove matched item.
                desc_tmp_lst[:] = (v for v in desc_tmp_lst if v != e)

                if(debug_flag): print "Debug: Found in desc list : %s" % e                
                scoring = scoring + scoring_token(e, debug_flag)

                break
            else:
                if( (is_model_word(e) and is_model_word(d)) ):
                    if( (e in d) or (d in e) ):
                        if(debug_flag): print "Debug: Found in D:%s and E:%s IS_MODEL and CONTAIN case." % (d, e)
                        scoring = scoring + MODEL_IN_MATCH_WEIGHT
                        if(debug_flag): print "DEBUG: %s scoring IN_MODEL = %d" % (e, MODEL_IN_MATCH_WEIGHT)

                        ## Remove matched item.
                        desc_tmp_lst[:] = (v for v in desc_tmp_lst if v != e)

                        break
                    
    if(debug_flag): print "DEBUG: Total scoring = %d" % scoring
    rate = float(scoring) / total_weight
    
    return rate


###############################################################################################
## Similarity in string.
###############################################################################################
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

###############################################################################################
## Main program started.
###############################################################################################
## Clear console screen for operations
os.system('cls')

if (len(sys.argv) < 2):
    print ">> Usage: pnm <product_desc_csv> <order_product_csv> <output_list_csv>"
    print ">> Type 'pnm help' to understand the program usage."

else:
    if (sys.argv[1]=='help'):
        ## Displaying the program help content.
        print ">> AtoZ Product Name Matching Program ..."
        print ">> Match product name in product description table, with the product name in order_product table."
        print ">> Higher matching rate will be scored if model number matched in product name between 2 list."
        print ""
        print ">> Usage: pnm <product_desc_csv> <order_product_csv> <output_list_csv>"

    elif (sys.argv[1]=='rework'):
        print ">> AtoZ Product Name Matching Program ..."
        print ">> Rework case."
        ## Command
        ## python pnm.py rework rework-source.csv rework-ref-green.csv rework-ref-red.csv green-output.csv red-output.csv
        
        ## Getting the parameters ...
        rework_source_csv = str(sys.argv[2])
        ref_green_csv = sys.argv[3]
        ref_red_csv = sys.argv[4]
        green_output_csv = sys.argv[5]
        red_output_csv = sys.argv[6]       

        print "--- Reowrk Input files validation ---" 
        print "Source CSV : %s" % rework_source_csv
        print ""
        print "Reference GREEN CSV : %s" % ref_green_csv
        print "Reference RED CSV : %s" % ref_red_csv
        print ""
        print "Target GREEN Output CSV : %s" % green_output_csv
        print "Target RED Output CSV : %s" % red_output_csv
        print ""

        ## Read in ... rework_source_csv 
        print "Read in [%s]..." % (rework_source_csv)
        with open(rework_source_csv, 'r') as f_rework_source:
            reader = csv.reader(f_rework_source)
            lst_rework_source = list(reader)
        ttl_rework_source_rcd = len(lst_rework_source)        
        print "Successfully read in %s with lines %s" % (rework_source_csv, str(ttl_rework_source_rcd))
        print ""

        ## Read in ... rework_ref_green_csv 
        print "Read in [%s]..." % (ref_green_csv)
        with open(ref_green_csv, 'r') as f_ref_green_csv:
            reader = csv.reader(f_ref_green_csv)
            lst_ref_green_csv = list(reader)
        ttl_ref_green_rcd = len(lst_ref_green_csv)        
        print "Successfully read in %s with lines %s" % (ref_green_csv, str(ttl_ref_green_rcd))
        print ""

        ## Read in ... rework_ref_red_csv 
        print "Read in [%s]..." % (ref_red_csv)
        with open(ref_red_csv, 'r') as f_ref_red_csv:
            reader = csv.reader(f_ref_red_csv)
            lst_ref_red_csv = list(reader)
        ttl_ref_red_rcd = len(lst_ref_red_csv)        
        print "Successfully read in %s with lines %s" % (ref_red_csv, str(ttl_ref_red_rcd))
        print ""

        ## Looping throgh all source, identify GREEN or RED item to output list.
        lst_red_output = []
        lst_green_output = []
        lst_escape_output = []

        ttl_rework_rcd = len(lst_rework_source)
        rework_ctr = 0
        for lst_si in lst_rework_source:
            curr_order_id = lst_si[0]
            curr_old_prod_id = lst_si[1]
            curr_old_prod_name = lst_si[2].strip()

            ##Find item in GREEN list first.
            b_find_in_green = False
            for lst_green_si in lst_ref_green_csv:
                green_prod_name = lst_green_si[2].strip()
                ## if(curr_order_id == lst_green_si[0] and curr_old_prod_id == lst_green_si[1]):
                ## if(curr_old_prod_name == green_prod_name or (curr_order_id == lst_green_si[0] and curr_old_prod_id == lst_green_si[1])):
                ## if(curr_order_id == lst_green_si[0] and curr_old_prod_id == lst_green_si[1]):
                ## if(curr_old_prod_name == green_prod_name or (similar(curr_old_prod_name, green_prod_name)>0.95)):
                if(curr_old_prod_name == green_prod_name):
                    b_find_in_green = True
                    rework_prod_id = lst_green_si[6]
                    rework_prod_name = lst_green_si[7]
                    lst_green_output.append([curr_order_id, curr_old_prod_id, curr_old_prod_name, rework_prod_id, rework_prod_name])
                    break
            
            ## Item not found in GREEN list, must be in RED list. Verify
            b_find_in_red = False
            if(b_find_in_green == False):
                for lst_red_si in lst_ref_red_csv:
                    red_prod_name = lst_red_si[2].strip()
                    ## if(curr_order_id == lst_red_si[0] and curr_old_prod_id == lst_red_si[1]):
                    ## if(curr_old_prod_name == red_prod_name or (curr_order_id == lst_red_si[0] and curr_old_prod_id == lst_red_si[1])):
                    ## if(curr_order_id == lst_red_si[0] and curr_old_prod_id == lst_red_si[1]):
                    ## if(curr_old_prod_name == red_prod_name or (similar(curr_old_prod_name, red_prod_name)>0.95)):
                    if(curr_old_prod_name == red_prod_name):
                        b_find_in_red = True
                        lst_red_output.append([curr_order_id, curr_old_prod_id, curr_old_prod_name])
                        break
            
            ## If item do not found in GREEN and RED list, escape item. No suppor to have.
            if(b_find_in_green == False and b_find_in_red == False):
                print "Escape item found!! Order_id = %s, Prod_id = %s" % (curr_order_id, curr_old_prod_id)
                print ""
                lst_escape_output.append([curr_order_id, curr_old_prod_id, curr_old_prod_name])

            rework_ctr = rework_ctr + 1            
            rework_pp = float(rework_ctr*100) / float(ttl_rework_rcd)
            print "Complete processed Rework records ... [%d / %d], [%.2f%%] completed\r" % (rework_ctr, ttl_rework_rcd, rework_pp),


        ## End of all source loop, output list.
        print ""
        print "Output Total %s Records of GREEN list into ... %s" % (str(len(lst_green_output)), green_output_csv)
        save_list_to_file(lst_green_output, green_output_csv)
        print ""

        print "Output Total %s Records of RED list into ... %s" % (str(len(lst_red_output)), red_output_csv)
        save_list_to_file(lst_red_output, red_output_csv)
        print ""

        if(len(lst_escape_output) > 0):
            print "Output Total %s Records of ESCAPE list into ... %s" % (str(len(lst_escape_output)), "rework-escape.csv")
            save_list_to_file(lst_escape_output, "rework-escape.csv")
            print ""

        print "Rework operation completed!"

    elif (sys.argv[1]=='test'):
        ## Operation testing.
        print "Testing procedure area ..."

        '''
        test1 = "High-grade"
        test2 = "HS5-GANG"
        test3 = "18-2"
        test1 = test1.replace("-", "")
        test2 = test2.replace("-", "")
        test3 = test3.replace("-", "")                
        print test1.isalpha(); print test2.isalpha(); print test3.isalpha()
        print test1.isalnum(); print test2.isalnum(); print test3.isalnum()
        print test1.isdigit(); print test2.isdigit(); print test3.isdigit()
        '''

        ## order_prod = "  Epson 141 SET Ink Cartridge (CMYK) *** BUY 1 SET FREE 1 LAPTOP LOCK"               
        order_prod = "EPSON L210 — A4 3-in-1 Print/Scan/Copy USB Color Inkjet Printer"
        ## desc_prod = "HP 951XL Cyan OJ ink cartr"
        ## desc_prod = "HP 704 Black Ink Cartridge (CN692AA)" ##39 0.78
        ## desc_prod = "Kristall Liquid Screen Protector - SmartPhone"
        desc_prod = "Canon PIXMA MG3170 — A4 3-in-1 Print/Scan/Copy WiFi Color Inkjet Printer"

        if(order_prod == desc_prod): print "Equal"
        print similar(order_prod, desc_prod)
        print (similar(order_prod, desc_prod) > 0.8)
        
        '''
        ## Process prod_desc
        print "Starting == %s" % desc_prod
        curr_prod = special_trim( desc_prod );          print curr_prod 
        curr_prod = special_replace( curr_prod );       print curr_prod 
        curr_prod = special_remove( curr_prod );        print curr_prod 
        curr_prod = curr_prod.lower();                  print curr_prod 
        curr_prod = special_word_remove( curr_prod );   print curr_prod 
        lst_desc_token = clean_token_list( curr_prod.split() );     print lst_desc_token
        lst_desc_token = extend_desc_token_list(lst_desc_token);    print lst_desc_token

        ## Process order_prod
        print "Starting == %s" % order_prod 
        curr_prod = special_trim( order_prod );     print curr_prod 
        curr_prod = special_replace( curr_prod );   print curr_prod 
        curr_prod = special_remove(curr_prod);      print curr_prod 
        curr_prod = curr_prod.lower();              print curr_prod 
        curr_prod = special_word_remove(curr_prod); print curr_prod 
        lst_order_token = clean_token_list(curr_prod.split());      print lst_order_token
        lst_order_token = extend_op_token_list(lst_order_token);    print lst_order_token
        
        total_weight = calc_ttl_token_weight(lst_order_token, False)
        print lst_order_token, total_weight

        mr = match_rate(lst_desc_token, lst_order_token, total_weight, True)
        print "Matching rate = %f" % mr        
        '''

    else:
        ## Debuging flag
        ## df = True
        df = False

        ## Defining variables.
        lst_prod_desc = []          ## Original read in product description list.        
        lst_order_prod = []         ## Original read in order product list.
        lst_output = []             ## Holding the output list.
        output_tupple = []          ## Holding the output tupple for every element in list.
        match_no_desc = []          ## Order Product match nothing in prod-desc.

        ## Define list for rating operation storage. 
        ## Subscrib to nested list concept.
        ## Storing tokenized words in a list that attached in order-id, product-id list.
        lst_prod_desc_token = []    ## Holding tokenized words for product description.
        lst_order_prod_token = []   ## Holding tokenized words for order product.

        ## Getting the parameters ...
        product_desc_csv = str(sys.argv[1])
        order_product_csv = sys.argv[2]
        output_csv = sys.argv[3]

        ## Start generating the records...
        print "--- Input files validation ---" 
        print "Product Desciption CSV : %s" % (product_desc_csv)
        print "Order Product CSV : %s" % order_product_csv
        print "Target Output CSV : %s" % output_csv
        print ""

        ## Read in ... Product Desciption 
        print "Read in [%s]..." % (product_desc_csv)
        with open(product_desc_csv, 'r') as f_prod_desc:
            reader = csv.reader(f_prod_desc)
            lst_prod_desc = list(reader)
        ttl_rcd = len(lst_prod_desc)
        last_idx = ttl_rcd - 1
        print "Successfully read in %s with lines %s" % (product_desc_csv, str(ttl_rcd))

        ## Test print and access element.
        print "Line no. %d = %s" % (ttl_rcd, lst_prod_desc[last_idx])
        print "Line no. %d = %s, Item no.2 : %s" % (ttl_rcd, lst_prod_desc[last_idx], lst_prod_desc[last_idx][1])
        print ""

        ## Read in ... Order Product
        print "Read in [%s]..." % (order_product_csv)
        with open(order_product_csv, 'r') as f_order_prod:
            reader = csv.reader(f_order_prod)
            lst_order_prod = list(reader)
        ttl_ord_prod_rcd = len(lst_order_prod)
        last_idx = ttl_ord_prod_rcd - 1
        print "Successfully read in %s with lines %s" % (order_product_csv, str(ttl_ord_prod_rcd))

        ## Test print and access element.
        print "Line no. %d = %s" % (ttl_ord_prod_rcd, lst_order_prod[last_idx])
        print "Line no. %d = %s, Item no.3 : %s" % (ttl_ord_prod_rcd, lst_order_prod[last_idx], lst_order_prod[last_idx][2])
        print ""

        ## Generating token in product desc list.
        ## Loop through every item in product description list.        
        for lst_pd in lst_prod_desc:
            ## First item in every list item holding product description.
            curr_prod = special_trim(lst_pd[1])                             ## Apply special Trim function.
            curr_prod = special_replace( curr_prod )                        ## Apply special replace function.
            curr_prod = special_remove(curr_prod)                           ## Apply special Character remove function.
            curr_prod = curr_prod.lower()                                   ## To lower case before tokenizing.
            curr_prod = special_word_remove(curr_prod)                      ## Remove special words.            
            lst_pd_token = clean_token_list(curr_prod.split())              ## Cleaned tokenized list.
            lst_pd_token = extend_desc_token_list(lst_pd_token)             ## Extend list token for prod desc.
            
            ## Attach into new list, store old value + token.
            lst_prod_desc_token.append([lst_pd[0], lst_pd[1], lst_pd_token])
        print "Completed tokenized Product Description list...\n"

        ## Generating token in order product list.
        ## Loop through every item in order product list.
        op_ctr = 0
        for lst_op in lst_order_prod:
            ## Second item in every list item holding product description.
            curr_prod = special_trim(lst_op[2])                             ## Apply special Trim function.
            curr_prod = special_replace( curr_prod )                        ## Apply special replace function.
            curr_prod = special_remove(curr_prod)                           ## Apply special Character remove function.
            curr_prod = curr_prod.lower()                                   ## To lower case before tokenizing.
            curr_prod = special_word_remove(curr_prod)                      ## Remove special words.
            lst_op_token = clean_token_list(curr_prod.split())              ## Tokenized list.
            lst_op_token = extend_op_token_list(lst_op_token)               ## Extend list token for order prod.
            
            total_weight = calc_ttl_token_weight(lst_op_token, False)       ## Total token weight.
            
            ## Attach into new list, store old value + token + total weight.
            lst_order_prod_token.append([lst_op[0], lst_op[1], lst_op[2], lst_op_token, total_weight])

            ## Output tokenizing progress for order products..."
            op_ctr = op_ctr + 1
            op_pp = float(op_ctr*100) / float(len(lst_order_prod))
            print "Tokenizing order-product-name [%s / %s], [%.2f%%] completed... \r" % (op_ctr, len(lst_order_prod), op_pp),
        
        print ""
        print "Completed tokenized Order Product list + Total Rating calculation... \n"

        ## For every item in order-product list.
        ctr = 1             ## Initialize counter.
        id_match_case = 0   ## Hold the number of case that id match or success rate.
        for op_ele in lst_order_prod_token:
            ## if(df): print "DEBUG: Process Order_Prod_Lst : %s" % (op_ele)
            order_id = op_ele[0]        ## Record the order-id for update sql generation purpose.
            old_prod_id = op_ele[1]     ## Record the old-prod-id.
            old_prod_name = op_ele[2]   ## Record the old-prod-name.
            lst_op_token = op_ele[3]    ## Get the order-prod-token list.
            total_weight = op_ele[4]    ## Obtain pre-calculated total weight.
            
            max_rate = 0.0              ## Set the max-rating = 0
            curr_rate= 0.0              ## Reset current rating.
            chg_prod_id = None          ## Set the chg-prod-id = null
            chg_prod_desc = None        ## Set the curr-prod-desc = null
            
            ## For every item in product-desc list.
            for prod_desc_ele in lst_prod_desc_token:
                ## if(df): print "DEBUG: Process Desc_Prod_Lst : %s" % (prod_desc_ele)
                curr_prod_id = prod_desc_ele[0]     ## Record the new-product-id
                lst_pd_token = prod_desc_ele[2]     ## Get the prod-desc-token list.

                ## Perform rating calculation, curr-rate.                
                curr_rate = match_rate(lst_pd_token, lst_op_token, total_weight, False)
                if(df): print "curr_rate=%f, max_rate=%f" % (curr_rate, max_rate)

                ## Reset max-rating = curr-rate IF curr-rate > max-rating.
                ## if(curr_rate >= 1.0): print "curr_rate=%f, max_rate=%f" % (curr_rate, max_rate)
                if(curr_rate > max_rate):                    
                    max_rate = curr_rate                ## Reset max-rating = curr-rate
                    chg_prod_id = curr_prod_id          ## Reset the chg-prod-id = new-product-id
                    chg_prod_desc = prod_desc_ele[1]    ## Reset the curr-prod-desc = curr item product-desc
                    if(df): print "DEBUG: curr_rate=%f, chg_prod_id=%s, chg_prod_desc=%s, max_rate=%f" % (curr_rate, chg_prod_id, chg_prod_desc, max_rate) 
                else:
                    curr_rate = 0.0

                if(curr_rate >= 1.0): break             ## Save some time to loop thru other when getting max scoring. 
            ## End loop of prod-desc-element.
            
            ## If old-prod-id != chg-prod-id, then add record to list.            
            ## Record only different product-id case.
            if( chg_prod_id == None ):
                ## Matching nothing case.
                tmp_lst = [order_id, old_prod_id, old_prod_name, lst_op_token, total_weight]
                match_no_desc.append( tmp_lst )
                if(df): print "DEBUG: No match case. %s" % (tmp_lst)
            else:
                if(old_prod_id != chg_prod_id):
                    ## print "DEBUG: old_prod_id=%s, chg_prod_id=%s, max_rate=%f" % (old_prod_id, chg_prod_id, max_rate)
                    ## Setup the output list content.
                    ## Output-List = (old-prod-id, order-prod-name, chg-prod-id, curr-prod-desc, max-rating)
                    output_tupple.append([order_id, old_prod_id, old_prod_name, chg_prod_id, chg_prod_desc, max_rate])
                else:
                    id_match_case = id_match_case + 1
                    if(df): print "DEBUG: Increase Prod-ID match case."
            
            ## Output processign state, % processing.
            pp = float(ctr*100) / float(ttl_ord_prod_rcd)
            print "Complete processed Order Product records ... [%d / %d], [%.2f%%] completed\r" % (ctr, ttl_ord_prod_rcd, pp),
            
            ctr = ctr + 1   ## Increase process counter.
        ## End loop of order-prod-element.

        ## Ouptut output-list statistic.
        print "Complete processed ALL Order Product items."
        
        ## Output the output result list
        lst_proc_output = []
        ## For every item in output-list
        for out_ele in output_tupple:
            ## If max-rating > OUTPUT_THRESHOLD_RATING, then
            if(out_ele[5] >= OUTPUT_THRESHOLD_RATING):
                ## Add item into output list.
                lst_proc_output.append( [out_ele[0], out_ele[1], out_ele[2], out_ele[3], out_ele[4], out_ele[5]] )
        
        ## Output processed statistic 
        output_case = len(output_tupple)
        output_th_case = len(lst_proc_output)
        matched_case = output_case  + id_match_case
        match_no_desc_case = len(match_no_desc)
        print ""
        print "Successfully matched case with Order-Product-ID == Description-Product-ID : %d" % id_match_case
        print "Successfully matched case with Different Product ID : %d" % output_case
        print "Order Product ID match no case : %d" % match_no_desc_case
        print "Successfully output cases with Threshold=%d : %d" % (OUTPUT_THRESHOLD_RATING, output_th_case)
        print "Matching percentage : %.2f%%" % (float(matched_case*100) / float(ttl_ord_prod_rcd))
        print "Output case percentage : %.2f%%" % (float(output_th_case*100) / float(ttl_ord_prod_rcd))

        ## Dump list into file.
        save_list_to_file(lst_proc_output, output_csv)
        save_list_to_file(match_no_desc, "match_no_case.csv")

        print("Operation completed!")



