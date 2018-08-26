##############################################################################################################
## Version 1.2
## Filename: v1.0-AtoZ-MBA.R
## Description : AtoZ MBA Analysis - Generate images for MBA for displaying in dashboard.
##               Generate relationship diagrams for 3 dataset: Overall business, YTD, Month
## Start Date : 20-Nov-2017
## Last Modified Date : 25-Nov-2017
## 
## Modification Version :
## 21-Nov-17    Start version. - Modification minimize execution.
##              Required packages:
##                  install.packages("arules")
##                  install.packages("arulesViz")
##                  install.packages("plyr", dependencies = TRUE)
##   
##  25-Nov-17   Updated R-studio version for eliminating graphic warning.
##              Testing with generated item list data.
##  29-Nov-17   Experiments + coding in all necessaries statement for different data sources.
##  30-Nov-17   Finalize output image for each category.
##
##############################################################################################################

# Load the libraries
library(arules)
library(arulesViz)
library(plyr)
library(colorspace) # for sequential_hcl

#--- Clear previous memory set. ------------
rm(list=ls())

#-------Set working directory. ------------
setwd("C:\\Python27\\MBA-ECaaP\\working")

#------------------------------------------------Association Rules----------------------------
# Convert itemlist data to basket transaction data
## txn = read.transactions(file="14-Jun_ItemList.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)
## txn = read.transactions(file="dev-test.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)
txn_A = read.transactions(file="31102017-A-mba-source.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)
## txn_S = read.transactions(file="31102017-S-mba-source.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)
## txn_M = read.transactions(file="31102017-M-mba-source.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)
## txn_P = read.transactions(file="31102017-P-mba-source.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)

## Display Summary of transaction
summary(txn_A)
## summary(txn_S)
## summary(txn_M)
## summary(txn_P)

# Analysis Rule based on Analysis Category Code
## rules <- apriori(txn, parameter = list(supp = 0.001, conf = 0.8, maxlen=3))
## rules_A <- apriori(txn_A, parameter = list(supp = 0.001, conf = 0.5))
## rules_A <- sort(rules_A, by="confidence", decreasing=TRUE)

# Analysis Rule based on Sub-Category
## rules_S <- apriori(txn_S, parameter = list(supp = 0.001, conf = 0.8))
## rules_S <- sort(rules_S, by="confidence", decreasing=TRUE)

# Analysis Rule based on Manufacturing
## rules_M <- apriori(txn_M, parameter = list(supp = 0.001, conf = 0.8))
## rules_M <- sort(rules_M, by="confidence", decreasing=TRUE)

# Analysis Rule based on Product Name
## rules_P <- apriori(txn_P, parameter = list(supp = 0.001, conf = 0.5))
## rules_P <- sort(rules_P, by="confidence", decreasing=TRUE)

## summary(rules_A)
## inspect(rules_A)
## plot(rules_A[1:5], method='graph')
## plot(rules_A[1:22], method='grouped')

## summary(rules_S)
## inspect(rules_S)

## summary(rules_M)
## inspect(rules_M)

## summary(rules_P)
## inspect(rules_P[200:220])

## Avoid redundancy of generated rules
## subset.matrix <- is.subset(rules, rules)
## subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
## redundant <- colSums(subset.matrix, na.rm=T) >= 1
## rules.pruned <- rules[!redundant]
## rules <- rules.pruned

# getting relationship of what product does customer likely to buy if they bought office equipment
## rules<-apriori(data=txn, parameter=list(supp=0.001, conf = 0.08), 
##               appearance = list(default="lhs", rhs="Office Equipments"),
##               control = list(verbose=F))
## rules<-sort(rules, decreasing=TRUE, by="confidence")
## oe_rules<-apriori(data=txn_A, parameter=list(supp=0.001, conf = 0.08), 
##                  appearance = list(default="lhs", rhs="OFFICE EQUIPMENT"),
##                  control = list(verbose=F))
## oe_rules<-sort(oe_rules, decreasing=TRUE, by="confidence")

## Display Summary of rules
## summary(oe_rules)
## inspect(oe_rules)

ink_rules  <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="INK"), control = list(verbose=F))
t_rules    <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="TONER"), control = list(verbose=F))
pa_rules   <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="PAPER"), control = list(verbose=F))
p_rules    <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="PRINTER"), control = list(verbose=F))
oe_rules   <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="OFFICE EQUIPMENT"), control = list(verbose=F))
s_rules    <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="STATIONARY"), control = list(verbose=F))
tech_rules <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="TECHNOLOGY"), control = list(verbose=F))
c_rules    <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="CLEANING"), control = list(verbose=F))
b_rules    <- apriori(data=txn_A, parameter=list(supp=0, conf = 0, minlen=2), appearance = list(default="rhs", lhs="BREAKROOM"), control = list(verbose=F))

ink_rules  <- sort(ink_rules, decreasing=TRUE, by="confidence")
t_rules    <- sort(t_rules, decreasing=TRUE, by="confidence")
pa_rules   <- sort(pa_rules, decreasing=TRUE, by="confidence")
p_rules    <- sort(p_rules, decreasing=TRUE, by="confidence")
oe_rules   <- sort(oe_rules, decreasing=TRUE, by="confidence")
s_rules    <- sort(s_rules, decreasing=TRUE, by="confidence")
tech_rules <- sort(tech_rules, decreasing=TRUE, by="confidence")
c_rules    <- sort(c_rules, decreasing=TRUE, by="confidence")
b_rules    <- sort(b_rules, decreasing=TRUE, by="confidence")


plot(ink_rules, method='graph', control=list(verbose=F, main=""))
dev.copy(device=png, filename="ink_rules.png", width=1000, height=800)
dev.off()

plot(b_rules, method='graph', control=list(verbose=F, main=""))
dev.copy(device=png, filename="b_rules.png", width=1000, height=800)
dev.off()
