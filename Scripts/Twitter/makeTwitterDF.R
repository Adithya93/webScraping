# Function takes in a numeric vector of IDs, extracted through Python scripts from FullContact and Clearbit APIs
twitterInfo <- function(x){
  myUsers <- lookupUsers(x)
  usersDF <- twListToDF(myUsers)
# Handle missing information from Twitter due to suspended IDs
  if(nrow(usersDF) != length(x)){
    warning('DataFrame obtained has missing rows! Trying to detect IDs without information')
    missingIDs <- x[!(x %in% usersDF$id)]
    print(missingIDs)
    filler <- matrix(nrow = length(missingIDs), ncol = ncol(usersDF))
    fillerDF <- as.data.frame(filler)
    names(fillerDF) <- names(usersDF)
    fillerDF$id <- missingIDs
    usersDF <- rbind(usersDF, fillerDF)
  }
  usersDF
}