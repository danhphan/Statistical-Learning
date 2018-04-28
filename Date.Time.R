
# Date and Time type in R

d <- as.Date("2015-6-23")
d
typeof(d)
class(d)

d1 <- as.Date("2010/5/21")
d1
class(d1)

d2 <- as.Date("3-23-2020",format="%m-%d-%Y")
d2

d3 <- as.Date("April 26, 2001",format="%B %d, %Y")
d3

d4 <- as.Date("22JUN01",format="%d%b%d")
d4

bdays = c(tukey=as.Date('1915-06-16'),fisher=as.Date('1890-02-17'),cramer=as.Date('1893-09-25'), kendall=as.Date('1907-09-06'))
bdays

weekdays(bdays)
months(bdays,abbreviate = TRUE)
quarters(bdays)

### chron library
#install.packages("chron")
library(chron)
dtimes = c("2002-06-09 12:45:40","2003-01-29 09:30:40",
                       "2002-09-04 16:45:40","2002-11-13 20:00:40",
                       "2002-07-07 17:30:40")
dtimes
dtparts = t(as.data.frame(strsplit(dtimes,' ')))
dtparts
row.names(dtparts) <- NULL
dtparts
thetimes <- chron(dates=dtparts[,1],times=dtparts[,2], format=c('y-m-d','h:m:s'))
thetimes
