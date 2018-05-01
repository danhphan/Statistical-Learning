
library(ggplot2)
library(readr)
library(VIM)
train <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/kaggle/train (1).csv")
test <- read_csv("D:/Drive/Persona/MIT Study/R Projects/Statistical Learning/kaggle/test (1).csv")

dim(train)
dim(test)

train <- train[,1:81]
test <- test[,1:80]
str(train)
str(test)

# Check missing parttern
help(aggr)
train_agg <- aggr(train, sortVars=TRUE)
# Variable        Count
# PoolQC 0.9952054795
# MiscFeature 0.9630136986
# Alley 0.9376712329
# Fence 0.8075342466
# FireplaceQu 0.4726027397

# Remove these variables
train$PoolQC <- NULL
train$MiscFeature <- NULL
train$Alley <- NULL
train$Fence <- NULL

summary(train$FireplaceQu)
unique(train$FireplaceQu)


test_agg <- aggr(test,sortVars=TRUE)
# Variable       Count
# PoolQC 0.997943797
# MiscFeature 0.965044551
# Alley 0.926662097
# Fence 0.801233722
# FireplaceQu 0.500342700

test$PoolQC <- NULL
test$MiscFeature <- NULL
test$Alley <- NULL
test$Fence <- NULL

write.csv(data, submission.csv)






