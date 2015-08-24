library(stringr)
# Call these functions AFTER calling those in inferEduSal.R, as the guessAge function depends
# partly on the INFERRED_EDUCATION_LEVEL_NUM feature


# Takes in string representing Job Dates
# Returns numeric vector representing total months of experience
# Based on assumption that job durations in LinkedIn have format of 
# (x years, y months) or (x years)
guessExp <- function(x) {
  patterns <- c('\\(\\d+\\s\\S+\\s\\d\\s\\S+\\)', '\\(\\d+\\s\\S+\\)')
  hisPeriods <- str_match_all(x, patterns)
  mixed <- hisPeriods[[1]]
  pureYears <- hisPeriods[[2]]
  sumYears <- sum(as.numeric(str_match(mixed, '\\d'))) + sum(as.numeric(str_match(pureYears, '\\d')))
  sumMonths <- sum(as.numeric(str_match(mixed, '\\s\\d')))
  return(sumYears * 12 + sumMonths)
}

# Character-vector-friendly version of above function
guessExps <- function(x) {
  return(sapply(x,guessExp))
}

# Function that takes in DataFrame with LI_JOBDATES column
# and returns matrix augmented with numeric column for total months of experience 
getExps <- function(x) {
  if(!('LI_JOBDATES') %in% names(x)) {
    stop('Input has no data on LinkedIn Job Dates')
  }
  IM_TOTAL_EXP_MONTHS_NUM <- guessExps(x$LI_JOBDATES)
  newMat <- cbind(x, IM_TOTAL_EXP_MONTHS_NUM)
  # For ease of reference
  colNum <- (1:ncol(newMat))[names(newMat) == 'LI_JOBDATES']
  newMat <- newMat[,c(1:colNum, ncol(newMat), (colNum + 1) : (ncol(newMat) - 1))]
  return(newMat)
}

## Determine Age using available information for each person
# in order of priority: FB Age > FB Graduation Year > LI_EXPERIENCE (from guessExp)
# Otherwise, NA
# Returns n by 2 DF with cols 1) guessed Age and 2) Confidence Level
# Confidence Levels:
# 0 : NA, 1 : Guessed with Exp, 2 : Guessed with Grad, 3 : Direct Age from FB
guessAge <- function(x) {
  fbAge <- as.character(x$FB_Age_NUM)
  if(!is.na(fbAge) & fbAge != 'Unknown') {
    return(c(as.numeric(fbAge), 3))
  }
  
  if(x$IM_EDUCATION_LEVEL_NUM == 3){
    GRAD_AGE <- 26
  }
  else {
    GRAD_AGE <- 23
  }
  
  fbGrad <- as.character(x$FB_Graduation)
  liGrad <- as.character(x$LI_GRADUATIONYEAR)
  
  chosen <- NA
  
  if (!is.na(liGrad) & liGrad != 'Unknown') {
    chosen <- liGrad
  }
  
  else if (!is.na(fbGrad) & fbGrad != 'Unknown') {
    chosen <- fbGrad
  }
  
  if (!is.na(chosen)) {
    gradYear <- as.numeric(chosen)
    yearsFromGrad <- as.numeric(substring(Sys.Date(),1,4)) - gradYear
    return(c(GRAD_AGE + yearsFromGrad, 2))  
  }
  
  if(!('IM_TOTAL_EXP_MONTHS_NUM' %in% names(x))) {
    expMonths <- guessExp(x$LI_JOBDATES)
  }
  else {
    expMonths <- x$IM_TOTAL_EXP_MONTHS_NUM    
  }
  if(!is.na(expMonths) & expMonths != 0) {
    return(c(round(expMonths/12) + GRAD_AGE, 1))
  }
  else {
    return(c(NA, 0))
  }
}

# Data-Frame-friendly version of above function
guessAges <- function(x) {
  ageData <- t(sapply(1:nrow(x), function(y) {
    return(guessAge(x[y,]))
  }))
  ageDF <- as.data.frame(ageData)
  names(ageDF) <- c('IM_PREDICTED_AGE_NUM', 'IM_AGE_CONFIDENCE_NUM')
  return(ageDF)
}

# Function that takes in DataFrame with LI_JOBDATES column
# and returns matrix augmented with numeric column for total months of experience 
getAges <- function(x) {
  if(!('LI_JOBDATES' %in% names(x))) {
    error('Input has no information about Job Dates')
  }
  newMat <- cbind(x,guessAges(x))
  # For ease of reference
  DATES_COL <- (1:ncol(newMat))[names(newMat) == 'IM_TOTAL_EXP_MONTHS_NUM']
  newMat <- newMat[,c((1 : DATES_COL), ((ncol(newMat) - 1) : ncol(newMat)), 
                      ((DATES_COL + 1) : (ncol(newMat) - 2)))]
}