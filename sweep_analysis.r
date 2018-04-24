library(readr)
library(reshape2)
library(ggplot2)
library(plyr)

nashsweep <- read_csv("PycharmProjects/apt-code/nashsweep.csv")

bothsweep <- read_csv("~/PycharmProjects/apt-code/bothsweep.csv")
decoysweep <- read_csv("~/PycharmProjects/apt-code/decoysweep.csv")

sweep <- bothsweep

sweeps <- subset(sweep,equilibrium == "nash")
title <- "Nash Equilibrium"

sweeps <- subset(sweep,equilibrium != "nash")
title <- "Stackelberg Equilibrium"

sweeps <- as.data.frame(sweeps)

utils = melt(sweeps,id=c("t1_prior","equilibrium"))
utils = subset(utils,variable %in% c("payoff","uniform"))

utils$variable <- revalue(utils$variable,c("payoff"="equilibrium","uniform"="uniform random"))

p <- ggplot(utils, aes(x=t1_prior,y=value,group=variable))
p + geom_line(aes(linetype=variable)) + theme_bw() + ylab("Defender's Utility") + xlab("Prior Probability of Attacker Type 1")

mdata <- melt(sweeps,id=c("t1_prior","payoff","equilibrium","uniform","decoys"))
ggplot(mdata, aes(variable,t1_prior, fill = value)) + geom_raster() + ggtitle(title)

attacker = subset(mdata,variable %in% c("11","12","21","22"))
defender = subset(mdata,!variable %in% c("11","12","21","22"))
ggplot(attacker, aes(variable,t1_prior, fill = value)) + geom_raster() +  xlab("Attacker's Action") + ylab("Prior Probability of Attacker Type 1") + labs(fill='Action \nProbability') 
ggplot(defender, aes(variable,t1_prior, fill = value)) + geom_raster() + xlab("Defender's Action") + ylab("Prior Probability of Attacker Type 1") + labs(fill='Action \nProbability')

(p <- ggplot(mdata, aes(variable, t1_prior)) + geom_tile(aes(fill = value), colour = "white") + scale_fill_gradient(low = "white",high = "steelblue") + ggtitle(title))

diff = data.frame(bothsweep$t1_prior,bothsweep$equilibrium,decoysweep$decoys,decoysweep$payoff-bothsweep$payoff, decoysweep$`11`-bothsweep$`11`,decoysweep$`12`-bothsweep$`12`,decoysweep$`21`-bothsweep$`21`,decoysweep$`22`-bothsweep$`22`, decoysweep$we1-bothsweep$we1,decoysweep$we2-bothsweep$we2,decoysweep$e1-bothsweep$e1,decoysweep$`e2`-bothsweep$`e2`)

p <- ggplot(diff, aes(x=bothsweep.t1_prior,y=decoysweep.payoff...bothsweep.payoff,group=bothsweep.equilibrium))
p + geom_line(aes(linetype=bothsweep.equilibrium)) + theme_bw() + ylab("Delta Defender's Utility") + xlab("Prior Probability of Attacker Type 1") + scale_linetype_discrete(name="Equilibrium")

p <- ggplot(decoysweep, aes(x=t1_prior,y=decoys,group=equilibrium))
p + geom_line(aes(linetype=equilibrium)) + theme_bw() + ylab("Optimal Number of Decoys") + xlab("Prior Probability of Attacker Type 1") + scale_linetype_discrete(name="Equilibrium")

mdata <- melt(diff,id=c("bothsweep.t1_prior","decoysweep.payoff...bothsweep.payoff","bothsweep.equilibrium","decoysweep.decoys"))

mdata$variable <- revalue(mdata$variable,c("decoysweep..11....bothsweep..11."="11","decoysweep..12....bothsweep..12."="12","decoysweep.we1...bothsweep.we1"="we1","decoysweep..22....bothsweep..22."="22","decoysweep..21....bothsweep..21."="21","decoysweep.we2...bothsweep.we2"="we2","decoysweep.e1...bothsweep.e1"="e1","decoysweep.e2...bothsweep.e2"="e2"))

p <-ggplot(subset(mdata,bothsweep.equilibrium=="nash"), aes(variable,bothsweep.t1_prior, fill = value)) + geom_raster() + ggtitle("Strategy Change with Optimal Design NE") + xlab("Action") + ylab("Prior Probability of Attacker Type 1") +  labs(fill='Delta\nAction \nProbability')
p + scale_fill_distiller(type="div", limits=c(-1,1), palette="PuOr", values = c(0.0,1.0))
p + scale_fill_gradient2(high="#f1a340",low="#998ec3")
