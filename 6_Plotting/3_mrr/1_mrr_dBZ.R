# set working directory
getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/"
setwd(wd)
# Load modified 'myContourPlot' function
source("myContourPlot.R")
# List files in fileList
a <- list.files(paste(wd,"mrr/dbz/",sep=""),pattern=".csv")

# Plotting routine
for(i in a){
  mrr_dbz <- as.matrix(read.table(paste(wd,"mrr/dbz/",i,sep=""),header=F,sep=","))
  date1 <-strptime(as.character(mrr_dbz[,1]), format="%Y-%m-%d %H:%M")
  x <- seq(min(as.POSIXct(date1)),max(as.POSIXct(date1)),length.out=nrow(mrr_dbz))
  y <- seq(35,1085,length.out=31)  
  #  y <- seq(0,2000/1000,length=512)
  z <- mrr_dbz[,-1]
  test <- apply(z,c(1,2),as.numeric)
  xlim = range(date1[1],max(date1))
  gridx <-seq(from=x[1],to=max(x),by="hour")
  
  #  xtemp <- substring(i,1,8)  
  xtemp <- substring(i,1,17)
  tiff(paste(xtemp,"_dbz_plot.tiff", sep=""),height=10,width=15,unit="cm",pointsize=10,res=300)
  
  myContourPlot(x,y,test,zlim=range(0,max(test)),
                color.palette=colorRampPalette(c("blue","cyan","yellow", "red"),interpolate="linear",space="rgb"),
                nlevels=30,las=1,
                plot.title=paste("Reflectivity - ",xtemp),
                xlab="Hour", ylab="Height [m]",
                grid(col="darkgrey", lty="dotted"),
                abline(v=gridx, col="darkgrey", lty="dotted"))
  dev.off()
}