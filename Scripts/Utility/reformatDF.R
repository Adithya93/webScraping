## Script to be run on raw joint DF obtained from left join of LI, Twitter & FB Info

# Function that scores the completeness of each variable (column)
completeness <- function(x, total){
  return(sum((!is.na(x)) & (x != 'Unknown') & (nchar(as.character(x)) > 0))/total)
}

# Function that scores the completeness of each observation (row)
rowComp <- function(x){
  rowScores <- c()
  for(row in 1 : nrow(x)){
    rowScore <- completeness(x[row,], ncol(x))
    rowScores <- c(rowScores, rowScore)
  }
  return(rowScores)
}

# Function that takes the joint DF (LinkedIn, Twitter & Facebook) and reformats it
refactorDF<- function(jointDF){
  #JointUnion <- jointDF
  #newUnion <- JointUnion[,-c(12, 13, 20, 24)]
  # The following 5 lines are unstable and will change depending on
  # addition of more features  
  newUnion <- jointDF
  
  names(newUnion)[2:17] <- paste(rep('LI_', 16), names(newUnion)[2:17], sep='')
  names(newUnion)[18:27] <- paste(rep('TW_', 10), names(newUnion)[18:27], sep='')
  names(newUnion)[28:length(names(newUnion))] <- paste(rep('FB_', 17), names(newUnion)[28:length(names(newUnion))], sep = '')
  numVect <- c(7, 15, 17, 21, 22, 23, 24, 25, 27, 31, 33, 39, 41, 42, 43)
  names(newUnion)[numVect] <- paste(names(newUnion)[numVect], rep('_NUM', length(numVect)), sep = '')
  
  compScore <- sapply(names(newUnion), function(x){completeness(newUnion[x], nrow(newUnion))})
  completenessScore <- data.frame(t(compScore))
  rowScores <- rowComp(newUnion)
  newUnion$Completeness <- rowScores
  newUnion <- newUnion[,c(ncol(newUnion), 1:ncol(newUnion)-1)]
  return(list(newUnion, completenessScore))
}