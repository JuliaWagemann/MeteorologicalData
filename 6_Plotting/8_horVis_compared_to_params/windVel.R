getwd()
wd <- "H:/Masterarbeit/2_Data/3_fog_time_series/cluster_analysis/"
setwd(wd)

path <- "H:/Masterarbeit/2_Data/4_Plots/3_horVis_params/5_windVel/"

i<- "20121019_20121020"
j <- 7
horVis <- read.table(paste(wd,"horVis/",i,"_VPF710.csv",sep=""),header=TRUE,sep=",")
campbell <- read.table(paste(wd,"usa/",i,"_usa.csv",sep=""),header=TRUE,sep=",")
BP <- read.table(paste(wd,"breakPoints.csv",sep=""),header=TRUE,sep=";")


df_campbell <- data.frame(datetime = as.POSIXct(campbell$datetime), vel=campbell$vel,dir=campbell$dir)
df_horVis <- data.frame(datetime = as.POSIXct(horVis$datetime), horVis=horVis$Vis)

tiff(file=paste(path,i,"._poster.tiff",sep=""),width=1382,height=1217, units="px",res=300, compression="lzw")
par(mfrow=c(3,1),mar=c(0.5,1,0,0),oma=c(2.5,2.5,2,1),cex.axis=1.2,cex.lab=0.8,cex.main=1.4)
plot(df_horVis$datetime,df_horVis$horVis,type="l",
     log="y",
     xaxt="n",
     yaxp=c(0.1,100,1),
     mgp=c(3,0.5,0),
     )
mtext("[km]",side=2,line=1.8, cex=0.8)
abline(h=1,col="black",lty=4)
abline(v=df_horVis$datetime[BP[1,j]],lty=4)
abline(v=df_horVis$datetime[BP[2,j]],lty=4)
abline(v=df_horVis$datetime[BP[3,j]],lty=4)
abline(v=df_horVis$datetime[BP[4,j]],lty=4)
title(main=paste("#",j," - ",i), outer = TRUE,cex=1)

plot(df_campbell$datetime,df_campbell$vel,type="l",
     ylim=c(0,2.5),
     yaxp=c(0,2,2),
     mgp=c(3,0.5,0),
     xaxt="n")
mtext("[m " ~ s^-1 ~ "]",side=2,line=1.8, cex=0.8)
abline(v=df_campbell$datetime[BP[1,j]],lty=4)
abline(v=df_campbell$datetime[BP[2,j]],lty=4)
abline(v=df_campbell$datetime[BP[3,j]],lty=4)
abline(v=df_campbell$datetime[BP[4,j]],lty=4)

plot(df_campbell$datetime,df_campbell$dir,type="l",
     ylim=c(0,360),
     yaxp=c(0,300,2),
     mgp=c(3,0.5,0),)
mtext("Time", side=1,line=1.8, cex=0.8)
mtext("[°]",side=2,line=1.8, cex=0.8)
abline(v=df_campbell$datetime[BP[1,j]],lty=4)
abline(v=df_campbell$datetime[BP[2,j]],lty=4)
abline(v=df_campbell$datetime[BP[3,j]],lty=4)
abline(v=df_campbell$datetime[BP[4,j]],lty=4)
dev.off()