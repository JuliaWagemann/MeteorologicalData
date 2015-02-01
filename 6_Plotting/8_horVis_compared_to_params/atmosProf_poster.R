library(gdata)
library(scales)
library(grid)
library(reshape2)
library(ggplot2)
library(gridBase)
library(gridExtra)
library(gtable)


getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/"
setwd(wd)

source("atmosProf_settings_poster.R")

path <- "H:/Masterarbeit/2_Data/4_Plots/3_horVis_params/7_vertProfs/"
t <- 7
i <- "20121019_20121020_VPF730.csv"
vpf730 <- read.table((paste(wd,"vpf730/",i, sep="")), header = T, sep=",")
BP <- read.table("breakPoints.csv", header = T, sep=";")
BP_current <- BP[,t]
j <- substring(i,1,17)
if(file.exists(paste(wd,"vpf710/",j,"_VPF710.csv", sep=""))){
  vpf710 <- read.table((paste(wd,"vpf710/",j,"_VPF710.csv", sep="")), header = T, sep=",")
  visData <- data.frame(datetime = as.POSIXct(vpf710$datetime), vis =vpf710$Vis)
} else {
  visData <- data.frame(datetime = as.POSIXct(vpf730$datetime), vis =vpf730$Vis) 
}
#cloudradar <- read.table(paste(wd,"cloudradar/cloudinfo/",j,"_cloudradar_cloudinfo.csv",sep=""), header = T, sep=",")
#highCb <- data.frame(datetime = as.POSIXct(cloudradar$dateTime), highCb=cloudradar$CloudtopHeight_1)

if(file.exists(paste(wd,"cl31/cloudinfo/",j,"_cl31.csv", sep=""))){
  cl31 <- read.table((paste(wd,"cl31/cloudinfo/",j,"_cl31.csv", sep="")), header = T, sep=",")
  lowCb <- data.frame(datetime = as.POSIXct(cl31$datetime), lowCb=cl31$lowCb)
  } else {
  next
}

title <- paste("#",t," - ",j)
#atext = grobTree(textGrob("a)", x=0.01, hjust=0, y=0.99, vjust=1))
a = ggplot(visData, aes(x=datetime,y=vis)) +
  geom_line() +

  scale_y_log10() +
  scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
  geom_hline(yintercept=1, linetype="dotted") +
  geom_vline(xintercept=as.numeric(visData$datetime[BP_current[1:4]]), linetype=4) +
  ggtitle(title) +
#  annotation_custom(atext) +
  labs(y="[km]") +

  mytheme1    


if(file.exists(paste(wd,"cloudradar/dbz_5min/",j,"_cloudinfo_dbz.csv", sep=""))){
  cloudradar <- read.table(paste(wd,"cloudradar/dbz_5min/",j,"_cloudinfo_dbz.csv",sep=""),header=T,sep=",")
  df_cr <- data.frame(cloudradar)
  df_cr <- df_cr[1:53]
  
  y1 <- seq(0,0.2,length=52)
  vec <- rep(nrow(df_cr),times=52)
  Height_cr <- rep(y1,times=vec)
  
  mat.cr <- melt(df_cr)
  dBZ <- mat.cr$value
  Hour_cr <- as.POSIXct(mat.cr$TIME)
  
  breaks_cr <- c(-50,-30,-10)
  btext = grobTree(textGrob("b)",gp=gpar(cex=1), x=0.01, hjust=0, y=0.99, vjust=1))
  b = ggplot(mat.cr, aes(x=Hour_cr,y=Height_cr,fill=dBZ)) +
    geom_raster(interpolate=TRUE) + scale_fill_gradientn(limits=c(-50,0),breaks = breaks_cr,
                                                         colours=c("blue", "cyan", "yellow", "red"),
                                                         na.value="transparent") +

    scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
    scale_y_continuous(breaks=c(0.0,0.1,0.2,0.3)) +
    geom_vline(xintercept=as.numeric(visData$datetime[BP_current[1:4]]), linetype=4) +
    labs(y="Height [km] (AGL)", x="Hour (UTC)") +
#    annotation_custom(btext) +
    mytheme2 +
    guides(fill=guide)

}

if(file.exists(paste(wd,"cl31/backscatter/smoothed/log",j,"_cl31_BS.csv", sep=""))){
  cl31_BS_df <- read.table((paste(wd,"cl31/backscatter/smoothed/log/",j,"_cl31_BS.csv", sep="")),header=F,sep=",")
  df <- data.frame(cl31_BS_df)
  df <- df[,1:52]
  
  y2 <- seq(0,1, length=51)  
  vec <- rep(nrow(cl31_BS_df),times=51)
  Height <- rep(y2,times=vec)
  
  mat.df = melt(df)  
  Backscatter <- mat.df$value
  Hour <- as.POSIXct(mat.df$V1)  
  
  breaks <- c(1,3,5)
  ctext = grobTree(textGrob("c)", x=0.01, hjust=0, y=0.99, vjust=1))
  d = ggplot(mat.df, aes(x=Hour,y=Height,fill=Backscatter)) +
    geom_raster(interpolate=TRUE) + scale_fill_gradientn(limits=c(0,5.5),breaks = breaks,
                                                         colours=c("blue", "cyan", "yellow", "red"),
                                                         na.value="blue4") + 
    scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
    scale_y_continuous(breaks=c(0.0,0.5,1.0)) +
    labs(y="Height [km] (AGL)", x="Hour (UTC)") +
    geom_vline(xintercept=as.numeric(visData$datetime[BP_current[1:4]]), linetype=4) +
#    annotation_custom(ctext) +
    mytheme3 +
    guides(fill=guide)  
}

aGrob <- ggplotGrob(a)
bGrob <- ggplotGrob(b)
cGrob <- ggplotGrob(d)
finalPlot <- arrangeGrob(aGrob,bGrob,cGrob, ncol=1)


tiff(file=paste(path,j,"_poster_.tiff",sep=""),width=1382,height=1217, units="px",res=300, compression="lzw")
finalPlot
dev.off()


keep(wd,mytheme1,mytheme2, mytheme3, guide,sure=TRUE)
  
    