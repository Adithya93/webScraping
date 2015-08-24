## Takes in a list of twLists (each twList is a list of tweets by a person) and returns a nice list of DFs
getTweets <- function(x){
    vals <- sapply(x, function(y){
    thisguysposts <- c()
    if(length(y) > 0){
      thisguysposts <- twListToDF(y)  
    }
    else{
      return('No posts found for this guy')
    }
    return(thisguysposts)
    })
  return(vals)  
}
  
