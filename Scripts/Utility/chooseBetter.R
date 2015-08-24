## Following functions are applied (from bottom to top) on a joint DF to choose versions among duplicated emails 

# Choosing function applied to each column of data for repeated emails
chooseBetter <- function(x) {
  charX <- as.character(x)
  vals <- charX[!is.na(charX) & charX != 'Unknown']
  if (length(vals) == 0) {
    return(NA)
  }
  else if (length(vals) == 1) {
    return(vals)
  }
  else {
    return(charX[nchar(charX) == max(nchar(charX))][1])
  }
}

# Takes a list of (usually 2 row) DFs with repeated emails and returns a DF with unique emails
makeChoice <- function(x){
  if (class(x) != "list"){
    stop(paste('Input to makeChoice function must be a list. Given input is a ', class(x)))
  }
  chosenOnes <- sapply(x, function(y){sapply(y, function(z){chooseBetter(z)})})
  chosenOnesDF <- as.data.frame(t(chosenOnes))
  return(chosenOnesDF)
}

# Takes a joint DF (from joining PG and FC DFs) and returns list of DFs with duplicated emails
getDuplicates <- function(x){
  if(!'Email' %in% names(x)){
    stop('Input data frame to getDuplicates function must have a column called Email')
  }
  allMails <- x$Email
  uniqueMails <- unique(allMails)
  numOccurs <- sapply(uniqueMails, function(y){sum(allMails == y)})
  dupMails <- uniqueMails[numOccurs > 1]
  splitInfo <- split(x, x$Email %in% dupMails)
  pureInfo <- splitInfo[[1]]
  dupInfo <- splitInfo[[2]]
  dupSplit <- split(dupInfo, dupInfo$Email, drop = TRUE)
  return(list(pureInfo,dupSplit))
}

# Coordinates calls to all the above functions
purify <- function(x){
  splitVals <- getDuplicates(x)
  pureInfo <- splitVals[[1]]
  dupSplit <- splitVals[[2]]
  chosenDups <- makeChoice(dupSplit)
  finalDF <- rbind(pureInfo, chosenDups)
  return(finalDF)
}