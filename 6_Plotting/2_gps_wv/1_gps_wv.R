library(scales)
library(grid)
library(reshape2)
library(ggplot2)
library(gridExtra)

# Set working directory
getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/"
setwd(wd)

# List files in fileList
fileList <-list.files(paste(wd,"gps_wv/",sep=""))

# Plotting routine
for (i in fileList){
  wv <- read.table(paste(wd,"gps_wv/",i,sep=""), header = T, sep=",")
  j <- substring(i,1,17)
  
  combine <- data.frame(datetime = as.POSIXct(wv$dateTime), pwv=wv$PWV,pressure=wv$pressure)

  tiff(paste(j,"_pwv.tiff", sep=""),height=13,width=20,unit="cm", pointsize=6,res=300) 
  par(mfrow=c(1,1), cex.axis=1, cex.main=1.5, cex.lab=1.5, mar=c(0,2,0,2), oma =c(4,3,4,3))
  plot(combine$datetime, 
       combine$pwv,
       type = "b",   
       col ="black",
       xaxt="n",
       pch=19,
       ylim=c(0,20)
  ) 
  
  title(main=paste(j," - Precipitable water vapor"),outer=TRUE)
  mtext("[mm]",side=2,line= 3)

  legend("topright",2, c("pwv"), 
         col = c("black"), lty=1,inset=.01, x.intersp=1, y.intersp=1)
  axis.POSIXct(1, at=seq(combine$datetime[1],combine$datetime[length(combine$datetime)], by="hour"), 
               format="%H")
  mtext("Hours (UTC)",side=1,line= 2.5)
  dev.off()
}  
