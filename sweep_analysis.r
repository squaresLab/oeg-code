library(readr)
library(reshape2)
library(ggplot2)

nashsweep <- read_csv("PycharmProjects/apt/nashsweep.csv")

bothsweep <- read_csv("~/PycharmProjects/apt/bothsweep.csv")

sweep <- bothsweep

sweeps <- subset(sweep,equilibrium == "nash")
title <- "Nash Equilibrium"

sweeps <- subset(sweep,equilibrium != "nash")
title <- "Stackelberg Equilibrium"

sweeps <- as.data.frame(sweeps)

mdata <- melt(sweeps,id=c("t1_prior","payoff","equilibrium"))
ggplot(mdata, aes(variable,t1_prior, fill = value)) + geom_raster() + ggtitle(title)

attacker = subset(mdata,variable %in% c("11","12","21","22"))
defender = subset(mdata,!variable %in% c("11","12","21","22"))
ggplot(attacker, aes(variable,t1_prior, fill = value)) + geom_raster() +  xlab("Attacker's Action") + ylab("Prior Probability of Attacker Type 1") + labs(fill='Action \nProbability') 
ggplot(defender, aes(variable,t1_prior, fill = value)) + geom_raster() + xlab("Defender's Action") + ylab("Prior Probability of Attacker Type 1") + labs(fill='Action \nProbability')

(p <- ggplot(mdata, aes(variable, t1_prior)) + geom_tile(aes(fill = value), colour = "white") + scale_fill_gradient(low = "white",high = "steelblue") + ggtitle(title))
