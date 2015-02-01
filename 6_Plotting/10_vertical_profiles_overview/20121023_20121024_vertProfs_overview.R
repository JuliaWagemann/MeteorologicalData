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

source("H:/Masterarbeit/2_Data/3_fog_time_series/dsd/plots/vertProfs_overview_settings.R")

getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/dsd/plots/"
setwd(wd)
fogevent <- '20121023_20121024'

title <- paste("Fog event - ",fogevent)

i <- paste(fogevent,'_dBZProfiles.csv', sep ="")
j <- paste(fogevent,'_groundCombined.csv', sep="")
k <- paste(fogevent,'_profileCombined.csv', sep="")

nc <-max(count.fields(paste(wd,"dBZ_theo_ground/",j,sep=""), sep=","))
length <- ceiling(nc/3.90625)+2

dBZ_cr <- read.csv(paste(wd,"dBZ/",i,sep=""),header=F,sep=",")
dBZ_theo_ground <- read.csv(paste(wd,"dBZ_theo_ground/",j,sep=""),col.names=(paste("v",1:nc,sep="")),header=F,sep=",",fill=T)
dBZ_theo_profile <- read.csv(paste(wd,"dBZ_theo_profile/",k,sep=""),col.names=(paste("v",1:nc,sep="")),header=F,sep=",",fill=T)

y1 <- seq(0,(length-2)*3.90625,length=length-1)  # height dBZ
y2 <- seq(0,nc-2)   # height theoretical Profiles

df_cr <- data.frame(dBZ_cr[2:length])
df_ground <- data.frame(dBZ_theo_ground[2:nc])
df_profile <- data.frame(dBZ_theo_profile[2:nc])

vec <- rep(nrow(df_cr),times=length-1)
Height_cr <- rep(y1,times=vec)

mat.cr <- melt(df_cr)
dBZ <- mat.cr$value


###############################################################################
### PREPARE DATA FRAMES #######################################################
###############################################################################

for (p in 1:nrow(df_cr)){
  x01 <- c(as.numeric(df_cr[p,]))
  y01 <- c(as.numeric(df_ground[p,]))
  z01 <- c(as.numeric(df_profile[p,]))
  
  DF11 <- data.frame(height=y1,dBZ_measured = x01)
  DF12 <- data.frame(height=y2,theoretical_ground = y01, theoretical_profile = z01)
  
  DF01 <- merge(DF11,DF12,by="height", all=T)
  DF01[DF01==-999.0] <- NA
  
  DF<- data.frame(na.approx(DF01))
  DF_melt <- melt(DF,id="height",variable.name="Profile")
  assign(paste("DF_", p, sep=""), DF)
  assign(paste("DFmelt_", p, sep=""), DF_melt)
}

DF_2$dBZ_measured[DF_2$height>126.000]<-NA
DFmelt_2 <- melt(DF_2,id="height",variable.name="Profile")

x01 <- c(as.numeric(df_cr[0,]))
y01 <- c(as.numeric(df_ground[0,]))
z01 <- c(as.numeric(df_profile[0,]))

DF001 <- data.frame(height=y1,dBZ_measured = x01)
DF002 <- data.frame(height=y2,theoretical_ground = y01, theoretical_profile = z01)

DF01 <- merge(DF001,DF002,by="height", all=T)
DF01[DF01==-999.0] <- NA
DFdummy_melt <- melt(DF01,id="height",variable.name="Profile")
DFdummy_melt2 <- DFdummy_melt

DFdummy_melt$panel  <- "I"
DFdummy_melt2$panel  <- "II"
DFmelt_6$panel <- "III"

###############################################################################
### PLOTTING ##################################################################
###############################################################################

myPaletteMain <- c("#000000","#737373","#BDBDBD")

a =grobTree(textGrob("a)", x=0.03,hjust=0,y=0.99, vjust=1))
b = grobTree(textGrob("b)", x=0.03, hjust=0,y=0.99,vjust=1))
c = grobTree(textGrob("c)", x=0.03, hjust=0,y=0.99,vjust=1))
d = grobTree(textGrob("d)", x=0.03, hjust=0,y=0.99,vjust=1))




