library(readr)
library(reshape2)
library(ggplot2)
library(plyr)

sensitivity_sweep_fse <- read_csv("PycharmProjects/apt-code/sensitivity_sweep_fse.csv")
sensitivity_sweep_fse <- sensbackup
sweep <- as.data.frame(sensitivity_sweep_fse)

sweeps <- subset(sweep,sweep$na_prior==0.30)
sweeps <- sweeps[, !(names(sweeps) %in% c("na_prior","t2_prior"))]

sweeps$payoff = sweeps$payoff * -1
sweeps$uniform = sweeps$uniform * -1

sweeps <- subset(sweeps,equilibrium == "nash")
title <- "Nash Equilibrium"
# transform the harsanyi form tactics to the SE convention
nashform <- sweeps
sweeps$`11` <- nashform$`11`+nashform$`12`
sweeps$`12` <- nashform$`21`+nashform$`22`
sweeps$`21` <- nashform$`11`+nashform$`21`
sweeps$`22` <- nashform$`12`+nashform$`22`

sweeps <- subset(sweeps,equilibrium != "nash")
title <- "Stackelberg Equilibrium"

sweeps <- as.data.frame(sweeps)

utils = melt(sweeps,id=c("t1_prior","equilibrium"))
utils = subset(utils,variable %in% c("payoff","uniform"))

utils$variable <- revalue(utils$variable,c("payoff"="equilibrium","uniform"="uniform random"))

# 5 x 3
p <- ggplot(utils, aes(x=t1_prior,y=value,group=variable))
p <- p + geom_line(aes(linetype=variable)) + theme_bw() + ylab("Defender's Utility") + xlab("Prior Probability of Attacker Type 1") + scale_linetype_discrete(name="Defender Plays")
p + theme(legend.position=c(0.65,0.35), legend.text = element_text(size=14), legend.title=element_text(size=14), text=element_text(size=14)) + ggtitle(title) 


#,"decoys"
# 7 x 5
mdata <- melt(sweeps,id=c("t1_prior","payoff","equilibrium","uniform"))
p <- ggplot(mdata, aes(variable,t1_prior, fill = value)) + geom_raster() + ggtitle(title) 
p <- p + theme(legend.position=c(0.9,0.5), legend.text = element_text(size=16), legend.title=element_text(size=16), text=element_text(size=16))
p <- p + xlab("Action") + ylab("Prior Probability of Attacker Type 1") + scale_fill_continuous(name="Probability\nPlayed")
p

# start arch diff graphs
decoysweep <- read_csv("PycharmProjects/apt-code/decoy_sweep_fse.csv")
decoysweep$payoff = decoysweep$payoff * -1
decoysweep$uniform = decoysweep$uniform * -1

decoysweep$payoff = decoysweep$payoff - decoysweep$decoys * 0.03

# transform from nash to se action rep
# WARNING ONLY DO THIS BLOCK FOR SHOWING NE ACTION DELTA!
nashform <- decoysweep
decoysweep$`11` <- nashform$`11`+nashform$`12`
decoysweep$`12` <- nashform$`21`+nashform$`22`
decoysweep$`21` <- nashform$`11`+nashform$`21`
decoysweep$`22` <- nashform$`12`+nashform$`22`
# NE ACTION DELTA GRAPH PREPROCESSING 

v1 <- sweeps
bothsweep <- v1[(v1$t1_prior*1000)%%10==0,]

attacker = subset(mdata,variable %in% c("11","12","21","22"))
defender = subset(mdata,!variable %in% c("11","12","21","22"))
ggplot(attacker, aes(variable,t1_prior, fill = value)) + geom_raster() +  xlab("Attacker's Action") + ylab("Prior Probability of Attacker Type 1") + labs(fill='Action \nProbability') 
ggplot(defender, aes(variable,t1_prior, fill = value)) + geom_raster() + xlab("Defender's Action") + ylab("Prior Probability of Attacker Type 1") + labs(fill='Action \nProbability')

(p <- ggplot(mdata, aes(variable, t1_prior)) + geom_tile(aes(fill = value), colour = "white") + scale_fill_gradient(low = "white",high = "steelblue") + ggtitle(title))

