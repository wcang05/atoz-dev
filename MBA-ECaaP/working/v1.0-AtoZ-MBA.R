##############################################################################################################
## Version 1.0
## Filename: v1.0-AtoZ-MBA.R
## Description : AtoZ MBA Analysis - Generate images for MBA for displaying in dashboard.
##               Generate relationship diagrams for 3 dataset: Overall business, YTD, Month
## Start Date : 20-Nov-2017
## Last Modified Date : 21-Nov-2017
## 
## Modification Version :
## 1. Start version. - Modification minimize execution.
##    Required packages:
##       install.packages("arules")
##       install.packages("arulesViz")
##       install.packages("plyr", dependencies = TRUE)
## 
##
##############################################################################################################

# Load the libraries
library(arules)
library(arulesViz)
library(plyr)

#-------Set working directory. ------------
setwd("C:\\Python27\\MBA-ECaaP\\working")

#------------------------------------------------Association Rules----------------------------
# Convert itemlist data to basket transaction data
txn = read.transactions(file="14-Jun_ItemList.csv", rm.duplicates= TRUE, format="basket", sep=",", cols=1)

# remove double quotes in dataset
txn@itemInfo$labels <- gsub("\"","",txn@itemInfo$labels)

# Get the rules using apriori algorithm
rules <- apriori(txn, parameter = list(supp = 1, conf = 0.8))

# Sort rules
rules<-sort(rules, by="confidence", decreasing=TRUE)

# decrease support level and standardize rules to avoid long rules generated
rules <- apriori(txn, parameter = list(supp = 0.001, conf = 0.8,maxlen=3))

# avoid redundancy of generated rules
subset.matrix <- is.subset(rules, rules)
subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
redundant <- colSums(subset.matrix, na.rm=T) >= 1
rules.pruned <- rules[!redundant]
rules <- rules.pruned

# getting relationship of what product does customer likely to buy if they bought office equipment
rules<-apriori(data=txn, parameter=list(supp=0.001, conf = 0.08), 
               appearance = list(default="lhs", rhs="Office Equipments"),
               control = list(verbose=F))
rules<-sort(rules, decreasing=TRUE, by="confidence")

# if rules is not generated, lower confidence and support level for apriori algorithm is executed
rules<-apriori(data=txn, parameter=list(supp=0.001, conf = 0.08, minlen=2), 
               appearance = list(default="rhs", lhs="Office Equipments"),
               control = list(verbose=F))
rules<-sort(rules, decreasing=TRUE, by="confidence")

# Plot the 
png(filename="13-Dec_MBA_O.png")
# plot(rules,method="graph", interactive=TRUE,shading=NA)
plot(rules, method="graph", engine='interactive', shading=NA)

dev.off()

