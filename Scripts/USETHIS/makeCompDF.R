# Takes the name of a URL (usually localhost streaming custom HTML) and returns
# a data frame of Company Information
require(httr)
require(XML)
require(stringr)
library(dplyr)
source('saveGeoCodes.R')
source('ActivityInfluence.R')

#setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

# Accepts a URL hosting custom HTML document about LinkedIn Companies
# and returns Data Frame
makeCompDF <- function(x){
  myReq <- GET(x)
  myCont <- content(myReq)
  openXpath <- '//div/p[@id="'
  closeXpath <- '"]'
  
  fields <- c("Email", "url", "type", "facebook_handle", "facebook_likes", "geo_streetnumber", 
              "geo_subpremise", "geo_city", "geo_lng", "geo_lat", "geo_state", "geo_postalcode", 
              "geo_country", "geo_streetname", "location", "linkedin_handle", "emailprovider", 
              "metrics_alexausrank", "metrics_googlerank", "metrics_raised", "metrics_marketcap", 
              "metrics_alexaglobalrank", "metrics_employees", "crunchbase_handle", "description", 
              "tags", "ticker", "site_h1", "site_title", "site_url", "site_metaauthor", 
              "site_metadescription", "category_subindustry", "category_industrygroup", 
              "category_industry", "category_sector", "domain", "logo", "name", "angellist_handle", 
              "angellist_followers", "angellist_description", "angellist_id", "angellist_blogurl", 
              "tech", "domainaliases", "phone", "legalname", "twitter_handle", "twitter_followers", 
              "twitter_location", "twitter_site", "twitter_following", "twitter_avatar", "twitter_bio", 
              "twitter_id")  
  
  info <- sapply(fields, function(x){
    return(xpathSApply(myCont, paste(openXpath, x, closeXpath, sep = ""), xmlValue))
  })
  #return(as.data.frame(t(info)))
  return(as.data.frame(info))
}


# Makes above company DF, extracts unnecessary info, , and 
# returns augmented version of input Data Frame
# Parameter x : Company DF from above
editCompDF <- function(x) {
  compDF <- select(x, Email, metrics_employees, metrics_alexaglobalrank,
                   metrics_googlerank, twitter_followers, facebook_likes,
                   geo_city, type, category_industry, description)
  numVect <- c(2,3,4,5,6)
  numVars <- compDF[,numVect]
  realNums <- sapply(numVars, function(x){
    return(as.numeric(as.character(x)))
  })
  compDF[,numVect] <- realNums
  compDF$geo_city <- as.character(compDF$geo_city)
  return(compDF)
}

# Impute a rank for the company based on its numeric features
scoreCompany <- function(x) {
  myDF <- x
  numVect <- c(2,3,4,5,6)
  if(any(sapply(myDF[,numVect], class) != 'numeric')) {
    myDF <- editCompDF(x)    
  }
  numVars <- myDF[,numVect]
  numVars$metrics_alexaglobalrank <- - numVars$metrics_alexaglobalrank
  numVars$metrics_googlerank <- - numVars$metrics_googlerank
  normAct <- sapply(numVars, normalize)
  scores = rowSums(matrix(normAct, nrow = nrow(numVars), ncol = ncol(numVars)), na.rm = TRUE)
  relScores = (nrow(numVars) - rank(scores))/nrow(numVars)
  return(round(relScores, 2))
}

# Get Distance between companys' locations and target
companyDists <- function(x, y) {
  locs <- x$geo_city
  dists <- getDists(locs, y) 
  return(dists)
}


# Calls above function on a DF to return DF augmented with distance data
addCompDists <- function(x, y) {
  if(!('geo_city' %in% names(x))) {
    stop('Input does not contain Company "geo_city" location data. Check column name')
  }
  #charLocs <- as.character(x$LI_LOCATION)
  dists <- companyDists(x, y)[,2]
  newMat <- cbind(x, dists)
  names(newMat)[ncol(newMat)] <- paste('IM_DISTANCE_FROM_', y, '_NUM', sep ='')
  # For ease of reference
  LOC_COL <- (1 : ncol(newMat))[names(newMat) == 'geo_city']
  newMat <- newMat[,c((1 : LOC_COL), ncol(newMat), ((LOC_COL + 1) : (ncol(newMat) - 1)))]
}


# Does all the above, and edits names
# Param x : URL hosting Custom HTML
# Param y : Target Location of client (where you want to calculate distance from)
getComp <- function(x, y = 'Singapore') {
  compDF <- makeCompDF(x)
  editedDF <- editCompDF(compDF)
  scoredDF <- scoreCompany(editedDF)
  withDists <- addCompDists(editedDF, y)
  #goodComp <- cbind(editedDF, scoredDF, withDists)
  goodComp <- cbind(withDists, scoredDF)
  names(goodComp)[ncol(goodComp)] <- 'IM_SCORE'
  names(goodComp)[2:ncol(goodComp)] <- paste(rep('COMPANY_', ncol(goodComp) - 1), names(goodComp)[2:ncol(goodComp)], sep = '')
  return(goodComp)
}