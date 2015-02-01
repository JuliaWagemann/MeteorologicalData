library(gdata)
library(scales)
library(grid)
library(reshape2)
library(ggplot2)
library(gridBase)
library(gridExtra)
library(gtable)
library(wq)
library(RColorBrewer)

getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/"
setwd(wd)

source("vertProf_settings_poster.R")

i <- "20121119_20121120_cloudinfo_dbz.csv"
fogEvent <- 15
BP <- read.table("Bruchpunkte.csv", header = T, sep=";")
fogDev_BP <- read.table("fogDev_BP.csv", header=T, sep=";")
fogMain_BP <- read.table("fogMain_BP.csv", header=T, sep=";")
fogDiss_BP <- read.table("fogDiss_BP.csv", header=T, sep=";")

fogDev_current <- fogDev_BP[,fogEvent]
fogMain_current <- fogMain_BP[,fogEvent]
fogDiss_current <- fogDiss_BP[,fogEvent]
BP_current <- BP[,fogEvent]
j <- substring(i,1,17)

title <- paste("#",fogEvent," - ",j)

cloudradar_5min <- read.table(paste(wd,"cloudradar/dbz_5min/",i,sep=""),header=T,sep=",")

####################################################################################
# Set parameters
####################################################################################

heightMax <- 0.58
heightCloud <- 0.609
heightLength <- 156
rowNr <- nrow(cloudradar_5min)

lengthIIa <- fogMain_current[2] - fogMain_current[1]
lengthIIb <- fogMain_current[3] - fogMain_current[2]
lengthIII <- fogDiss_current[2] - fogDiss_current[1]

c1 <- c(20,30,40,53)
c2 <- c(10,28,43,60)
c3 <- c(2,8,18)

c11 <- c(fogMain_current[1]+c1[1]-1,fogMain_current[1]+c1[2]-1,fogMain_current[1]+c1[3]-1,fogMain_current[1]+c1[4]-1)
c22 <- c(fogMain_current[2]+c2[1]-1,fogMain_current[2]+c2[2]-1,fogMain_current[2]+c2[3]-1,fogMain_current[2]+c2[4]-1)
c33 <- c(fogDiss_current[1]+c3[1]-1,fogDiss_current[1]+c3[2]-1,fogDiss_current[1]+c3[3]-1)
#c33 <- c(0,0,0,0)
####################################################################################

df_cr <- data.frame(cloudradar_5min[1:(heightLength+1)])
y1 <- seq(0,heightCloud,length=heightLength)
vec <- rep(nrow(df_cr),times=heightLength)
Height_cr <- rep(y1,times=vec)

mat.cr <- melt(df_cr)
dBZ <- mat.cr$value
Hour_cr <- as.POSIXct(mat.cr$TIME)


df_cr5min <- data.frame(cloudradar_5min[2:(heightLength+1)])

vertProf_21 <- df_cr5min[fogMain_current[1]:fogMain_current[2],]
vertProf_22 <- df_cr5min[fogMain_current[2]:fogMain_current[3],]
vertProf_23 <- df_cr5min[fogDiss_current[1]:fogDiss_current[2],]


height <- seq(0,heightCloud, length=heightLength)

x01 <- c(as.numeric(vertProf_21[c1[1],]))
x21 <- c(as.numeric(vertProf_21[c1[2],]))
x31 <- c(as.numeric(vertProf_21[c1[3],])) 
x41 <- c(as.numeric(vertProf_21[c1[4],]))

x22 <- c(as.numeric(vertProf_22[c2[1],]))
x32 <- c(as.numeric(vertProf_22[c2[2],])) 
x42 <- c(as.numeric(vertProf_22[c2[3],]))
x52 <- c(as.numeric(vertProf_22[c2[4],]))

x23 <- c(as.numeric(vertProf_23[c3[1],]))
x33 <- c(as.numeric(vertProf_23[c3[2],])) 
x43 <- c(as.numeric(vertProf_23[c3[3],]))
x53 <- c(as.numeric(vertProf_23[c3[4],]))

my.cols <- brewer.pal(9,"OrRd")
myPaletteMain <- c("#BDBDBD","#969696","#525252","#000000")
myPaletteDiss <- c("#C6DBEF","#6BAED6", "#2171B5","#08306B")

