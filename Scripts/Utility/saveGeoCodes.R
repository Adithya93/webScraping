library(ggmap)
library(Imap)

# Takes a single string and returns a 1 by 2 numeric matrix of 
# the location's longitude and latitude
getGeocode <- function(x){
  result <- tryCatch(
    {
      geoVals <- geocode(x)
      matrix(c(geoVals$lon, geoVals$lat), nrow = 1, ncol = 2)
    },
    error = function(e){
      warning(paste('Problem calling geocode on ', x))
      print(e)
      return(matrix(c(NA, NA), nrow = 1, ncol = 2))
    },
    finally = {}
  )
  #return(matrix(c(geoVals$lon, geoVals$lat), nrow = 1, ncol = 2))
  return(result)
}


# Takes in a character vector of unique locations and returns a data frame
# representing database of longtitude and latitude information for each
# unique location in dataset
# Caching strategy to avoid need for REPEATED use Google Maps/Bing APIs 
# which have daily query limits of 2500 & 25 000
getGeocodes <- function(x){
  locNames <- x
  geoMat <- t(sapply(locNames, function(x){getGeocode(x)}))
  locsDF <- data.frame('Location' = locNames, 'Longtitude' = geoMat[,1], 'Latitude' = geoMat[,2])
  row.names(locsDF) <- 1:nrow(locsDF)
  return(locsDF)
}

# Calculates distance of all locations from source location
# Using geocodes obtained above and the geocode of source location
# parameter x is character vector of locations
# parameter y is target location
# Returns Data Frame with 2 columns : Location & Distance
getDists <- function(x, y) {
  targetGeo <- getGeocode(y)
  if(any(is.na(targetGeo))) {
    stop('Unable to determine geocode for target location. Try different location string.')
  }
  targetLong <- targetGeo[1]
  targetLat <- targetGeo[2]
  geoDF <- getGeocodes(x)
  longs <- geoDF$Longtitude
  lats <- geoDF$Latitude
  dists <- sapply(1:length(longs), function(x){
    gdist(longs[x],lats[x],targetLong,targetLat, units = 'km')
  })
  colName <- paste('DISTANCE_FROM_', y, 'NUM', sep = '')
  return(data.frame('LOCATION' = x, colName = dists))
}

# Calls above function on a DF to return DF augmented with distance data
addDists <- function(x, y) {
  if(!('LI_LOCATION' %in% names(x))) {
    stop('Input does not contain LinkedIn location data. Check if column name is
         "LI_LOCATION"')
  }
  charLocs <- as.character(x$LI_LOCATION)
  dists <- getDists(charLocs, y)[,2]
  newMat <- cbind(x, dists)
  names(newMat)[ncol(newMat)] <- paste('IM_DISTANCE_FROM_', y, '_NUM', sep ='')
  # For ease of reference
  LOC_COL <- (1 : ncol(newMat))[names(newMat) == 'LI_LOCATION']
  newMat <- newMat[,c((1 : LOC_COL), ncol(newMat), ((LOC_COL + 1) : (ncol(newMat) - 1)))]
}