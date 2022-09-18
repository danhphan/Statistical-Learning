
# # Date and Time type in R
# Date/time classes
# Three date/time classes are built-in in R, Date, POSIXct, and POSIXlt.

##################################################
## DATE
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

# Time calculation
difftime <- d3 - d2
difftime

dt2 <- difftime(d3,d2) # Default units is days
dt2
dt3 <- difftime(d3,d2,units="weeks")
dt3
dt4 <- difftime(d3,d2,units="hours")
dt4
# Add or subtract a number of days
d3
d3 + 10
d3-10

# create a vector of dates and find the intervals between them:
three.dates <- as.Date(c("2010-07-22", "2011-04-20", "2012-10-06"))
three.dates
diff(three.dates)
# Time differences in days
# [1] 272 535

# see the internal integer representation
unclass(d2)

####################################################
## Chron
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
class(thetimes)


## POSIX TIME

#############################################################
# POSIXct store date/time value as the nunber of second since 1/1/1970

# POSIXct
# If you have times in your data, this is usually the best class to use.

tm1 <- as.POSIXct("2013-07-24 23:55:26")
tm1
tm2 <- as.POSIXct("25072013 08:32:07", format = "%d%m%Y %H:%M:%S")
tm2

# specify the time zone:
tm3 <- as.POSIXct("2010-12-01 11:42:03", tz = "GMT")
tm3
unclass(tm1)
# Calculation
difftime(tm1,tm2,units="secs")
difftime(tm1,tm2,units="hours")

# A vector of dates
dts = c(1127056501,1104295502,1129233601,1113547501,
                 1119826801,1132519502,1125298801,1113289201)
mydates <- dts
class(mydates) <- c('POSIXt','POSIXct')
mydates
# Another way todo it
mydates <- structure(dts,class=c('POSIXt','POSIXct'))


mydate = as.POSIXct('2005-4-19 7:01:00')
mydate
days(mydate)
hours(mydate)
minutes(mydate)
seconds(mydate)
minutes(hdates)


# specify the time zone:
  
tm3 <- as.POSIXct("2010-12-01 11:42:03", tz = "GMT")
tm3
tm4 <- as.POSIXct('2013/2/23 5:6:04',tz="GMT")
tm4

#############################################################
# POSIXlt
# POSIXlt store a list of elements: second, minute, hour, day, month, and year
# This class enables easy extraction of specific componants of a time. 
# (“ct” stand for calender time and “lt” stands for local time. 
# “lt” also helps one remember that POXIXlt objects are lists.)
tm1.lt <- as.POSIXlt("2013-07-24 23:55:26")
tm1.lt
unclass(tm1.lt)
# Extract components
tm1.lt$sec
tm1.lt$min
tm1.lt$hour
tm1.lt$wday
tm1.lt$day
tm1.lt$mon
months(tm1.lt)
tm1.lt$year
years(tm1.lt)


## Create a list
dts = c("2005-10-21 18:47:22","2005-12-24 16:39:58",
        "2005-10-28 07:30:05 PDT")
pxdt <- as.POSIXlt(dts)
pxdt

hdates <- as.POSIXlt('2005-4-6 7:01:02')
hdates

