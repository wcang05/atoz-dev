#install.packages("arules")
#install.packages("arulesViz")
#install.packages("plyr", dependencies = TRUE)

# Load the libraries
library(arules)
library(arulesViz)
library(plyr)

# Import product Data by month 
df_monthly <- read.csv("14-Jun_prod.csv")
str(df_monthly)

# Data can't be easily converted to string, so have to increase it's row access level to give more privilege for editing
levels(df_monthly$category) <- c(levels(df_monthly$category), "Clearing & breakdown")
df_monthly$category[df_monthly$category == "CB"] <- "Clearing & breakdown"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Ink")
df_monthly$category[df_monthly$category == "I"] <- "Ink"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Others")
df_monthly$category[df_monthly$category == "O"] <- "Others"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Office Equipments")
df_monthly$category[df_monthly$category == "OE"] <- "Office Equipments"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Printer")
df_monthly$category[df_monthly$category == "P"] <- "Printer"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Ribbon")
df_monthly$category[df_monthly$category == "R"] <- "Ribbon"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Stationary")
df_monthly$category[df_monthly$category == "S"] <- "Stationary"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Technology")
df_monthly$category[df_monthly$category == "TE"] <- "Technology"

levels(df_monthly$category) <- c(levels(df_monthly$category), "Toner")
df_monthly$category[df_monthly$category == "TO"] <- "Toner"

# Sort data by email
df_sorted <- df_monthly[order(df_monthly$email),]

#convert item description to categorical format
df_sorted$category <- as.factor(df_sorted$category)
str(df_sorted)

# Check top and least product of the month
user_purchase <- count(df_sorted, 'category')
user_purchase <- arrange(user_purchase, desc(freq))
user_purchase["Mth_yr"] <- "2014-06"
write.csv(user_purchase,"14-Jun_prdsales.csv", row.names = TRUE)

# Check repeating customer
rep_cust <- data.frame(df_sorted$email)
colnames(rep_cust)[1] <- "email"
repeat_customer <- ddply(rep_cust,.(email),nrow)
rep_customer <- arrange(repeat_customer, desc(V1))
colnames(rep_customer)[2] <- "No. of Transaction"
rep_customer["Mth_yr"] <- "2014-06"
write.csv(rep_customer,"14-Jun_repcust.csv", row.names = TRUE)

# Merge related information like same user transaction in same month
df_itemList <- ddply(df_monthly,c("email","mth_yr"), 
                     function(df1)paste(df1$category, 
                                        collapse = ","))

# Remove email and mth_yr from data
df_itemList$email <- NULL
df_itemList$mth_yr <- NULL

#Rename column headers for ease of use
colnames(df_itemList) <- c("itemList")

# Generate csv file of data
write.csv(df_itemList,"14-Jul_ItemList.csv", row.names = TRUE)

#------------------------------------------------Association Rules----------------------------
# Convert itemlist data to basket transaction data
txn = read.transactions(file="14-Jun_ItemList.csv", rm.duplicates= TRUE, format="basket",sep=",",cols=1)

# remove double quotes in dataset
txn@itemInfo$labels <- gsub("\"","",txn@itemInfo$labels)

# visualize in descending order what product involve in transaction monthly
itemFrequencyPlot(txn,topN=10,type="absolute")

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
rules<-rules.pruned

# getting relationship of what product does customer likely to buy if they bought office equipment
rules<-apriori(data=txn, parameter=list(supp=0.001,conf = 0.08), 
               appearance = list(default="lhs",rhs="Office Equipments"),
               control = list(verbose=F))
rules<-sort(rules, decreasing=TRUE,by="confidence")

# if rules is not generated, lower confidence and support level for apriori algorithm is executed
rules<-apriori(data=txn, parameter=list(supp=0.001,conf = 0.08,minlen=2), 
               appearance = list(default="rhs",lhs="Office Equipments"),
               control = list(verbose=F))
rules<-sort(rules, decreasing=TRUE,by="confidence")

# Plot the 
png(filename="13-Dec_MBA_O.png")
plot(rules,method="graph",interactive=TRUE,shading=NA)
dev.off()