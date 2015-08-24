## Functions to visualize the completeness of observations on micro and macro levels

source('reformatDF.R')

# Plots graph of completeness of observations to facilitate choice of cut-off threshold
howBad <- function(vals, threshold=0.5){
  return(sum(vals$Completeness > threshold)/nrow(vals))
}

plotCompleteness <- function(data, threshVect, imgName){  
  myData <- data
  if(!('Completeness' %in% names(myData))){
    myData$Completeness <- rowComp(myData)
  }
  sigh <- sapply(threshVect, function(x){howBad(myData, x)})
  #if(substring(imgName, nchar(imgName) - nchar('.jpeg'), nchar(substring)) != '.jpeg'){
  #  stop('Image format must be JPEG')
  #}
  if(class(imgName) != 'character'){
    stop(paste('Image name must be of type character, not ', class(imgName)))
  }
  jpeg(imgName)
  plot(threshVect, sigh, xlab = 'Completeness Threshold', ylab = 'Pass Ratio', main = 'Completeness')
  dev.off()
  return(matrix(c(threshVect,sigh), nrow = length(sigh), ncol = 2))
}