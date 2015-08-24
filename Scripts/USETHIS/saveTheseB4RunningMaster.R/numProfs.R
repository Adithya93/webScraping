## Augments Data Frame with a numeric variable representing number of social media profiles 
## found for each person

# Returns TRUE if column x represents data for social media platform with abbreviation y
# Helper method for functions below
# e.g. testMatch('LI_CONNECTIONS', 'LI') ==> TRUE, 
# testMatch('TW_location', 'FB') == > FALSE
testMatch <-  function(x, y){
  return(substring(x, 1, 2) == y)
}

# Splits column indices by whether they are from LI, TW or FB 
# Takes in the names of DF as input and returns list of length 3
splitProfs <- function(x){
  indices <- 1:length(x)
  socMeds <- c('LI', 'TW', 'FB')
  #return(data.frame('LI'=indices[sapply(x,function(k){testMatch(k,'LI')})]))
  return(sapply(socMeds, function(y){
    return(indices[sapply(x, function(z){testMatch(z,y)})])
  }))
}

# Takes Data Frame as input and returns vector of length equal to no.of rows of DF
# where each unit represents number of Social Media profiles found for that person
hasProfs <- function(x){
  profs <- splitProfs(names(x))
  scores <- sapply(1:nrow(x), function(y){
    return(sum(sapply(profs, function(z){
      return(any(!is.na(x[y,z])))
    })))
  })
}

# More detailed version of hasProfs, which returns an n by 3 matrix
# where each column represents total 
# appearances of that person for each social media platform
profScores <- function(x){
  profs <- splitProfs(names(x))  
  scores <- sapply(1:nrow(x), function(y){
    return(sapply(profs, function(z){
      val <- x[y,z]
      charVal <- as.character(val)
      return(sum((!is.na(val)) & (charVal != 'Unknown') & (nchar(charVal) > 1)))
    }))
  })
  return(as.data.frame(t(scores)))
}

# Calls hasProfs on Data Frame and returns DF augmented with the resulting vector
# as 3rd column
addNumProfs <- function(x){
  numProfs <- hasProfs(x)
  allScores <- profScores(x)
  added <- cbind(numProfs, allScores)
  names(added) <- c('IM_PROFS_NUM', 'IM_LI_NUM', 'IM_TW_NUM', 'IM_FB_NUM')  
  result <- cbind(x, added)
  order <- c(1:2, ((ncol(result) - 3) : ncol(result)), (3:(ncol(result) - 4)))
  result <- result[,order]
  return(result)
}