DF1 <- data.frame(height = height, vec01 = x01, vec21 = x21, vec31 = x31,vec41=x41)
DF1[DF1==-999] <- NA
DF1_melt <- melt(DF1,id="height")

DF2 <- data.frame(height = height, vec22 = x22, vec32 = x32, vec42 = x42,vec52=x52)
DF2[DF2==-999] <- NA
DF2_melt <- melt(DF2,id="height")

DF3 <- data.frame(height = height, vec23 = x23, vec33 = x33, vec43 = x43,vec53=x53)
DF3[DF3==-999] <- NA
DF3_melt <- melt(DF3,id="height")

IIa =grobTree(textGrob("IIa", x=0.03,hjust=0,y=0.98, gp=gpar(fontsize=7), vjust=1))
IIb = grobTree(textGrob("IIb", x=0.03, hjust=0,y=0.98,gp=gpar(fontsize=7),vjust=1))
III = grobTree(textGrob("III", x=0.03, hjust=0,y=0.98,gp=gpar(fontsize=7),vjust=1))

a = ggplot(data=DF1_melt, aes(x=value,y=height, color=variable)) +
  geom_path(size=0.3) +
  geom_point(size=0.7)+
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  scale_y_continuous(breaks=c(0.0,0.1,0.2,0.3,0.4,0.5,0.6)) +
  labs(y="Height [km] (AGL)", x="dbZ") +
  annotation_custom(IIa) +
  mytheme1

b = ggplot(data=DF2_melt, aes(x=value,y=height, color=variable)) +
  geom_path(size=0.3) +
  geom_point(size=0.7)+
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  scale_y_continuous(breaks=c(0.0,0.1,0.2,0.3,0.4,0.5,0.6)) +
  labs(y="Height [km] (AGL)", x="dbZ") +
  annotation_custom(IIb) +
  mytheme2

c = ggplot(data=DF3_melt, aes(x=value,y=height, color=variable)) +
  geom_path(size=0.3) +
  geom_point(size=0.7)+
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  scale_y_continuous(breaks=c(0.0,0.1,0.2,0.3,0.4,0.5,0.6)) +
  labs(y="Height [km] (AGL)", x="dbZ") +
  annotation_custom(III) +
  mytheme3

pos1 <- (fogMain_current[1]+(0.5*(lengthIIa-3)))/rowNr
pos2 <- (fogMain_current[2]+(0.3*(lengthIIb-3)))/rowNr
pos3 <- (fogDiss_current[1]+(0.3*(lengthIII-12)))/rowNr

breaks_cr <- c(-50,-40,-30,-20,-10,0)
firstText =grobTree(textGrob("IIa", x=pos1,hjust=0,y=0.98, gp=gpar(fontsize=7), vjust=1))
secondText = grobTree(textGrob("IIb", x=pos2, hjust=0,y=0.98,gp=gpar(fontsize=7),vjust=1))
thirdText = grobTree(textGrob("III", x=pos3, hjust=0,y=0.98,gp=gpar(fontsize=7),vjust=1))


