# Joins LinkedIn, Twitter & Facebook DFs in a predefined formatting
joinSocMeds <- function(LI, TW, FB) {
  if(names(LI)[1] != 'Email') {
    names(LI)[1] <- 'Email'
  }
  LITWDF1 <- left_join(LI, TW)
  LITWDF2 <- left_join(TW, LI)
  LITWDF <- unique(rbind(LITWDF1, LITWDF2))
  JointDF1 <- left_join(LITWDF, FB)
  JointDF2 <- left_join(FB, LITWDF)
  JointDF <- unique(rbind(JointDF1, JointDF2))
}