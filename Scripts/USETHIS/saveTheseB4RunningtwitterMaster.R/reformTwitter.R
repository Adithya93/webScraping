## Takes in a DF of twitter user objects and returns a formatted data frame
reformTwitter <- function(x){  
  #userMat <- as.data.frame(myUsers[[1]])
  myMat <- mutate(x, Name = name)
  goodMat <- select(myMat, -c(followRequestSent, profileImageUrl, name))
  myvect <- c(12, 14,1,10, 2,3,4,5,6,7,8,9,11,13)
  ordMat <- goodMat[myvect]
  finalMat <- select(ordMat, -c(protected, verified, url, lang))
  return(finalMat)
}
