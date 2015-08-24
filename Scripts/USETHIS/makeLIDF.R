# Takes the name of a URL (usually localhost streaming custom HTML) and returns
# a data frame of LinkedIn Information
require(httr)
require(XML)
setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

makeLIDF <- function(x){
  myReq <- GET(x)
  myCont <- content(myReq)
  openXpath <- '//div/p[@id="'
  closeXpath <- '"]'
  
  fields <- c('EMAIL', 'FULLNAME', 'TITLE', 'LOCATION', 'INDUSTRY', 'CURRENTCOMPANY',
             'CONNECTIONS', 'PASTCOMPANIES', 'JOBTITLES', 'JOBDATES', 'EXPERIENCE', 'EDUCATIONLEVEL', 'EDUCATIONALINSTITUTION', 
             'GRADUATIONYEAR', 'SKILLS', 'GROUPS', 'GROUPNAMES', 'GROUPSIZES', 'ACTIVITIES')
  info <- sapply(fields, function(x){
    return(xpathSApply(myCont, paste(openXpath, x, closeXpath, sep = ""), xmlValue))
  })
  return(as.data.frame(info))  
}