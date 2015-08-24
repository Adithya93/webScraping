# Takes the name of a URL (usually localhost streaming custom HTML) and returns
# a data frame of LinkedIn Information
require(httr)
require(XML)
setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

makeRappDF <- function(x){
  myReq <- GET(x)
  myCont <- content(myReq)
  openXpath <- '//div/p[@id="'
  closeXpath <- '"]'
  
  fields <- c('Name', 'Location', 'Email', 'Headline', 'Jobs',
              'Companies', 'LinkedInProfile', 'Otherlinks')
  info <- sapply(fields, function(x){
    return(xpathSApply(myCont, paste(openXpath, x, closeXpath, sep = ""), xmlValue))
  })
  return(as.data.frame(info))  
}