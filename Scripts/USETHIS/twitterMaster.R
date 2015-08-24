setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

## These two packages are required
library(twitteR)
library(dplyr)

## These 3 scripts I wrote are used in this script
source("makeTwitterDF.R") 
source("reformTwitter.R")
source("tryTimelines.R")

twitterMaster <- function(idfile, emailfile, tablefile){
  if(!file.exists(idfile) || !file.exists(emailfile)){
    message('Oops! That file does not exist in this directory! Check file name and relative path, then try again.')
    return(NA)
  }
  
  consKey <- '0EKA6pqgqrPoPzD88MWgkvHkL'
  consSecret <- 'FKKanIwGEJW8GT1H991Nh7DszTv1LcMyPJIVJwneNrxCrJW7sR'
  appToken <- '1728231343-WeyZrPzK5H9hAwNYaYalGmS80UfGSy8Yx292tkO'
  appSecret <- 'SKBHwGPZBzy9zgGsA6Jvm1uowPQBFh1n6WGM7S9Z8W933'
  setup_twitter_oauth(consKey, consSecret, appToken, appSecret)
  allEmails <- read.csv(emailfile, header = FALSE)
  charEmails <- allEmails$V1
  names(charEmails)[1] <- 'Email'
  allIDS <- read.csv(idfile, header = FALSE)
  numIDs <- allIDS$V1
  emailIDs <- data.frame('ID' = numIDs, 'Email' = charEmails)
  myDF <- twitterInfo(numIDs)
  niceDF <- reformTwitter(myDF)
  myTimelines <- getTimelines(numIDs)
  coolDF <- mutate(niceDF, ID = id, LastTweetDate = created)
  #print(names(coolDF))
  coolerDF <- coolDF[,c(11, 2:10, 1,12)]
  #print(names(coolerDF))
  # In case screen names are being used instead of ID
  coolerDF$ID <- emailIDs$ID
  emailIDsInfo <- merge(emailIDs, coolerDF)
  #emailIDsInfo <- inner_join(emailIDs, coolerDF)
  TwitterDF <- merge(emailIDsInfo, myTimelines)
  TwitterDF <- select(TwitterDF, -c(screenName, created, id, ID))
  TwitterDF$LastTweetDate <- as.character(TwitterDF$LastTweetDate)
  write.csv(as.matrix(TwitterDF), tablefile)
  return(TwitterDF)
}