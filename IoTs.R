
# IOTS

rm(list = ls())
gc()

# Load library and data sources
library(readr)
mdata <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/data/MPID_data.csv")
mpostcodes <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/data/MPID_Postcodes.csv")


dim(mpostcodes)
mpostcodes <- mpostcodes[,1:6]
str(mpostcodes)
mpostcodes <- as.data.frame(mpostcodes)
str(mpostcodes)

mpostcodes[which(mpostcodes$Area %in% "Ryde"),]

library(dplyr)

post_frequence <- mpostcodes %>% select(Pcode) %>% group_by(Pcode) %>% 
  mutate(countP=n()) %>% arrange(desc(countP))

post_frequence

test <- mpostcodes %>% group_by(Area) %>% mutate(countA =count(Pcode), spos <- sum(Pcode)) %>% arrange(desc(countA))
test

##################### DATA ANALYTIC ###################
dim(mdata)
mdata <- mdata[,1:32]
str(mdata[,20:32])

head(mdata)

