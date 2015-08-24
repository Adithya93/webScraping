source('joinSocMeds.R')
source('reformatDF.R')
source('saveGeoCodes.R')
source('numProfs.R')
source('inferEduSal.R')
source('guessExpAge.R')
source('ActivityInfluence.R')
source('compositeScore.R')
source('chooseFeatures.R')

# Makes all joins and imputations based on the 4 input DFs and a chosen place (client location)
getAll <- function(LI, TW, FB, COMP, place = 'Singapore') {
  allDF <- joinSocMeds(LI, TW, FB, COMP)
  refactoredDF <- refactorDF(allDF)[[1]]
  withDists <- addDists(refactoredDF, place)
  withProfs <- addNumProfs(withDists)
  withEduSal <- gaugePotential(withProfs)
  withExp <- getExps(withEduSal)
  withAge <- getAges(withExp)
  withActInf <- addScores(withAge)
  withCompScore <- addCompScore(withActInf)
  finalDF <- addChosen(withCompScore)
  finalDF <- finalDF[,c(2,1,(3:ncol(finalDF)))]
  
  return(finalDF)
}