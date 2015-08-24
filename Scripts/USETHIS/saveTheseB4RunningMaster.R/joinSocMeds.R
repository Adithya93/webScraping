joinSocMeds <- function(LI, TW, FB, COMP) {
  if(names(LI)[1] != 'Email') {
    names(LI)[1] <- 'Email'
    LI$Email <- as.character(LI$Email)
  }
  TW$Email <- as.character(TW$Email)
  FB$Email <- as.character(FB$Email)
  COMP$Email <- as.character(COMP$Email)
  
  
  LITWDF1 <- left_join(LI, TW)
  LITWDF2 <- left_join(TW, LI)
  LITWDF <- unique(rbind(LITWDF1, LITWDF2))
  JointDF1 <- left_join(LITWDF, FB)
  JointDF2 <- left_join(FB, LITWDF)
  JointDF <- unique(rbind(JointDF1, JointDF2))
  
  print(ncol(JointDF))
  JointDF$Email <- as.character(JointDF$Email)
  COMP$Email <- as.character(COMP$Email)
  withComp1 <- left_join(JointDF, COMP, by = 'Email')
  print(ncol(withComp1))
  withComp2 <- left_join(COMP, JointDF, by = 'Email')
  print(ncol(withComp2))
  AllDF <- unique(rbind(withComp1, withComp2))
  return(AllDF)
}