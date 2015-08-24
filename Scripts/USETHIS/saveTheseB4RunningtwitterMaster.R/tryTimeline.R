## Take in a list of UserIDs, return a list of User Timelines
## (each timeline is a Twitter list)

getTimeline <- function(x){#}, y){
  #myLines <- c()
  
  #for(i in 1:length(x)){
    output <- tryCatch(
  {
    myans <- userTimeline(x)
    #print(myans)
    #myLines <- c(myLines, myans)
    #print(paste(" Value of item is ",  as.character(x)))
    #y <- c(y,myans)    
    myans
  },
  error = function(e){
  message("Oh no! There's a little problem...")
  message(e)
  #print(paste("Value of item is ",  as.character(x)))
  return(NA)
},
finally = {
  
}
    )
  }

