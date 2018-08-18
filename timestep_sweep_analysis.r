library(readr)
library("ggplot2", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.4")

prelim <- read_csv("~/research/saso2018-paper/prelim.csv", col_names = FALSE)

g<- ggplot(prelim, aes(x=X1, y=X4, group=X2)) +
  geom_line(aes(linetype=X2)) 
  #geom_point(aes(shape=X2))
  
g + theme_bw() + xlab("Number of Timesteps") + ylab("Time in Secconds") + labs(linetype="Game Type")
