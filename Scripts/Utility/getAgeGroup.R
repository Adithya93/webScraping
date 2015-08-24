
# Takes in a numeric vector of ages between 21 and 70
# Returns Age Level between 1 to 3
# 1: 21 - 30, 2: 31 - 50, 3: 51-70
getAgeGroup <- function(x){
  young <- c(21 : 30)
  medium <- c(31 : 50)
  old <- c(51 : 70)
  ageGroups <- list(young, medium, old)
  return((x %in% young) * 1 + (x %in% medium) * 2 + (x %in% old) * 3)  
}