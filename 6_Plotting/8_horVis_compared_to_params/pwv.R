getwd()
wd <- "H:/Masterarbeit/2_Data/3_fog_time_series/cluster_analysis/"
setwd(wd)

path <- "H:/Masterarbeit/2_Data/4_Plots/3_horVis_params/6_pwv/"

i<- "20121019_20121020"
j <- 7
horVis <- read.table(paste(wd,"horVis/",i,"_VPF710.csv",sep=""),header=TRUE,sep=",")
campbell <- read.table(paste(wd,"gps_wv/",i,"_gps_wv.csv",sep=""),header=TRUE,sep=",")
BP <- read.table(paste(wd,"breakPoints.csv",sep=""),header=TRUE,sep=";")


df_campbell <- data.frame(datetime = as.POSIXct(campbell$dateTime), pwv=campbell$PWV)
df_horVis <- data.frame(datetime = as.POSIXct(horVis$datetime), horVis=horVis$Vis)

df_merged <- merge(df_campbell,df_horVis, by.y="datetime", all.y=TRUE)
new <- df_merged[!is.na(df_merged$pwv),]

tiff(file=paste(path,i,"_poster_.tiff",sep=""),width=1382,height=1217, units="px",res=300, compression="lzw")
par(mfrow=c(2,1),mar=c(0.5,0.5,0,0),oma=c(2.5,2.5,2,1),cex.lab=0.8,cex.axis=0.8,cex.main=0.9)
plot(df_merged$datetime,df_merged$horVis,type="l",
     log="y",
     xaxt="n",
     yaxp=c(0.1,10,1),
     mgp=c(3,0.5,0),
     )
mtext("[km]",side=2,line=1.7, cex=0.8)
abline(h=1,col="black",lty=4)
abline(v=df_horVis$datetime[BP[1,j]],lty=4)
abline(v=df_horVis$datetime[BP[2,j]],lty=4)
abline(v=df_horVis$datetime[BP[3,j]],lty=4)
abline(v=df_horVis$datetime[BP[4,j]],lty=4)
title(main=paste("#",j," - ",i), outer = TRUE,cex=1)

plot(df_merged$datetime,df_merged$pwv,type="b",
     pch=20,
     ylim=c(15,30),
     yaxp=c(10,30,4),
     mgp=c(3,0.5,0),)
lines(new$datetime,new$pwv, )
mtext("[mm]",side=2,line=1.7, cex=0.8)
mtext("Time", side=1,line=1.7,cex=0.8)
abline(v=df_merged$datetime[BP[1,j]],lty=4)
abline(v=df_merged$datetime[BP[2,j]],lty=4)
abline(v=df_merged$datetime[BP[3,j]],lty=4)
abline(v=df_merged$datetime[BP[4,j]],lty=4)
dev.off()
