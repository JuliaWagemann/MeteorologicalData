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
fileList <-list.files(paste(wd,"usa/",sep=""))

# Plotting routine
for (i in fileList){
  usa <- read.table(paste(wd,"usa/",i,sep=""), header = T, sep=",")
  j <- substring(i,1,17)
  
  combine <- data.frame(datetime = as.POSIXct(usa$datetime), vel=usa$vel,dir=usa$dir)
  
  tiff(paste(j,"_usa.tiff", sep=""),height=13,width=20,unit="cm", pointsize=6,res=300) 
  par(mfrow=c(2,1), cex.axis=1, cex.main=1.5, cex.lab=1.5, mar=c(0,2,0,2), oma =c(4,3,4,3))
  plot(combine$datetime, 
       combine$vel,
       type = "l",   
       col ="black",
       xaxt="n",
       lty=3,
       las=1) 
  title(main=paste(j," - Wind velocity and direction"),outer=TRUE)
  mtext("[ m" ~ s^-1 ~ "]",side=2,line= 3)  
  legend("topleft",2, c("Wind velocity"), 
         col = c("black"), lty=1,inset=.01, x.intersp=1, y.intersp=1)
  plot(combine$datetime,combine$dir, type="p", col="black", xaxt="n",pch=4,yaxp=c(0,360,6),ylim=c(0,360),las=1)
  axis.POSIXct(1, at=seq(combine$datetime[1],combine$datetime[length(combine$datetime)], by="hour"), 
               format="%H")
  legend("topleft",1.9, c("Wind direction"), 
         col = c("black"), lty=c(3),inset=.01, x.intersp=1, y.intersp=1)
  mtext("Hours (UTC)",side=1,line= 2.5)
  mtext("[°]",side=2,line= 3)  

  dev.off()
}  
