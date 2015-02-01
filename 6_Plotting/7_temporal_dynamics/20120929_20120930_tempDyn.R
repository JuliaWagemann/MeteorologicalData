library(hydroGOF)


getwd()
wd <-"H:/Masterarbeit/2_Data/3_fog_time_series/dsd/LWP/Integrals/"
setwd(wd)

fogEvent <- '20120929_20120930_Integrals.csv'
fogEventNr <- 3
Integrals <- read.table(fogEvent, header = T, sep=",")
breakPoints <-read.table('breakpoints_tempDyn.csv', header = T, sep=";") 

LWP.df <- data.frame(dateTime = as.POSIXct(Integrals$dateTime), 
                     LWP_ground = Integrals$LWP_ground, 
                     LWP_profile = Integrals$LWP_profile, 
                     LWP_measured_ground = Integrals$LWP_measured_ground,
                     LWP_measured_profile=Integrals$LWP_measured_profile)
ZIntegral.df <- data.frame(dateTime = as.POSIXct(Integrals$dateTime),
                           dBZ_ground = Integrals$dBZIntegral_ground, 
                           dBZ_profile = Integrals$dBZIntegral_profile, 
                           dBZ_measured = Integrals$dBZIntegral_measured)


ZIntegral_ordered <- ZIntegral.df[order(ZIntegral.df[,1]),]
dateTime <- ZIntegral_ordered$dateTime

diff_ground <- ZIntegral_ordered$dBZ_ground-ZIntegral_ordered$dBZ_measured
diff_profile <- ZIntegral_ordered$dBZ_profile-ZIntegral_ordered$dBZ_measured

ZIntegral_ordered$diff_ground <- diff_ground
ZIntegral_ordered$diff_profile <- diff_profile

ZIntegral_ordered[ZIntegral_ordered$diff_ground==0 | 
                    ZIntegral_ordered$diff_ground<(-4000),]<- NA

ZIntegral_ordered$datetime <- dateTime
ZIntegral_ordered$dateTime <- NULL

TSLength <- length(ZIntegral_ordered$dBZ_measured)

rmse1_2a <- rmse(ZIntegral_ordered$dBZ_ground[1:breakPoints[1,fogEventNr]],
                ZIntegral_ordered$dBZ_measured[1:breakPoints[1,fogEventNr]],na.rm=T)

rmse2_2a<- rmse(ZIntegral_ordered$dBZ_measured[1:breakPoints[1,fogEventNr]],
               ZIntegral_ordered$dBZ_profile[1:breakPoints[1,fogEventNr]])

rmse1_2b <- rmse(ZIntegral_ordered$dBZ_ground[breakPoints[1,fogEventNr]:breakPoints[2,fogEventNr]],
                 ZIntegral_ordered$dBZ_measured[breakPoints[1,fogEventNr]:breakPoints[2,fogEventNr]],na.rm=T)

rmse2_2b<- rmse(ZIntegral_ordered$dBZ_measured[breakPoints[1,fogEventNr]:breakPoints[2,fogEventNr]],
                ZIntegral_ordered$dBZ_profile[breakPoints[1,fogEventNr]:breakPoints[2,fogEventNr]])

rmse1_3 <- rmse(ZIntegral_ordered$dBZ_measured[breakPoints[2,fogEventNr]:TSLength],
                ZIntegral_ordered$dBZ_ground[breakPoints[2,fogEventNr]:TSLength])

rmse2_3 <- rmse(ZIntegral_ordered$dBZ_measured[breakPoints[2,fogEventNr]:TSLength],
                ZIntegral_ordered$dBZ_profile[breakPoints[2,fogEventNr]:TSLength])

rmse1_total <- rmse(ZIntegral_ordered$dBZ_measured[1:TSLength],
                ZIntegral_ordered$dBZ_ground[1:TSLength])
rmse2_total <- rmse(ZIntegral_ordered$dBZ_measured[1:TSLength],
                    ZIntegral_ordered$dBZ_profile[1:TSLength])

######################################################################################################

