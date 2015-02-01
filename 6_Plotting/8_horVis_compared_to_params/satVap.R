getwd()
wd <- "H:/Masterarbeit/2_Data/3_fog_time_series/cluster_analysis/"
setwd(wd)

path <- "H:/Masterarbeit/2_Data/4_Plots/3_horVis_params/2_satVap/"

i<- "20121019_20121020"
j <- 7
horVis <- read.table(paste(wd,"horVis/",i,"_VPF710.csv",sep=""),header=TRUE,sep=",")
campbell <- read.table(paste(wd,"campbell/",i,"_campbell.csv",sep=""),header=TRUE,sep=",")
BP <- read.table(paste(wd,"breakPoints.csv",sep=""),header=TRUE,sep=";")

wv_diff <- campbell$VP_Avg-campbell$VP_sat_Avg

df_campbell <- data.frame(datetime = as.POSIXct(campbell$datetime), vp=campbell$VP_Avg,
                          vpSat=campbell$VP_sat_Avg,wvDiff=wv_diff)
df_horVis <- data.frame(datetime = as.POSIXct(horVis$datetime), horVis=horVis$Vis)

tiff(file=paste(path,i,"._poster.tiff",sep=""),width=1382,height=1217, units="px",res=300, compression="lzw")
par(mfrow=c(2,1),mar=c(0.5,0.5,0,0),oma=c(2.5,2.5,2,1),cex.axis=0.8,cex.main=0.9)
plot(df_horVis$datetime,df_horVis$horVis,type="l",
     log="y",
     xaxt="n",
     yaxp=c(0.1,10,1),
     mgp=c(3,0.5,0)
     )
mtext("[km]",side=2,line=1.7, cex=0.8)
abline(h=1,col="black",lty=4)
abline(v=df_horVis$datetime[BP[1,j]],lty=4)
abline(v=df_horVis$datetime[BP[2,j]],lty=4)
abline(v=df_horVis$datetime[BP[3,j]],lty=4)
abline(v=df_horVis$datetime[BP[4,j]],lty=4)
title(main=paste("#",j," - ",i), outer = TRUE,cex=1)

plot(df_campbell$datetime,df_campbell$vpSat,type="l",
     ylim=c(0.5,2),
     yaxp=c(0,2,4),
     mgp=c(3,0.5,0),
     col="grey50",
     lwd=2)
lines(df_campbell$datetime,df_campbell$vp,lty=1)
mtext("Time", side=1,line=1.7, cex=0.8)
mtext("[hPa]",side=2,line=1.7, cex=0.8)
abline(v=df_campbell$datetime[BP[1,j]],lty=4)
abline(v=df_campbell$datetime[BP[2,j]],lty=4)
abline(v=df_campbell$datetime[BP[3,j]],lty=4)
abline(v=df_campbell$datetime[BP[4,j]],lty=4)
legend("topleft", c("sat. WV", "WV"),lty=c(1,1),col=c("grey50","black"),lwd=c(2,1),inset=0.01,cex=0.6,
       y.intersp=0.8,seg.len=2)
dev.off()