Ia = ggplot(data=DFdummy_melt, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype=1, size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dbZ") +
#  annotation_custom(a) +
  mythemeIa

Ib = ggplot(data=DFdummy_melt, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE, linetype=1, size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
#  annotation_custom(b) +
  mythemeIb

Ic = ggplot(data=DFdummy_melt, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype=1,size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
#  annotation_custom(c) +
  mythemeIb

Id = ggplot(data=DFdummy_melt, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype="solid",size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  facet_grid(panel ~.) +
#  annotation_custom(d) +
  mythemeIc

IIa = ggplot(data=DFmelt_1, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype=1, size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  annotation_custom(a) +
  mythemeIIa

IIb = ggplot(data=DFmelt_2, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE, linetype=1, size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  annotation_custom(b) +
  mythemeIIb

IIc = ggplot(data=DFdummy_melt2, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype=1,size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
#  annotation_custom(c) +
  mythemeIIb

IId = ggplot(data=DFdummy_melt2, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype="solid",size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  facet_grid(panel ~.) +
#  annotation_custom(d) +
  mythemeIIc

IIIa = ggplot(data=DFmelt_3, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype=1, size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  annotation_custom(a) +
  mythemeIIIa

IIIb = ggplot(data=DFmelt_4, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE, linetype=1, size=0.8) +
#  guides(colour=TRUE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  annotation_custom(b) +
  mythemeIIIb1 +
  theme(legend.key = element_blank()) +
  theme(legend.background=element_rect(fill="white", colour="darkgrey"))+
  theme(legend.text=element_text(size=14, colour ="black"))+
  theme(legend.title=element_text(size=14))

IIIc = ggplot(data=DFmelt_5, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype=1,size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  annotation_custom(c) +
  mythemeIIIb2

IIId = ggplot(data=DFmelt_6, aes(x=value,y=height, color=Profile)) +
  geom_path(NA.rm=TRUE,linetype="solid",size=0.8) +
  guides(colour=FALSE)+
  scale_colour_manual(values=myPaletteMain) +
  xlim(-60,0) +
  labs(y="Height [m] (AGL)", x="dBZ") +
  facet_grid(panel ~.) +
  annotation_custom(d) +
  mythemeIIIc


IaGrob <- ggplotGrob(Ia)
IbGrob <- ggplotGrob(Ib)
IcGrob <- ggplotGrob(Ic)
IdGrob <- ggplotGrob(Id)

IIaGrob <- ggplotGrob(IIa)
IIbGrob <- ggplotGrob(IIb)
IIcGrob <- ggplotGrob(IIc)
IIdGrob <- ggplotGrob(IId)

IIIaGrob <- ggplotGrob(IIIa)
IIIbGrob <- ggplotGrob(IIIb+theme(legend.position="none"))
IIIcGrob <- ggplotGrob(IIIc)
IIIdGrob <- ggplotGrob(IIId)

g_legend<-function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}

myLegend <- g_legend(IIIb)

finalPlot <- grid.arrange(arrangeGrob(IaGrob,IbGrob,IcGrob,IdGrob,ncol=4,nrow=1,
                                      heights=c(1.1,0.9,1,0.25), widths=c(1.1,0.9,0.9,1.1)),
                          arrangeGrob(IIaGrob,IIbGrob,IIcGrob,IIdGrob, ncol=4,nrow=1,
                                      heights=c(1.1,0.9,1,0.25), widths=c(1.1,0.9,0.9,1.1)),
                          arrangeGrob(IIIaGrob,IIIbGrob,IIIcGrob, IIIdGrob,ncol=4,nrow=1,
                                      heights=c(1.1,0.9,1,0.25), widths=c(1.1,0.9,0.9,1.1)),
                          myLegend,ncol=1,nrow=4,
                          heights=c(1.1,0.9,1.1,0.25), widths=c(1.1,0.8,0.8,1.1),
                          main=textGrob(title,gp=gpar(fontsize=20,font=1),vjust=1.5))
finalPlot

