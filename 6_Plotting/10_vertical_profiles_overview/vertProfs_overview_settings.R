

mythemeIa <- theme_bw() +
  theme(plot.margin=unit(c(1.5,0.05,0.05,0.57),"cm")) +
  theme(axis.text.y = element_text(size=14, colour = "black")) +
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_blank()) +
  theme(axis.title.x = element_blank())  + 
  theme(axis.ticks.x = element_blank()) +
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5))  

mythemeIb <- theme_bw() +
  theme(plot.margin=unit(c(1.5,0.05,0.05,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.title.x = element_blank())+ 
  theme(axis.text.x = element_blank()) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(axis.ticks.x = element_blank()) +
  theme(plot.title = element_blank())

mythemeIc <- theme_bw() +
  theme(plot.margin=unit(c(1.5,1.5,0.05,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_blank()) +
  theme(axis.title.x = element_blank())  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(axis.ticks.x = element_blank()) +
  theme(strip.text.y = element_text(size = 14, colour = "black", angle = 270))

  
mythemeIIa <- theme_bw() +
  theme(plot.margin=unit(c(0.05,0.05,0.05,0.57),"cm")) +
  theme(axis.text.y = element_text(size=14, colour = "black")) +
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_blank()) +
  theme(axis.title.x = element_blank())  + 
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(axis.ticks.x = element_blank()) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5))  

mythemeIIb <- theme_bw() +
  theme(plot.margin=unit(c(0.05,0.05,0.05,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_blank()) +
  theme(axis.title.x = element_blank())  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(axis.ticks.x = element_blank()) +
  theme(plot.title = element_blank())

mythemeIIc <- theme_bw() +
  theme(plot.margin=unit(c(0.05,1.5,0.05,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_blank()) +
  theme(axis.title.x = element_blank())  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(axis.ticks.x = element_blank()) +
  theme(strip.text.y = element_text(size = 14, colour = "black", angle = 270))

  
mythemeIIIa <- theme_bw() +
  theme(plot.margin=unit(c(0.05,0.05,0.3,0.57),"cm")) +
  theme(axis.text.y = element_text(size=14, colour = "black")) +
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(axis.title.x = element_blank())  + 
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0))

mythemeIIIb1 <- theme_bw() +
  theme(plot.margin=unit(c(0.05,0.05,0.3,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(plot.title = element_blank()) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0)) +
  theme(legend.text=element_text(size=14, colour ="black")) +
  theme(legend.position="bottom")


  

mythemeIIIb2 <- theme_bw() +
  theme(plot.margin=unit(c(0.05,0.05,0.3,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(plot.title = element_blank()) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0))

mythemeIIIc <- theme_bw() +
  theme(plot.margin=unit(c(0.05,1.5,0.3,0.05),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(axis.title.x = element_blank())  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0)) +
  theme(strip.text.y = element_text(size = 14, colour = "black", angle = 270))
