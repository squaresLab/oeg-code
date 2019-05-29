library(readr)
library("partykit", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.6")

postprocnash <- read_csv("PycharmProjects/apt-code/postprocnash.csv")
postprocstackelberg <- read_csv("PycharmProjects/apt-code/postprocstackelberg.csv")

postprocnash <- postprocnash[1:2000000,]
postprocstackelberg <- postprocstackelberg[1:2000000,]

# transform the harsanyi form tactics to the SE convention
nashform <- postprocnash
data <- nashform
data$`11` <- nashform$`11`+nashform$`12`
data$`12` <- nashform$`21`+nashform$`22`
data$`21` <- nashform$`11`+nashform$`21`
data$`22` <- nashform$`12`+nashform$`22`

data = rbind(data,postprocstackelberg)

data$equilibrium <- as.factor(data$equilibrium)

data$`11` <- round(data$`11`,digits=5)
data$`12` <- round(data$`12`,digits=5)
data$`21` <- round(data$`21`,digits=5)
data$`22` <- round(data$`22`,digits=5)

data <- subset(data, data$`11` <= 1)
data <- subset(data, data$`12` <= 1)
data <- subset(data, data$`21` <= 1)
data <- subset(data, data$`22` <= 1)

data <- subset(data, data$`11` >= 0)
data <- subset(data, data$`12` >= 0)
data <- subset(data, data$`21` >= 0)
data <- subset(data, data$`22` >= 0)

drops <- c("a(n1)","a(n2)","c(P)","p(3)","3","d(3)")
data_dropped <- data[ , !(names(data) %in% drops)]

predictors <- data_dropped[,-c(21:29)]

# 12 x 16
# 8 x 19
# attacker 1 uses TTP 1
a1ttp1 <- data_dropped["11"] #+ data_dropped["X12"] # commment out for stackelberg case

frame <- predictors
frame["a1ttp1"] <- a1ttp1

tree <- ctree(a1ttp1 ~ ., data = frame, maxdepth=4)
plot(tree)
