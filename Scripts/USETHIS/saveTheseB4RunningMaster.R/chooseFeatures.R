
# Helper Function for all functions below
# Returns TRUE if number evaluates to valid character/numeric information
checkValid <- function(x) {
  if (!is.na(x) && x != 'Unknown') {
    return(TRUE)
  }
  else {
    return(FALSE)
  }
}

# Takes a row of DF and compares LinkedIn location with Twitter & FB locations to
# return chosen one
chooseLoc <- function(x) {
  charFB <- as.character(x$FB_Location)
  charLI <- as.character(x$LI_LOCATION)
  charTW <- as.character(x$TW_location)
  # As FB has a timestamp, its location has priority if last FB post was recent
  if (checkValid(x$FB_DaysSinceLastPost_NUM)) { 
  if (as.numeric(x$FB_DaysSinceLastPost_NUM) < 365) {
    if (checkValid(charFB)) {
      return(charFB)
    }
  }
}
  # This feature is yet to be processed
#  else if (x$TW_DaysSinceLastPost < 365) {
    if (checkValid(charTW)) {
      return(charTW)
    }
#  }
  
  else if (checkValid(charLI)) {
    return(charLI)
  }
  
  else {
    return(NA)
  }
}

# Vector-friendly version of above function
chooseLocs <- function(x) {
  if(!all(c('LI_LOCATION', 'TW_location', 'FB_Location') %in% names(x))) {
    stop('Missing one of the location fields. Ensure DF has LI_LOCATION, TW_location & FB_Location')
  }
  return(sapply(1:nrow(x), function(y) {
    return(chooseLoc(x[y,]))
  }))
}

# Chooses Education from LinkedIn & Facebook Education data
chooseEdu <- function(x) {
  charLI <- as.character(x$LI_EDUCATIONALINSTITUTION)
  charFB <- as.character(x$FB_Education)
  if(checkValid(charLI)) {
    return(charLI)
  }
  else if (checkValid(charFB)) {
    return(charFB)
  }
  else {
    return(NA)
  }
}

# Vector-friendly version of above function, takes in DF
chooseEdus <- function(x) {
  if(!all(c('LI_EDUCATIONALINSTITUTION', 'FB_Education') %in% names(x))) {
    stop('Missing one of the education fields. Ensure DF has LI_EDUCATIONALINSTITUTION, 
         & FB_Education')
  }
  return(sapply(1:nrow(x), function(y) {
    return(chooseEdu(x[y,]))
  }))
}

chooseGrad <- function(x) {
  charLI <- as.character(x$LI_GRADUATIONYEAR)
  charFB <- as.character(x$FB_Graduation)
  if(checkValid(charLI)) {
    return(charLI)
  }
  else if (checkValid(charFB)) {
    return(charFB)
  }
  else {
    return(NA)
  }
}

chooseGrads <- function(x) {
  if (!all(c('LI_GRADUATIONYEAR', 'FB_Graduation') %in% names(x))) {
    stop('Missing one of the graduation fields. Ensure DF has LI_GRADUATIONYEAR & FB_Graduation fields')
  }
  return(sapply(1:nrow(x), function(y) {
    return(chooseGrad(x[y,]))
  }))
}

chooseCols <- function(x) {
  chosenLocs <- chooseLocs(x)
  chosenGrads <- chooseGrads(x)
  chosenEdus <- chooseEdus(x)
  chosenDF <- data.frame('IM_CHOSEN_LOCATION' = chosenLocs, 
                         'IM_CHOSEN_GRADUATION_YEAR' = chosenGrads,
                         'IM_CHOSEN_EDUCATION' = chosenEdus)
  return(chosenDF)
}

addChosen <- function(x) {
  chosens <- chooseCols(x)
  newMat <- cbind(x, chosens)
}