
# IOTS

rm(list = ls())
gc()
# Load library and data sources
library(readr)
library(ggplot2)
library(dplyr)


mpostcodes <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/data/MPID_Postcodes.csv")
mdata <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/data/MPID_data.csv")

# Explore data
# Postcodes table
dim(mpostcodes)
mpostcodes <- mpostcodes[,1:6]
str(mpostcodes)
class(mpostcodes)
mpostcodes[which(mpostcodes$Area %in% "Ryde"),]


# post_frequence <- mpostcodes %>% select(Pcode) %>% group_by(Pcode) %>% 
#   mutate(countP=n()) %>% arrange(desc(countP))


##################### DATA ANALYTIC ###################
dim(mdata)
mdata <- mdata[,1:28]
str(mdata[,20:28])
str(mdata)
head(mdata[,20:28])

#### QUESTION? ####
## PEAK HOURS EACH DAY ##
ggplot(data=mdata,aes(x=`Arrival Time`,y=Bus)) +
  geom_point()

ggplot(data=mdata,aes(x=`Arrival Time`,y=Train)) +
  geom_point()

boxplot(mdata$`Arrival Time`~mdata$`Travel Mode - Mon`)

test <- mdata %>% group_by(`Arrival Time`) %>% summarise(CountN =n())
test

testdata <- mdata %>% left_join(mpostcodes,by=c("Postcode"="Pcode"))
dim(mdata)
dim(testdata)

ggplot(data=test,aes(x=`Arrival Time`,y=CountN)) +
  geom_point()
hist(test$CountN~test$`Arrival Time`)

str(mpostcodes)
shapefile <- mpostcodes
data <- fortify(shapefile)
data
str(mdata)

################################################################
# Print Map
library(stringr)
testdata$`Arrival Time`
test2 <- as.character(testdata$`Arrival Time`)
test2 <- str_sub(test2,1,2)
test2
testdata$hours <- test2

loc <- geocode("21 Byfield St, Macquarie Park NSW 2113")
loc <- as.numeric(loc)
loc
macqpark <-get_map(location=loc,zoom=11)
macqmap <- ggmap(macqpark, extent = "device", legend = "topleft")

# Check from 5am, 6am, 7am
sub_data <- testdata[which(testdata$hours %in% c("05","06","07")),]
macqmap +
  stat_density2d(
    aes(x = Long, y = Lat, fill = ..level.., alpha = ..level..),
    size = 2, bins = 4, data = sub_data,
    geom = "polygon"
  ) +
  scale_fill_gradient(low = "black", high = "red") + 
  facet_wrap(~hours)


#############################
# Test qmap

help(qmap)

qmap('2 Lyonpark Rd Macquarie Park NSW 2113', zoom = 15, maptype = 'hybrid') +
  geom_polygon(aes(x = Long, y = Lat, group = Area), data = data,
               colour = 'white', fill = 'black', alpha = .4, size = .3)

# qmap(location = "Macquarie university")
# qmap(location = "Macquarie university", zoom = 14)
# qmap(location = "20 ethel street, eastwood, nsw, 2122", zoom = 14, source = "osm")
# qmap(location = "baylor university", zoom = 14, source = "osm", scale = 20000)
# qmap(location = "baylor university", zoom = 14, maptype = "satellite")
# qmap(location = "baylor university", zoom = 14, maptype = "hybrid")
# qmap(location = "baylor university", zoom = 14, maptype = "toner", source = "stamen")
# qmap(location = "baylor university", zoom = 14, maptype = "watercolor", source = "stamen")
# qmap(location = "Macquarie university", zoom = 14, maptype = "terrain-background", source = "stamen")
# qmap(location = "baylor university", zoom = 14, maptype = "toner-lite", source = "stamen")
