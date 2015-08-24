# Takes the name of a URL (usually localhost streaming custom HTML) and returns
# a data frame of Company Information
require(httr)
require(XML)
require(stringr)
setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

# Accepts a URL hosting custom HTML document about LinkedIn Companies
# and returns Data Frame
makeCompDF <- function(x){
  myReq <- GET(x)
  myCont <- content(myReq)
  openXpath <- '//div/p[@id="'
  closeXpath <- '"]'
  
  fields <- c('Email', 'Name', 'Industry', 'Size', 'Followers')  
  
  info <- sapply(fields, function(x){
    return(xpathSApply(myCont, paste(openXpath, x, closeXpath, sep = ""), xmlValue))
  })
  return(as.data.frame(info))  
}

# Uses above method to augment existing Data Frame
# that has (at least) raw LI fields with Company information
# adds variable representing 1-8 numeric banding of company size
# where 1 --> 1 to 10 staff & 8 --> 10001+ staff
# also ensures names of company parameters adhere to DF's convention
# @param x: URL
# @param y: DataFrame
addCompInfo <- function(x, y) {
  compInfo <- makeCompDF(x)
  compSizes <- compInfo$Size
  levels(compSizes) <- c('1-10', '11-50', '51-200', '201-500', '501-1000', 
                         '1001-5000', '5001-10000', '10001')
  names(compInfo)[2:ncol(compInfo)] <- c('LI_COMPANY_NAME', 'LI_COMPANY_INDUSTRY', 
                                         'LI_COMPANY_SIZE', 'LI_COMPANY_FOLLOWERS_NUM')
  # Rearrange Company Size & No.of Followers so that numeric compSizes
  # is adjacent to its raw factor column
  compInfo <- compInfo[,c((1:3),5,4)]
  compInfo$IM_LI_COMPANY_SIZE_NUM <- as.numeric(compSizes)
  newMat <- left_join(y, compInfo)  
  # Place next to last LI column in DF y for reading convenience
  LICols <- (1:ncol(x))[substring(names(newMat), 1, 2) == 'LI']
  lastLICol <- max(LICols)
  #chosenCol <- lastLICol + 1
  numCols = ncol(compInfo)
  lastCol = ncol(newMat)
  newMat <- newMat[,c((1:lastLICol),((lastCol + 1 - numCols) : (lastCol)), 
                      ((lastLICol + 1) : (lastCol - numCols)))]
}