d = ggplot(mat.cr, aes(x=Hour_cr,y=Height_cr,fill=dBZ)) +
  annotate("rect", xmin=Hour_cr[fogMain_current[1]], xmax=Hour_cr[fogMain_current[2]-1],ymin=0.015,ymax=heightMax, alpha=.5,fill="lightgrey")+
  annotate("rect", xmin=Hour_cr[fogMain_current[2]], xmax=Hour_cr[fogMain_current[3]-1],ymin=0.015,ymax=heightMax, alpha=.5,fill="lightgrey")+
  annotate("rect", xmin=Hour_cr[fogDiss_current[1]], xmax=Hour_cr[fogDiss_current[2]],ymin=0.015,ymax=heightMax, alpha=.5,fill="lightgrey")+
  geom_raster(interpolate=TRUE) + scale_fill_gradientn(limits=c(-50,0),breaks = breaks_cr,
                                                       colours=c("blue", "cyan", "yellow", "red"),
                                                       na.value="transparent") +
  scale_x_datetime(labels= date_format("%H"),breaks= date_breaks("2 hour")) +
  scale_y_continuous(breaks=c(0.0,0.1,0.2,0.3,0.4,0.5,0.6)) +
  
  geom_segment(aes(x = Hour_cr[c11[1]], y = 0.025, xend = Hour_cr[c11[1]], 
                   yend = height[length(DF1$vec01[!is.na(DF1$vec01)])+13]),
               colour="#BDBDBD",size=0.5) +
  geom_segment(aes(x = Hour_cr[c11[2]], y = 0.025, xend = Hour_cr[c11[2]], 
                   yend = height[length(DF1$vec21[!is.na(DF1$vec21)])+13]),
               colour="#969696",size=0.5) +
  geom_segment(aes(x = Hour_cr[c11[3]], y = 0.025, xend = Hour_cr[c11[3]], 
                   yend = height[length(DF1$vec31[!is.na(DF1$vec31)])+13]),
               colour="#525252",size=0.5) +
  geom_segment(aes(x = Hour_cr[c11[4]], y = 0.025, xend = Hour_cr[c11[4]], 
                   yend = height[length(DF1$vec41[!is.na(DF1$vec41)])+13]),
               colour="#000000",size=0.5) + 
  geom_segment(aes(x = Hour_cr[c22[1]], y = 0.025, xend = Hour_cr[c22[1]], 
                   yend = height[length(DF2$vec22[!is.na(DF2$vec22)])+13]),
               colour="#BDBDBD",size=0.5) +
  geom_segment(aes(x = Hour_cr[c22[2]], y = 0.025, xend = Hour_cr[c22[2]], 
                   yend = height[length(DF2$vec32[!is.na(DF2$vec32)])+13]),
               colour="#969696",size=0.5) +
  geom_segment(aes(x = Hour_cr[c22[3]], y = 0.025, xend = Hour_cr[c22[3]], 
                   yend = height[length(DF2$vec42[!is.na(DF2$vec42)])+13]),
               colour="#525252",size=0.5) +
  geom_segment(aes(x = Hour_cr[c22[4]], y = 0.025, xend = Hour_cr[c22[4]], 
                   yend = height[length(DF2$vec52[!is.na(DF2$vec52)])+13]),
               colour="#000000",size=0.5) +
 geom_segment(aes(x = Hour_cr[c33[1]], y = 0.025, xend = Hour_cr[c33[1]], 
                  yend = height[length(DF3$vec23[!is.na(DF3$vec23)])+13]),
              colour="#BDBDBD",size=0.5) +
 geom_segment(aes(x = Hour_cr[c33[2]], y = 0.025, xend = Hour_cr[c33[2]], 
                  yend = height[length(DF3$vec33[!is.na(DF3$vec33)])+13]),
              colour="#969696",size=0.5) +
 geom_segment(aes(x = Hour_cr[c33[3]], y = 0.025, xend = Hour_cr[c33[3]], 
                  yend = height[length(DF3$vec43[!is.na(DF3$vec43)])+13]),
              colour="#525252",size=0.5) +
 geom_segment(aes(x = Hour_cr[c33[4]], y = 0.025, xend = Hour_cr[c33[4]], 
                  yend = height[length(DF3$vec53[!is.na(DF3$vec53)])+16]),
              colour="#000000",size=0.5) +
 geom_segment(aes(x= Hour_cr[fogMain_current[1]], xend=Hour_cr[fogMain_current[2]-1],
                  y= heightMax, yend=heightMax), colour="darkgrey", size=1) +
 geom_segment(aes(x= Hour_cr[fogMain_current[2]], xend=Hour_cr[fogMain_current[3]-1],
                  y= heightMax, yend=heightMax), colour="darkgrey", size=1) +
 geom_segment(aes(x= Hour_cr[fogDiss_current[1]], xend=Hour_cr[fogDiss_current[2]],
                  y= heightMax, yend=heightMax), colour="darkgrey", size=1) +
  labs(y="Height [km] (AGL)", x="Hour (UTC)") +
  mytheme4 +
  guides(fill=guide2) +  
  annotation_custom(firstText) + 
  annotation_custom(secondText) +  
  annotation_custom(thirdText)


aGrob <- ggplotGrob(a)
bGrob <- ggplotGrob(b)
cGrob <- ggplotGrob(c)
dGrob <- ggplotGrob(d)

tiff(file=paste(path,j,"_poster.tiff",sep=""),width=1382,height=1217, units="px",res=300, compression="lzw")
finalPlot <- grid.arrange(arrangeGrob(aGrob,bGrob,cGrob, ncol=3),dGrob, nrow=2,main=textGrob(title,gp=gpar(fontsize=10,font=1),vjust=1.5))
dev.off()

