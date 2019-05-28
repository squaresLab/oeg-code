library("partykit", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.5")

merged.nash.reparied.time <- read.csv("~/PycharmProjects/apt-code/merged.nash.reparied.time.csv", header=FALSE)
merged.nash.reparied <- read.csv("~/PycharmProjects/apt-code/merged.nash.reparied.csv")

data <- merged.nash.reparied

nash.merged <- read.csv("~/PycharmProjects/apt-code/interp_results/nash.merged.csv")
merged.nash <- read.csv("~/PycharmProjects/apt-code/interp_results/merged.nash.csv")

data <- merged.nash [sample(nrow(merged.nash ),100000),]

# transform the harsanyi form tactics to the SE convention
nashform <- data
data$`X11` <- nashform$`X11`+nashform$`X12`
data$`X12` <- nashform$`X21`+nashform$`X22`
data$`X21` <- nashform$`X11`+nashform$`X21`
data$`X22` <- nashform$`X12`+nashform$`X22`


out.stackelberg.0 <- read.csv("~/PycharmProjects/apt-code/interp_results/out.stackelberg.0.csv")
data <- out.stackelberg.0

data = rbind(data,out.stackelberg.0)

data<-merged.nash

data <- nash.merged

drops <- c("a.n1.","a.n2.","c.P.","equilibrium","p.3.","X3","d.3.")
drops <- c("a.n1.","a.n2.","c.P.","p.3.","X3","d.3.")
data_dropped <- data[ , !(names(data) %in% drops)]
# use for nash only
predictors <- data_dropped[,-c(19:34)]
# use for nash and stackel combined
predictors <- data_dropped[,-c(20:34)]

# 12 x 16
# attacker 1 uses TTP 1
a1ttp1 <- data_dropped["X11"] #+ data_dropped["X12"] # commment out for stackelberg case

frame <- predictors
frame["a1ttp1"] <- a1ttp1

tree <- ctree(a1ttp1 ~ ., data = frame, maxdepth=4)
plot(tree)

# defender gives up and passes
p <- data_dropped["p"]

frame <- predictors
frame["p"] <- p

tree <- ctree(p ~ ., data = frame, maxdepth=4)
plot(tree)

# defender waits
waits <- data_dropped["we1"] + data_dropped["we2"] + data_dropped["wp"]
frame <- predictors
frame["w"] <- waits

tree <- ctree(w ~ ., data = frame, maxdepth=4)
plot(tree)

# defender plays wp
wp <- data_dropped["wp"]

frame <- predictors
frame["wp"] <- wp

tree <- ctree(wp ~ ., data = frame, maxdepth=4)
plot(tree)

# defender blind evicts ttp1
evict <- data_dropped["e1"]
frame <- predictors
frame["E1"] <- evict

tree <- ctree(E1 ~ ., data = frame, maxdepth=4)
plot(tree,inner_panel=node_inner(tree,
                                                abbreviate = FALSE,            # short variable names
                                                pval = FALSE,                 # no p-values
                                                id = FALSE),
     terminal_panel=node_boxplot(tree, 
                                  fill = c("white"),            # make box white not grey
                                  id = FALSE))

# defender plays active measure
active <- data_dropped["ae1"] + data_dropped["ae2"] + data_dropped["ap"]
frame <- predictors
frame["a"] <- active

tree <- ctree(a ~ ., data = frame, maxdepth=4)
plot(tree)

names()

# example data$yr.above <- rowSums(data > 30)
data_dropped$rsums <- rowSums(data_dropped[,24:32] > 0)
