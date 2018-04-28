
# Mapping postcodes, longtitude and lattitude to map

require(ggplot2)


mpostcodes <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/data/MPID_Postcodes.csv")

dim(mpostcodes)
mpostcodes <- mpostcodes[,1:6]
str(mpostcodes)
mpostcodes <- as.data.frame(mpostcodes)
str(mpostcodes)

poacoord <- data.frame('poa'=mpostcodes$Pcode, 'lat'=mpostcodes$Lat, 'long'=mpostcodes$Long)

# Ratio Aus born vs elsewhere born
ratio <- data.frame('poa'=rep(10,100),'Freq'=rep(20,100))


popcount <- na.omit(merge(ratio, poacoord, all=FALSE))
popcount <- popcount[rev(order(popcount$Freq)),] # Place the small bubbles on top
popcount$cat <- sapply(popcount$Freq, function(x) if (x < 6) {'> 1:6'} else {'< 1:6'})


ggplot(popcount, aes(x=long, y=lat, colour=cat)) +
  scale_size(range = c(1,20), name = 'Population') +
  geom_point() +
  coord_equal()


#install.packages("ggmap")
library(ggmap)

set.seed(500)
df <- round(data.frame(
  x = jitter(rep(-95.36, 50), amount = .3),
  y = jitter(rep( 29.76, 50), amount = .3)
), digits = 2)
map <- get_googlemap('houston', markers = df, path = df, scale = 2)
ggmap(map, extent = 'device')


