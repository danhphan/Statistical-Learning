
# Time series analysis
# # get data
# $wget–no-check-certificate–progress=dot https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD > chicago_crime_data.csv
# 
# library(data.table)
# dat = fread("chicago_crime_data.csv")
# colnames(dat) = gsub(" ", "_", tolower(colnames(dat)))
# dat[, date2 := as.Date(date, format="%m/%d/%Y")]
# mydat = dat[primary_type=="THEFT", .N, by=date2][order(date2)]
# mydat[1:6]
# 

set.seed(123)
t <- seq(from = 1, to = 100, by = 1) + 10 + rnorm(100, sd = 7)
t
plot(t)
length(t)
args(ts)
class(ts)
typeof(ts)

tseries <- ts(t,start = c(2000,1),frequency = 4)
print(tseries)
plot(tseries)

set.seed(123)
seq <- seq(from = 1, to = 100, by = 1) + 10
ts1 <- seq + rnorm(100, sd = 5)
ts2 <- seq + rnorm(100, sd = 12)
ts3 <- seq^2 + rnorm(100, sd = 300)
tsm <- cbind(ts1, ts2, ts3)
tsm <- ts(tsm, start=c(2000, 1), frequency = 4)
plot(tsm)
class(tsm)
typeof(tsm)

plot.ts(tsm)

tseries_sub <- window(tseries,start=c(2000,1),end=c(2012,4))
plot.ts(tseries_sub)
start(tsm)
end(tsm)
frequency(tsm)

# Tidy Time Series Analysis
#install.packages("tidyquant")
#install.packages("cranlogs")
library(tidyquant)  # Loads tidyverse, tidquant, financial pkgs, xts/zoo
library(cranlogs)   # For inspecting package downloads over time

