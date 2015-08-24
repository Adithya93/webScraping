library(stringr)
library(dplyr)
## Add more keywords to lists
gaugeEdu <- function(x){
  if(is.na(x)) {
    return(NA)
  }
  smallX <- str_to_lower(x)
  if(any(str_count(smallX, pattern=c('mba','master','phd', 'doctorate', 'postgrad', 
                                     'msc','post-grad', 'm.sc', 'm.b.a')))) {
    return(3)
  }
  else if(any(str_count(smallX, pattern=c('bachelor', 'degree', 'graduate', 'bsc', 'b.sc', 'b.e', 'm.a', 'b.a')))){
    return(2)
  }
  else if(any(str_count(smallX, pattern=c('diploma', 'polytechnic', 'student', 'certificate', 'undergraduate')))){
    return(1)
  }
  else if(str_count(smallX, 'unknown') || nchar(x) < 5){
    return(NA)
  }
  else{
    return(0)
  }
}

## Add more keywords to lists
gaugeSeniority <- function(x){
  if(is.na(x)) {
    return(NA)
  }
  smallX <- str_to_lower(x)
  if(any(str_count(smallX, pattern=c('direct',' ceo ','president', 'founder', 'vp', 'chief executive officer', 'dean'
                                     , 'head', 'lead', ' cfo ', ' gm ', 'general manager', 'counsel')))){
    return(3)
  }
  else if(any(str_count(smallX, pattern=c('manag', 'engineer', 'architect', 'owner', 'chief', 'executive', 'sales', 'developer', 
                                          'professor', 'consultant', 'senior', 'maintenance', 'special', 'supervisor', 'partner', 'programmer'
                                          , 'advis')))){
    return(2)
  }else if(any(str_count(smallX, pattern=c('admin', 'technician', 'teacher', 'staff', 'analyst', 'officer', 'assistant', 
                                           'representative', 'inspector', 'economist', 'junior', 'support', 'intern', ' hr ')))){
    return(1)
  }
  else if(str_count(x, 'unknown') || nchar(x) < 5){
    return(NA)
  }
  else{
    return(0)
  }
}

# Takes in a LinkedIn Data Frame x and returns n by 2 Data Frame with factors from 0 to 3
# guessing Education and Salary levels
gaugePotential <- function(x){
  emails <- x$Email
  edulevs <- as.character(x$LI_EDUCATIONLEVEL)
  worklevs <- as.character(x$LI_TITLE)
  booya <- as.data.frame(sapply(edulevs, gaugeEdu))
  wicked <- as.data.frame(sapply(worklevs, gaugeSeniority))              
  guessDF <- data.frame(emails, booya, wicked)
  names(guessDF) <- c('Email', 'IM_INFERRED_EDUCATION_LEVEL_NUM', 'IM_INFERRED_SALARY_LEVEL_NUM')
  augDF <- inner_join(x, guessDF)
  return(augDF)
}

