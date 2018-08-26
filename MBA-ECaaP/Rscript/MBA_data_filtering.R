# load installed package library
library(tidyr)
library(plyr)
library(dplyr)

# Import dataset 
read_data <- read.csv("u_cust_prd_ord.csv", header = TRUE, stringsAsFactors = FALSE)

# Filter specific column
filtered_data <- data.frame(read_data$email.x,
                            read_data$mth_yr,
                            read_data$category_code)

# Rename filtered column
colnames(filtered_data)[1] <- "email"
colnames(filtered_data)[2] <- "mth_yr"
colnames(filtered_data)[3] <- "category"

# Splitting data by months
monthly_split <- split(filtered_data, filtered_data$mth_yr)

# access list of months and keep it in a data frame for reference, in this case, the first list of month is accessed.by_months <- as.data.frame(split_by_months[1])
by_months <- as.data.frame(monthly_split[30])

# Rename filtered column
colnames(by_months)[1] <- "email"
colnames(by_months)[2] <- "mth_yr"
colnames(by_months)[3] <- "category"

# Generate CSV file
write.csv(by_months, file="16-Mar_prod.csv") 