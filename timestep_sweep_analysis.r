library(readr)
library("ggplot2", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.4")

prelim <- read_csv("~/research/saso2018-paper/prelim.csv", col_names = FALSE)
prelim <- read_csv("PycharmProjects/apt-code/timestep_sweep_fse.csv")
attach(prelim)
agg <- aggregate(prelim, by=list(timesteps,equilibrium), FUN=median)  

g<- ggplot(agg, aes(x=timesteps, y=time, group=equilibrium)) + geom_line(aes(linetype=equilibrium)) 
  #geom_point(aes(shape=X2))

g <- g + theme_bw() + xlab("Number of Timesteps") + ylab("Time in Seconds") + labs(linetype="Game Type")
g <- g + theme(legend.position=c(0.5,0.5), legend.text = element_text(size=12), legend.title=element_text(size=12), text=element_text(size=12))
g
