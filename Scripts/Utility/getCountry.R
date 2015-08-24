# Text parsing to determine country based on assumption that 
# country name appears last in location string, usually after commas (if any)
# Does not work for USA, since most US-based LI locations mention only city/state 
# and rarely mention USA/America
# Helper function that operates on 1 given location string
getCountry <- function(x) {
  if(is.na(x)) {
    return(NA)
  }
  else if(x == "") {
    return('Unknown')
  }
  else if(str_count(x, ',') == 0) {
    return(x)
  }
  else {
    return(sub('.*,\\s*', '', x))
  }
}

# Calls the above helper function with sapply to determine all countries
# Takes in DataFrame and returns vector of countries
getCountries <- function(x) {
  liLocations <- as.character(x$LI_LOCATION)
  countries <- sapply(liLocations, getCountry)
}

# Calls getCountries on input DF to return DF augmented with
# LI_COUNTRIES variable
addCountries <- function(x) {
  augmented <- x
  if('LI_COUNTRY' %in% names(x)) {
    warning('It appears that the input Data Frame already has a "Countries" variable')
  }
  countries <- getCountries(x)
  # Based on current formatting assumptions
  LI_LOC_COL <- (1:ncol(x))[names(x) == 'LI_LOCATION']
  augmented$IM_LI_COUNTRY <- countries
  augmented <- augmented[,c((1:(LI_LOC_COL)), ncol(augmented), 
                            (LI_LOC_COL + 1):(ncol(augmented)-1))]
}

# Returns a Data Frame of country distribution
# Takes an augmented Data Frame as input
countryDist <- function(x) {
  input <- x
  if(!('LI_COUNTRY' %in% names(input))) {
    warning('It appears that the input Data Frame does not have a "Countries" variable. 
  Adding one now.')
    input <- addCountries(input)
  }
  
  byCountries <- split(input, input$LI_COUNTRY, drop = TRUE)
  countryNums <- sapply(byCountries, nrow)
  mostCounts <- sort(countryNums, decreasing =TRUE)
  countriesDF <- data.frame('IM_COUNTRY' = names(mostCounts), 'IM_NUM_OCCURENCES' = mostCounts)
  row.names(countriesDF) <- 1:nrow(countriesDF)
  return(countriesDF)
}