diff = data.frame(bothsweep$t1_prior,bothsweep$equilibrium,decoysweep$decoys,decoysweep$payoff-bothsweep$payoff, decoysweep$`11`-bothsweep$`11`,decoysweep$`12`-bothsweep$`12`,decoysweep$`21`-bothsweep$`21`,decoysweep$`22`-bothsweep$`22`, decoysweep$ae1-bothsweep$ae1,decoysweep$ae2-bothsweep$ae2,decoysweep$ap-bothsweep$ap,decoysweep$we1-bothsweep$we1,decoysweep$we2-bothsweep$we2,decoysweep$wp-bothsweep$wp,decoysweep$e1-bothsweep$e1,decoysweep$`e2`-bothsweep$`e2`,decoysweep$`p`-bothsweep$`p`)

diff$bothsweep.equilibrium <- revalue(diff$bothsweep.equilibrium,c("nash"="Nash","stackelberg"="Stackelberg"))

# 6 x 4
p <- ggplot(diff, aes(x=bothsweep.t1_prior,y=decoysweep.payoff...bothsweep.payoff,group=bothsweep.equilibrium))
p <- p + geom_line(aes(linetype=bothsweep.equilibrium)) + theme_bw() + ylab("Delta Defender's Utility") + xlab("Prior Probability of Attacker Type 1") + scale_linetype_discrete(name="Equilibrium")
p <- p + theme(legend.position=c(0.7,0.3), legend.text = element_text(size=14), legend.title=element_text(size=14), text=element_text(size=14))
p

decoysweep$equilibrium <- revalue(decoysweep$equilibrium,c("nash"="Nash","stackelberg"="Stackelberg"))

p <- ggplot(decoysweep, aes(x=t1_prior,y=decoys,group=equilibrium))
p <- p + geom_line(aes(linetype=equilibrium)) + theme_bw() + ylab("Optimal Number of Decoys") + xlab("Prior Probability of Attacker Type 1") + scale_linetype_discrete(name="Equilibrium")
p <- p + theme(legend.position=c(0.7,0.5), legend.text = element_text(size=14), legend.title=element_text(size=14), text=element_text(size=14))
p

mdata <- melt(diff,id=c("bothsweep.t1_prior","decoysweep.payoff...bothsweep.payoff","bothsweep.equilibrium","decoysweep.decoys"))

mdata$variable <- revalue(mdata$variable,c("decoysweep..11....bothsweep..11."="11","decoysweep..12....bothsweep..12."="12","decoysweep.we1...bothsweep.we1"="we1","decoysweep..22....bothsweep..22."="22","decoysweep..21....bothsweep..21."="21","decoysweep.we2...bothsweep.we2"="we2","decoysweep.e1...bothsweep.e1"="e1","decoysweep.e2...bothsweep.e2"="e2","decoysweep.ae2...bothsweep.ae2"="ae2","decoysweep.ae1...bothsweep.ae1"="ae1","decoysweep.p...bothsweep.p"="p","decoysweep.wp...bothsweep.wp"="wp","decoysweep.ap...bothsweep.ap"="ap"))

p <-ggplot(subset(mdata,bothsweep.equilibrium=="nash"), aes(variable,bothsweep.t1_prior, fill = value)) + geom_raster() + ggtitle("Strategy Change with Optimal Design NE") + xlab("Action") + ylab("Prior Probability of Attacker Type 1") +  labs(fill='Delta\nAction \nProbability')
p + scale_fill_distiller(type="div", limits=c(-1,1), palette="PuOr", values = c(0.0,1.0))
p <- p + scale_fill_gradient2(high="#f1a340",low="#998ec3")
p <- p + theme(legend.position=c(0.5,0.5), legend.text = element_text(size=14), legend.title=element_text(size=14), text=element_text(size=14))
p
# new

p <-ggplot(subset(sweeps,sweeps.equilibrium=="nash"), aes(variable,bothsweep.t1_prior, fill = value)) + geom_raster() + ggtitle("Strategy Change with Optimal Design NE") + xlab("Action") + ylab("Prior Probability of Attacker Type 1") +  labs(fill='Delta\nAction \nProbability')
p + scale_fill_distiller(type="div", limits=c(-1,1), palette="PuOr", values = c(0.0,1.0))
p + scale_fill_gradient2(high="#f1a340",low="#998ec3")
