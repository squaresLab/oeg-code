library(readr)
library(reshape)
library(ggplot2)

nashsweep <- read_csv("PycharmProjects/apt/nashsweep.csv")
mdata <- melt(nashsweep,id=c("t1_prior","payoff"))
ggplot(mdata, aes(variable,t1_prior, fill = value)) + geom_raster()

attacker = subset(mdata,variable %in% c("11","12","21","22"))
defender = subset(mdata,!variable %in% c("11","12","21","22"))
ggplot(attacker, aes(variable,t1_prior, fill = value)) + geom_raster()
ggplot(defender, aes(variable,t1_prior, fill = value)) + geom_raster()

(p <- ggplot(mdata, aes(variable, t1_prior)) + geom_tile(aes(fill = value), colour = "white") + scale_fill_gradient(low = "white",high = "steelblue"))
