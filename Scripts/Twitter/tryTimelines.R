getTimelines <- function(x){
  myLines <-matrix(nrow = length(x), ncol = 1)
  reTweets <- c()
  for(i in 1:length(x)){
    hisTweets <- getTimeline(x[i])
    numReTweets <- 0
    hisText <- "No Tweets Found"    
    if(length(hisTweets) == 1){
      hisTweets <- list(hisTweets)
    }
    if(length(hisTweets) > 1){
      hisTweetDF <- twListToDF(hisTweets)
      numReTweets <- sum(hisTweetDF$retweetCount)
      hisText <- paste(hisTweetDF$text, collapse = "\n")      
    }
    reTweets <- c(reTweets, numReTweets)
    myLines[i] <- hisText      
  }
  timelineDF <- list(myLines, reTweets)
  result <- tryCatch(
  {
    timelineDF <- data.frame(ID = x, Latest_Tweets = myLines, Retweets = reTweets)
    timelineDF
  },
  error = function(e){
    message("There's a problem in creating the data frame, so I'll try to decode the funny characters :P")
    message(e)
    modified <- as.matrix(sapply(myLines, iconv))
    timelineDF <- data.frame(ID = x, Latest_Tweets = modified, Retweets = reTweets)    
    return(timelineDF)
  },
  finally = {}
    )
  #timelineDF <- data.frame(ID = x, Latest_Tweets = myLines, Retweets = reTweets)
  #return(timelineDF)
  return(result)
}
