# Takes the name of a URL (usually localhost streaming custom HTML) and returns
# a data frame of Company Information
require(httr)
require(XML)
require(stringr)
library(dplyr)
source('saveGeoCodes.R')
setwd("C:/Users/Adithya/Desktop/Summer '15/NEWCLEUS")

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
  return(as.data.frame(info))  
}


# Makes above company DF, extracts unnecessary info, , and 
# returns augmented version of input Data Frame
# Parameter x : Company DF from above
editCompDF <- function(x) {
  compDF <- select(x, Email, metrics_employees, metrics_alexaglobalrank,
                   metrics_googlerank, twitter_followers, facebook_likes,
                   geo_city, type, category_industry, description)
}

# Impute a rank for the company based on its numeric features
scoreCompany <- function(x) {
  
  
}

# Get Distance between company's location and target
companyDist <- function(x, y) {
  
  
}

# Does all the above, edits names
addComp <- function(x, y) {
  
  names(compDF)[2:ncol(compDF)] <- paste(rep('COMPANY_', ncol(compDF) - 1), names(compDF)[2:ncol(compDF)], sep = '')
}