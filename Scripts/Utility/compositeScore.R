library(dplyr)
# The functions char2Num, char2Nums and normalize can be accessed from ActivityInfluence.R
source('ActivityInfluence.R')

# Takes in a Data Frame which must have the following 4 features (in any order)
# 1) IM_INFERRED_EDUCATION_LEVEL_NUM, 2) IM_INFERRED_SALARY_LEVEL_NUM
# 3) IM_TOTAL_EXP_MONTHS_NUM, 4) IM_LI_SIZE_LEVEL_NUM
# Similar to Activity & Influence Scores, the numbers are relative
# With min 0, max 1, mean & median ~ 0.5
compositeScore <- function(x) {
  features <- c('IM_INFERRED_EDUCATION_LEVEL_NUM', 'IM_INFERRED_SALARY_LEVEL_NUM',
                'IM_TOTAL_EXP_MONTHS_NUM', 'IM_LI_SIZE_LEVEL_NUM')
  if(!(all(features %in% names(x)))) {
    stop(paste('Input data is missing one of the 4 variables required for Composite Score:',
               paste(features, rep(';', length(features)))))
  }
  compositeDF <- select(x, IM_INFERRED_EDUCATION_LEVEL_NUM, IM_INFERRED_SALARY_LEVEL_NUM, 
                        IM_TOTAL_EXP_MONTHS_NUM, IM_LI_SIZE_LEVEL_NUM)
  numComp <- sapply(compositeDF, char2Nums)
  numCompDF <- as.data.frame(numComp)
  normComp <- sapply(numCompDF, normalize)
  scores = rowSums(matrix(normComp, nrow = nrow(numComp), ncol = ncol(numComp)), na.rm = TRUE)
  relScores = (nrow(numComp) - rank(scores))/nrow(numComp)
  return(round(relScores, 2))  
}

# Takes in a Data Frame and calls compositeScore to return
# DF augmented with result, keeping with naming convention
addCompScore <- function(x) {
  scores <- compositeScore(x)
  newMat <- cbind(x, scores)
  names(newMat)[ncol(newMat)] <- 'IM_COMPOSITE_SENIORITY_SCORE_NUM'
  return(newMat)
}