par(mfrow=c(1,1), cex.axis=1, cex.main=1.5, cex.lab=1.5, mar=c(2,2,1,8.5), 
    oma =c(2,3,1,1),xpd=FALSE)
plot(ZIntegral_ordered$datetime,
     ZIntegral_ordered$diff_ground,
     ylab="",
     xlab="",
     ylim=c(-1500,1500),
     type = "l",   
     col ="black",
     xaxt="n")
abline(h=0,lty=21)
abline(v=ZIntegral_ordered$datetime[breakPoints[1,fogEventNr]],lty=4)
abline(v=ZIntegral_ordered$datetime[breakPoints[2,fogEventNr]],lty=4)

###### For 2 Segments #############################################
# segments(ZIntegral_ordered$datetime[1],3350,ZIntegral_ordered$datetime[breakPoints[1,fogEventNr]-1],
#          3350, lwd=1.5, col="grey20")
# segments(ZIntegral_ordered$datetime[breakPoints[1,fogEventNr]+1],3350,
#          ZIntegral_ordered$datetime[length(ZIntegral_ordered$datetime)],3350,lwd=1.5,
#          col="grey20")


###### For 3 Segments #############################################
segments(ZIntegral_ordered$datetime[1],1400,
         ZIntegral_ordered$datetime[breakPoints[1,fogEventNr]-1],
         1400, lwd=1.5, col="grey20")
segments(ZIntegral_ordered$datetime[breakPoints[1,fogEventNr]+1],1400,
         ZIntegral_ordered$datetime[breakPoints[2,fogEventNr]-1],
         1400, lwd=1.5, col="grey20")
segments(ZIntegral_ordered$datetime[breakPoints[2,fogEventNr]+1],1400,
         ZIntegral_ordered$datetime[length(ZIntegral_ordered$datetime)],1400,lwd=1.5,
         col="grey20")
lines(ZIntegral_ordered$datetime, ZIntegral_ordered$diff_profile,col="darkgrey")
points(ZIntegral_ordered$datetime, ZIntegral_ordered$diff_ground,pch=20)
points(ZIntegral_ordered$datetime, ZIntegral_ordered$diff_profile,pch=20, col="darkgrey")
axis.POSIXct(1, at=seq(ZIntegral_ordered$datetime[1],
                       ZIntegral_ordered$datetime[length(ZIntegral_ordered$datetime)], 
                       by="hour"),format="%H")

mtext("Hour UTC", side=1, line=2.5)
mtext("Difference to measured dBZ (Integral)", side=2, line = 2.8)
mtext("IIa", side =3, line = -1.2,adj=0,at=ZIntegral_ordered$datetime[17])
mtext("IIb", side =3, line = -1.2,adj=0,at=ZIntegral_ordered$datetime[43])
mtext("III", side =3, line = -1.2,adj=0,at=ZIntegral_ordered$datetime[63])
legend("bottom",inset=c(0.01,0.01),c("dsd_ground","dsd_profile"),
       col=c("black","darkgrey"),lty=c(1,1),pch=c(20,20),merge=TRUE, horiz=TRUE,cex=0.9)
par(xpd=TRUE)
legend("right",inset=c(-0.32,0),c('RMSE',
                                  paste('ground_total:',format(round(rmse1_total,2),nsmall=2)),
                                  paste('profile_total:',format(round(rmse2_total,2),nsmall=2)),
                                  paste('ground_IIa:',format(round(rmse1_2a,2),nsmall=2)),
                                  paste('profile_IIa:',format(round(rmse2_2a,2),nsmall=2)),
                                  paste('ground_IIb:',format(round(rmse1_2b,2),nsmall=2)),
                                  paste('profile_IIb:',format(round(rmse2_2b,2),nsmall=2)),
                                  paste('ground_III:',format(round(rmse1_3,2),nsmall=2)),
                                  paste('profile_III:',format(round(rmse2_3,2),nsmall=2)),
                                  lty=NULL),cex=0.9, bty="n",text.font=c(2,1,1,1,1,1,1,1,1))





