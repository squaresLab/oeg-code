library(readr)
library(reshape)
library(ggplot2)

nashsweep <- read_csv("PycharmProjects/apt/nashsweep.csv")

bothsweep <- read_csv("~/PycharmProjects/apt-code/bothsweep.csv")

sweep <- bothsweep

sweeps <- subset(sweep,equilibrium == "nash")
title <- "Nash"

sweeps <- subset(sweep,equilibrium != "nash")
title <- "Stackelberg"

sweeps <- as.data.frame(sweeps)

mdata <- melt(sweeps,id=c("t1_prior","payoff","equilibrium"))
ggplot(mdata, aes(variable,t1_prior, fill = value)) + geom_raster() + ggtitle(title)

attacker = subset(mdata,variable %in% c("11","12","21","22"))
defender = subset(mdata,!variable %in% c("11","12","21","22"))
ggplot(attacker, aes(variable,t1_prior, fill = value)) + geom_raster() + ggtitle(title)
ggplot(defender, aes(variable,t1_prior, fill = value)) + geom_raster() + ggtitle(title)

(p <- ggplot(mdata, aes(variable, t1_prior)) + geom_tile(aes(fill = value), colour = "white") + scale_fill_gradient(low = "white",high = "steelblue") + ggtitle(title))
