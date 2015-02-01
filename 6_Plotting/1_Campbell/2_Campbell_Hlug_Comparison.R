library(scales)
library(grid)
library(reshape2)
library(ggplot2)
library(gridExtra)
####################################################################
# This script takes campbell and hlug data and compares air temperature
# relative Humidity and Solar radiation
####################################################################

# Set working directory
getwd()
wd <-"H:/Masterarbeit/2_Data/2_Daten_gemittelt/"
setwd(wd)

# List all campbell files
fileList <-list.files("H:/Masterarbeit/2_Data/2_Daten_gemittelt/campbell/")
for (i in fileList){
 
  campbell <- read.table((paste(wd,"campbell/",i, sep="")), header = F, sep=",")
  if(i == "20121030.csv"){
    next
  }
  if(i == "20121218.csv" || i =="20121219.csv" || i=="20121220.csv"){
    campbell <- campbell[-14]
  }
  # Check if 
  if(file.exists(paste(wd,"hlug/",i, sep=""))){
    hlug <- read.table((paste(wd,"hlug/",i, sep="")), header = F, sep=",")
  } else {
    next
  }

  # Establish data frames
  T_2m <- data.frame(datetime = campbell$V1, T2m = campbell[,19], T2mAir = campbell$V3)
  T_2m_Air <- campbell$V3
  T_hlug <- data.frame(datetime =hlug$V1, Thlug= hlug$V2)
  
  rH_2m <- data.frame(datetime = campbell$V1, rH_2m = campbell[,21])
  rH_Psy <- campbell$V18
  rH_hlug <- data.frame(datetime = hlug$V1, rH_hlug = hlug$V3)
  
  rad <- data.frame(datetime = campbell$V1, rad = campbell$V4)
  rad_hlug <- data.frame(datetime = hlug$V1, rad_hlug = hlug$V4)
  
  combine1 = merge(T_2m, T_hlug, by="datetime",all=T, sort=T)
  combine2 = merge(rH_2m, rH_hlug, by="datetime",all=T, sort=T)
  combine3 = merge(rad, rad_hlug, by="datetime",all=T, sort=T)
  
  df1<- data.frame(Hour=as.POSIXct(combine1$datetime),y = c(combine1$T2m,combine1$Thlug), levelTemp=rep(c("T2m", "Thlug"),each=nrow(campbell)))
  df2 <- data.frame(Hour=as.POSIXct(combine2$datetime),y= c(combine2$rH_2m,combine2$rH_hlug), levelrH=rep(c("rH_2m", "rH_hlug"),each=nrow(campbell)))
  df3 <- data.frame(Hour=as.POSIXct(combine3$datetime),y= c(combine3$rad,combine3$rad_hlug), levelRad=rep(c("rad", "rad_hlug"),each=nrow(campbell)))
  
  df1$panel  <- "Temperature"
  df2$panel  <- "rel. Humidity"
  df3$panel  <- "Radiation"
  
  mytheme_df1 <- theme_bw() + 
    theme(plot.margin=unit(c(1.5,1.6,0,1.5),"lines")) +
    theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
    theme(axis.text = element_text(size=8, colour = "black")) +
    theme(axis.title.y = element_text(vjust = 0.1,size=8,colour="black")) + 
    theme(axis.title.x = element_text(vjust = -0.4,size = 8, colour = "black")) +
    theme(plot.title=element_text(size = 10,colour = "black",vjust= 1.5)) +
    theme(axis.ticks.x = element_blank())+
    theme(axis.text.x = element_blank()) +
    theme(legend.text =element_text(size=6,colour="black")) +
    theme(strip.text.y = element_text(size=6, colour = "grey20"))
  
  mytheme_df2 <- theme_bw() + 
    theme(plot.margin=unit(c(0.5,1,0,1.5),"lines")) +
    theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
    theme(axis.text = element_text(size=8, colour = "black")) +
    theme(axis.title.y = element_text(vjust = 0.1,size=8,colour="black")) + 
    theme(axis.title.x = element_text(vjust = -0.4,size = 8, colour = "black")) +
    theme(axis.ticks.x = element_blank())+
    theme(axis.text.x = element_blank()) +
    theme(plot.title=element_text(size = 11,colour = "black",vjust= 1.5)) +
    theme(legend.text =element_text(size=6,colour="black"))+
    theme(strip.text.y = element_text(size=6, colour = "grey20"))
  
  mytheme_df3 <- theme_bw() + 
    theme(plot.margin=unit(c(0.5,1,1.5,1.5),"lines")) +
    theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
    theme(axis.text = element_text(size=8, colour = "black")) +
    theme(axis.title.y = element_text(vjust = 0.1,size=8,colour="black")) + 
    theme(axis.title.x = element_text(vjust = -0.4,size = 8, colour = "black")) +
    theme(plot.title=element_text(size = 11,colour = "black",vjust= 1.5)) +
    theme(legend.text =element_text(size=6,colour="black"))+
    theme(strip.text.y = element_text(size=6, colour = "grey20"))
  
  xtemp <- substring(i,1,nchar(i)-4)
  title <- bquote(paste("Campbell and HLUG comparison - ", .(xtemp)))
  
  p1  <- ggplot(df1, aes(x=Hour,y=y), group=levelTemp) +
    theme_bw() +
    geom_line(aes(colour=levelTemp), size=0.5) +
    geom_point(aes(x = as.POSIXct(combine1$datetime),y=combine1$Thlug), colour = "red", size=1) +
    ggtitle(title) +
    scale_colour_manual("",values=c("darkgrey", "red")) +
    scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
    labs(x=NULL, y="[?C]") +
    facet_grid(panel ~.) +
    mytheme_df1
  
  p2 <- ggplot(df2, aes(x=Hour,y=y), group=levelrH) +
    theme_bw() +
    geom_line(aes(colour=levelrH), size=0.5) +
    geom_point(aes(x = as.POSIXct(combine2$datetime),y=combine2$rH_hlug), colour = "red", size=1) +
    scale_colour_manual("",values=c("darkgrey", "red")) +
    scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
    labs(x=NULL, y="[%]") +
    facet_grid(panel ~.) +
    mytheme_df2
  
  p3 <- ggplot(df3, aes(x=Hour,y=y), group=rad) +
    theme_bw() +
    geom_line(aes(colour=levelRad), size=0.5) +
    geom_point(aes(x = as.POSIXct(combine3$datetime),y=combine3$rad_hlug), colour = "red", size=1) +
    scale_colour_manual("",values=c("darkgrey", "red")) +
    scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
    labs(x="Hour (UTC)", y="W" ~ m^-2) +
    facet_grid(panel ~.) +
    mytheme_df3
  
  pt1<- ggplot_gtable(ggplot_build(p1))
  pt2<- ggplot_gtable(ggplot_build(p2))
  pt3<- ggplot_gtable(ggplot_build(p3))
  maxWidth = unit.pmax(pt1$widths[2:5],pt2$widths[2:5],pt3$widths[2:5])
  pt1$widths[2:5] <- as.list(maxWidth)
  pt2$widths[2:5] <- as.list(maxWidth)
  pt3$widths[2:5] <- as.list(maxWidth)
  
  grid.arrange(pt1,pt2,pt3,ncol=1)  
  tiff(paste(xtemp,"_campbell_hlug.tiff", sep=""),height=13,width=20,unit="cm", pointsize=6,res=300)
  print(grid.arrange(pt1,pt2,pt3,ncol=1))
  dev.off()
}
