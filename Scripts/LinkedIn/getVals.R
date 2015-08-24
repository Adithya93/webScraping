# Takes an XML Internal Node and checks to see if it has certain features, adding the ones it has
getFeatures <- function(x, vals=c()){
  children <- xmlChildren(x)
  if(length(children) == 0){   
    return(as.character(xmlValue(x)))
  }
  xClass <- xmlGetAttr(x, 'class') 
  if(class(xClass) == 'character' && xClass != 'INFO'){
    if(xClass == 'links borders'){
      #return(paste('Link : ', xmlGetAttr(x, 'href')))
      return(as.character(xmlGetAttr(x, 'href')))
    }
    #return(paste(xClass, ': ', as.character(xmlValue(x))))
    return(as.character(xmlValue(x)))
  }
    
  vals <- c(vals, sapply(children, getFeatures))
  return(as.data.frame(t(vals)))
}

# Takes a list of people nodes
getAll <- function(x){
  Emails <- c()
  Names <- c()
  Info <- c()
  Links <- c()
  
  allInfo <- sapply(x, getFeatures)
  len <- length(allInfo)
  for(i in 1:len){
    current <- allInfo[[i]]
    Names <- c(Names, current[[1]])
    Emails <- c(Emails, current[[2]])
    if(length(current) > 2){
      Info <- c(Info, current[[3]])
      if(length(current) > 3){
        Links <- c(Links, current[[4]])
      }
      else{
        Links <- c(Links, "Not Found")
      }            
    }
    else{
      Info <- c(Info, "Not Found")
      Links <- c(Links, "Not Found")
 }

#    tryCatch(
#    {     
#    Info <- c(Info, allInfo[[i]][[3]])
#    Links <- c(Links, allInfo[[i]][[4]])
#    },
#    error = function(e){
#      Info <- c(Info, "Not Found")
#      Links <- c(Info, "Not Found")
#      message(paste(allInfo[[i]][[1]], " does not have information"))      
#    }
#    )
#  }
#  liDF <- as.data.frame(allInfo)
}
print(length(Emails))
print(length(Names))
print(length(Info))
print(length(Links))
#liDF <- data.frame('Email' = Emails, 'Name' = Names, 'Info' = Info, 'Links' = Links)
myVals <- list(Emails, Names, Info, Links)
}
  
  
  
