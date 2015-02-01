library(scales)
library(grid)
library(reshape2)
library(ggplot2)
library(gridExtra)
library(zoo)

# Set working directory
getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/"
setwd(wd)

# Path to campbell data
fileList <-list.files(paste(wd,"campbell/", sep=""),pattern="csv")

for (i in fileList){
  
  campbell <- read.table((paste(wd,"campbell/",i, sep="")), header = T, sep=",")
  j <- substring(i,1,17)
  # Path to relative humidity data from HLUG, as rH values from Linden sensors are corrupted
  if(file.exists(paste(wd,"hlug/",j,"_VPF710.csv", sep=""))){
    hlug <- read.table((paste(wd,"hlug/",j,"_VPF710.csv", sep="")), header = T, sep=",")
  } else {
    next
  }

  T1_2m_Avg <- data.frame(datetime = as.POSIXct(campbell$datetime), Tair = campbell$T1_2m_Avg)

  rH_2m <- data.frame(datetime = as.POSIXct(hlug$datetime), rH =hlug$rH)
  
  combine <- merge(T1_2m_Avg,rH_2m,by="datetime",all=T, sort=T)
  rhInterpolate <- na.approx(combine$rH)
  
  # Open tiff file 
  tiff(paste(j,"_Tair_relH.tiff", sep=""),height=13,width=20,unit="cm", pointsize=6,res=300) 

  # Plotting routine
  par(mfrow=c(1,1), cex.axis=1, cex.main=1.5, cex.lab=1.5, mar=c(2,2,1,2), oma =c(2,3,2,3))
  plot(combine$datetime, 
       combine$Tair,
       ylim=c(0,5),
       ylab="[°C]",
       xlab="Hours (UTC)",
       type = "l",   
       col ="red",
       xaxt="n") 
  title(main=paste(j," - Temperature and rel. Humidity at 2m"),outer=TRUE)
  mtext("Hours (UTC)",side=1,line= 2.5)
  mtext("[°C]",side=2,line= 2.5)
  par(new=TRUE)
  plot(combine$datetime, combine$rH, col="blue",type="p",pch=21, yaxt="n", xaxt="n",ylab="", xlab="")
  axis(4, col="black",lwd=1)
  mtext("[%]",side=4,line=2.5)
  axis.POSIXct(1, at=seq(combine$datetime[1],combine$datetime[length(combine$datetime)], by="hour"), 
               format="%H")
  legend("bottomright",1.9, c("Tair", "rel. Humidity"), 
         col = c("red", "blue"), lty=c(1,1),inset=.01, x.intersp=1, y.intersp=1)
  # Save tiff file
  dev.off()
}



