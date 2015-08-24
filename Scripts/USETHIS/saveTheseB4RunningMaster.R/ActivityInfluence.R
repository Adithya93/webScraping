
# Converts character or factor with blanks and 'Unknown' values into numeric vector 
# where 'Unknown' is turned into NAs
char2Num <- function(x) {
  if(is.na(x) || as.character(x) == 'Unknown' || nchar(as.character(x)) == 0) {
    return(NA)
  }
  else {
    return(as.numeric(x))
  }
}

# Vector-friendly version of above function
char2Nums <- function(x) {
  return(sapply(x, char2Num))
}

# Takes a numeric vector and returns the normalized version
normalize <- function(x) {
  theMean = mean(x, na.rm = TRUE)
  theSD = sd(x, na.rm=TRUE)
  return((x - theMean)/theSD)
}

# Takes DF with info about activities, cleans identified vectors using char2Num, normalizes it
# and returns 0 to 1 relative score of such vectors for each person
# Most Active person gets (almost) 1, Least Active person gets 0 
activityScore <- function(x) {
  activities <- c('TW_statusesCount_NUM', 'TW_favoritesCount_NUM', 'FB_DaysSinceLastPost_NUM') 
  if(!all(activities %in% names(x))) {
    stop(paste('Missing one of the activity fields in Data Frame. Ensure that', 
               paste(activities, rep(',', length(activities)), sep = ''), 'are in Data Frame'))
  }
  activitiesDF <- select(x, TW_statusesCount_NUM, TW_favoritesCount_NUM, FB_DaysSinceLastPost_NUM)
  numAct <- sapply(activitiesDF, char2Nums)  
  # Negate days since last post 
  numActDF <- as.data.frame(numAct)
  numActDF$FB_DaysSinceLastPost_NUM <- - numActDF$FB_DaysSinceLastPost_NUM 
  #View(numActDF$DaysSinceLastPost)
  normAct <- sapply(numActDF, normalize)
  scores = rowSums(matrix(normAct, nrow = nrow(numAct), ncol = ncol(numAct)), na.rm = TRUE)
  relScores = (nrow(numAct) - rank(scores))/nrow(numAct)
  return(round(relScores, 2))
}

# Same as above, but for Influence instead of Activity
influenceScore <- function(x) {
  #infs <- c('LI_CONNECTIONS_NUM', 'TW_Retweets_NUM', 'IM_INFERRED_SALARY_LEVEL_NUM',
  #          'LI_COMPANY_FOLLOWERS_NUM', 'TW_followersCount_NUM', 'TW_friendsCount_NUM', 
  #          'FB_Friends_NUM', 'TW_listedCount_NUM')
  infs <- c('LI_CONNECTIONS_NUM', 'TW_Retweets_NUM', 'IM_INFERRED_SALARY_LEVEL_NUM',
            'TW_followersCount_NUM', 'TW_friendsCount_NUM', 
            'FB_Friends_NUM', 'TW_listedCount_NUM')
  
  
  if(!all(infs %in% names(x))) {
    stop(paste('Missing one of the interest fields in Data Frame. Ensure that', 
               paste(infs, rep(',', length(infs)), sep = ''), 'are in Data Frame'))
  }
  #infsDF <- select(x, LI_CONNECTIONS_NUM, TW_Retweets_NUM, IM_INFERRED_SALARY_LEVEL_NUM,
  #                 LI_COMPANY_FOLLOWERS_NUM, TW_followersCount_NUM, TW_friendsCount_NUM, 
  #                 FB_Friends_NUM, TW_listedCount_NUM)
  infsDF <- select(x, LI_CONNECTIONS_NUM, TW_Retweets_NUM, IM_INFERRED_SALARY_LEVEL_NUM,
                                    TW_followersCount_NUM, TW_friendsCount_NUM, 
                                    FB_Friends_NUM, TW_listedCount_NUM)
  
  
  numInf <- sapply(infsDF, char2Nums)  
  normInf <- sapply(as.data.frame(numInf), normalize)
  scores = rowSums(matrix(normInf, nrow = nrow(numInf), ncol = ncol(numInf)), na.rm = TRUE)
  relScores = (nrow(numInf) - rank(scores))/nrow(numInf)
  return(round(relScores, 2))
}

# Takes in DF and returns DF augmented with Activity Score & Influence Score vectors
addScores <- function(x) {
  actScores <- activityScore(x)
  infScores <- influenceScore(x)
  newMat <- cbind(x, actScores, infScores)
  names(newMat)[(ncol(newMat) - 1) : ncol(newMat)] <- c('IM_ACTIVITY_SCORE','IM_INFLUENCE_SCORE')
  return(newMat)
}