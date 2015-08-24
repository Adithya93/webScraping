# Takes the name of a URL (usually localhost streaming custom HTML) and returns
# a data frame of LinkedIn Information
require(httr)
require(XML)
library(dplyr)
setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

makeFBDF <- function(x){
  myReq <- GET(x)
  myCont <- content(myReq)
  openXpath <- '//div/p[@id="'
  closeXpath <- '"]'
  
  fields <- c('Email', 'USERNAME', 'Gender', 'Location', 'Hometown', 'Friends', 'Married', 'Followers', 
              'Education', 'Schools', 'Job', 'Company', 'Graduation', 'Age', 'SchoolingYears',
              'Movies', 'Music', 'Sports', 'MainInterest', 'LastPostDate', 'DaysSinceLastPost')
  
  
  info <- sapply(fields, function(x){
    return(xpathSApply(myCont, paste(openXpath, x, closeXpath, sep = ""), xmlValue))
  })
  fbdf <- as.data.frame(info)
  fbdf <- select(fbdf, -USERNAME)  
}