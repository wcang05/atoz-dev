# install related package for data wrangling
#install.packages("tidyr")
#install.packages("plyr")
#install.packages("dplyr")

# load installed package library
library(tidyr)
library(plyr)
library(dplyr)

# read 2 related file with header and keep its formatting
raw_customer_data <- read.csv("u_customer_add.csv", header = TRUE, stringsAsFactors = FALSE)
raw_product_data <- read.csv("u_cust_prd_ord.csv", header = TRUE, stringsAsFactors = FALSE)

# separate customer id with email into different column in u_customer_add.csv
customer_data <- separate(data = raw_customer_data, col = customer_id, into = c("customer_id","email"), sep = ",")

# merge raw_product_data data with customer data by customer_id to create new data frame before analysis
# merge priority is given to raw_product_data (left join merging)
prep_data <- merge(raw_product_data, customer_data, by = c("customer_id"), all.x = TRUE)

# combining firstname and lastname to create company name
companies <- unite(prep_data, company_name, firstname.x, lastname.x, sep = " ")

#get list of month
months <- data.frame(companies$mth_yr)
colnames(months) <- "mth_yr"
months <- unique(months)

# Select only related attribute to be process
ready_data <- data.frame(companies$email.x, 
                         companies$company_name,
                         companies$postcode,
                         companies$category_code,
                         companies$total.x,
                         companies$mth_yr)

# rename each attribute in data frame
colnames(ready_data)[1] <- "email.x"
colnames(ready_data)[2] <- "company_name"
colnames(ready_data)[3] <- "postcode"
colnames(ready_data)[4] <- "category_code"
colnames(ready_data)[5] <- "total.x" 
colnames(ready_data)[6] <- "mth_yr"

# splitting data by each month 
split_by_months <- split(ready_data, ready_data$mth_yr)
  
# access list of months and keep it in a data frame for reference, in this case, the first list of month is accessed.by_months <- as.data.frame(split_by_months[1])
by_months <- as.data.frame(split_by_months[30])  

# rename each attribute in  reference data frame
colnames(by_months)[1] <- "email.x"
colnames(by_months)[2] <- "company_name"
colnames(by_months)[3] <- "postcode"
colnames(by_months)[4] <- "category_code" 
colnames(by_months)[5] <- "total.x"
colnames(by_months)[6] <- "mth_yr"
  
# create product view 
user_email <- table(by_months$email.x)
list_email <- as.data.frame(user_email)
list_email$Freq <- NULL
colnames(list_email)[1] <- "email.x"
list_product <- table(by_months$email.x, by_months$category_code)
check_product <- as.data.frame.matrix(list_product)
                  
# get total number of transaction per email
check_product <- transform(check_product, sum=rowSums(check_product))
  
# Convert Y if value is not null or N if value is null in category code
check_product$P[check_product$P != 0] <- "Y"
check_product$I[check_product$I != 0] <- "Y"
check_product$TO[check_product$TO != 0] <- "Y"
check_product$S[check_product$S != 0] <- "Y"
check_product$CB[check_product$CB != 0] <- "Y"
check_product$OE[check_product$OE != 0] <- "Y"
check_product$TE[check_product$TE != 0] <- "Y"
check_product$R[check_product$R != 0] <- "Y"
check_product$O[check_product$O != 0] <- "Y"
  
check_product$P[check_product$P == 0] <- "N"
check_product$I[check_product$I == 0] <- "N"
check_product$TO[check_product$TO == 0] <- "N"
check_product$S[check_product$S == 0] <- "N"
check_product$CB[check_product$CB == 0] <- "N"
check_product$OE[check_product$OE == 0] <- "N"
check_product$TE[check_product$TE == 0] <- "N"
check_product$R[check_product$R == 0] <- "N"
check_product$O[check_product$O == 0] <- "N"
  
# calculate total.x 
total <- data.frame(by_months$email.x, by_months$total.x)
total_updated <- ddply(total,"by_months$email.x",numcolwise(sum))
colnames(total_updated)[2] <- "total.x"
colnames(total_updated)[1] <- "email.x"
  
# avoiding multiple postcode attached to an email
postcode <- data.frame(by_months$email.x, by_months$postcode)
clean <- postcode[!duplicated(postcode[,1]),]
colnames(clean)[2] <- "Poskod"
colnames(clean)[1] <- "email.x"
  
# avoiding redundancy in company name column                                                                  #####
companyName <- data.frame(by_months$email.x, by_months$company_name)
cleanCompanyName <- unique(companyName)
colnames(cleanCompanyName)[2] <- "Company Name"
colnames(cleanCompanyName)[1] <- "email.x"

# combine separate chunks of processed data based on above code (left join merging)
first_part <- merge(cleanCompanyName, clean, by = c("email.x"), all.x = TRUE)
check_product <- cbind(list_email,check_product)
  
# sum that is empty will be filtered and this will shows the transaction that occurs by mth_yr
filter_check_product <- check_product[check_product$sum != 0,]
#second_part <- bind_rows(first_part,check_product)
#second_part <- cbind.fill(first_part,check_product)
  
# outer join merging for complete report by month
second_part <- merge(first_part, filter_check_product, by = c("email.x"), all=TRUE)
full_report <- merge(second_part, total_updated, by = c("email.x"), all = TRUE)
full_report["Mth_yr"] <- "16-Mar"
colnames(full_report)[13] <- "Number of transaction"

# Generate CSV file
write.csv(full_report, file="16-Mar.csv")  