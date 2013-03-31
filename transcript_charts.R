#!/usr/bin/env Rscript

library(ggplot2)

  inputfile = paste0('output2.tsv')
  cat("reading from file", inputfile, "\n")
  frame <- read.table(inputfile, header=TRUE, sep="\t", quote="", comment.char="") # avoid catching "#" or "'"
  
  attach(frame)

  # Take the sum of tweets for each date
  aggdate <- aggregate(x=count, by=list(date), FUN = sum)
  names(aggdate) = c("date2", "tweetcount2")

  # Count the number of users (length) for each date
  agg_users_per_chat <- aggregate(x=username, by=list(date), FUN = length) 
  names(agg_users_per_chat) = c("date2", "usercount2")

  # Take the sum of tweets for each user
  agguser <- aggregate(x=count, by=list(username), FUN = sum)
  names(agguser) = c("username3", "tweetcount3")

  # Count the number of chats (length) for each user
  agg_chats_per_user <- aggregate(x=date, by=list(username), FUN = length) 
  names(agg_chats_per_user) = c("username3", "chatcount3")

  chatdata <- merge(aggdate, agg_users_per_chat)
  userdata <- merge(agguser, agg_chats_per_user)

  outputfile = 'geowebchat_over_time_chart.pdf'
  pdf(outputfile, 10, 7)   # Create a PDF of 10 inches wide by 7 inches tall


  # Non-ggplot style:
  # print(barplot(table(username, date), las=2))

  # ggplot guide here: http://learnr.wordpress.com/2009/03/17/ggplot2-barplots/

  # This creates a separate bar for each user... but that's too many colors to follow.
  # ggplot(frame, aes(x=date, y=count, fill=username)) + geom_bar(stat="identity")

  attach(chatdata)

  b <- ggplot(chatdata, aes(x=date2, y=tweetcount2, fill=usercount2)) 
  b <- b + labs(title = "#geowebchat participation over time")
  b <- b + labs(x = NULL, y = "number of tweets", fill = "number of\nparticipants")
  b <- b + geom_bar(stat="identity", aes(fill=usercount2)) 
  #b <- b + scale_fill_brewer(palette=3)
  b <- b + scale_y_continuous(minor_breaks = seq(0,300,20))

  new_theme <- theme_update(axis.text.x = element_text(angle = 90,
     hjust = 1), panel.grid.major = element_line(color = "grey80"),
     panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank(),
     panel.grid.minor.y = element_line( size=.1, color = "grey90"), panel.background = element_blank(),
     axis.ticks = element_blank())
     #axis.ticks = element_blank(), legend.position = "none")

  b

  dev.off()

  outputfile = 'geowebchat_over_time_scatter.pdf'
  pdf(outputfile, 10, 7)   # Create a PDF of 10 inches wide by 7 inches tall

  s <- ggplot(chatdata, aes(x=tweetcount2, y=usercount2))
  s <- s + labs(title = "#geowebchat participation over time")
  s <- s + labs(x = "number of tweets", y = "number of participants")
  s <- s + geom_point()

  new_theme <- theme_update(axis.text.x = element_text(angle = 90,
     hjust = 1), panel.grid.major = element_line(color = "grey80"),
     panel.grid.minor.x = element_line( size=.1, color = "grey90"), 
     panel.grid.minor.y = element_line( size=.1, color = "grey90"), 
     panel.background = element_blank(),
     axis.ticks = element_blank())

  s

  dev.off()

  outputfile = 'geowebchat_by_user_chart.pdf'
  pdf(outputfile, 10, 7)   # Create a PDF of 10 inches wide by 7 inches tall

  attach(userdata)

  b <- ggplot(userdata, aes(reorder(username3,-tweetcount3),tweetcount3, fill=chatcount3)) # The minus makes it a descending sort
  b <- b + labs(title = "#geowebchat participation by user")
  b <- b + labs(x = NULL, y = "number of tweets", fill = "number\nof chats")
  b <- b + geom_bar(stat = "identity", aes(fill=chatcount3))
  b <- b + scale_y_continuous(minor_breaks = seq(0,1000,50))

  new_theme <- theme_update(axis.text.x = element_text(angle = 90, size=6,
     hjust = 1), panel.grid.major = element_line(color = "grey80"),
     panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank(),
     panel.grid.minor.y = element_line( size=.1, color = "grey90"), panel.background = element_blank(),
     axis.ticks = element_blank())

  b

  dev.off()

  outputfile = 'geowebchat_by_user_scatter.pdf'
  pdf(outputfile, 10, 7)   # Create a PDF of 10 inches wide by 7 inches tall

  s <- ggplot(userdata, aes(x=tweetcount3, y=chatcount3))
  s <- s + labs(title = "#geowebchat participation by user")
  s <- s + labs(x = "number of tweets", y = "number of chats")
  s <- s + geom_point()

  new_theme <- theme_update(axis.text.x = element_text(angle = 90,
     hjust = 1), panel.grid.major = element_line(color = "grey80"),
     panel.grid.minor.x = element_line( size=.1, color = "grey90"), 
     panel.grid.minor.y = element_line( size=.1, color = "grey90"), 
     panel.background = element_blank(),
     axis.ticks = element_blank())

  s

  dev.off()




  # TODO: later, try the facet_grid chart


  detach(frame)