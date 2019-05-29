library(readr)

postprocnash <- read_csv("PycharmProjects/apt-code/postprocnash.csv")
postprocstackelberg <- read_csv("PycharmProjects/apt-code/postprocstackelberg.csv")

postprocnash <- postprocnash[1:200000,]
postprocstackelberg <- postprocstackelberg[1:200000,]

# transform the harsanyi form tactics to the SE convention
nashform <- postprocnash
data <- nashform
data$`11` <- nashform$`11`+nashform$`12`
data$`12` <- nashform$`21`+nashform$`22`
data$`21` <- nashform$`11`+nashform$`21`
data$`22` <- nashform$`12`+nashform$`22`

data = rbind(data,postprocstackelberg)