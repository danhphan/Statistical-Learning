
# Time series analysis
# get data
$wget–no-check-certificate–progress=dot https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD > chicago_crime_data.csv

library(data.table)
dat = fread("chicago_crime_data.csv")
colnames(dat) = gsub(" ", "_", tolower(colnames(dat)))
dat[, date2 := as.Date(date, format="%m/%d/%Y")]
mydat = dat[primary_type=="THEFT", .N, by=date2][order(date2)]
mydat[1:6]

