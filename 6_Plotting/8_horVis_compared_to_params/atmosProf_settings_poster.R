guide = guide_colourbar(title=NULL,barwidth=0.4,barheight=3.5, label.theme = element_text(size =8,angle=0))

mytheme1 <- theme_bw() + 
  theme(plot.margin=unit(c(0.25,2,-0.5,0.28),"cm")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.55)) +
  theme(axis.text.x = element_blank()) +
  theme(axis.ticks.x = element_blank()) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_text(size=8, colour = "black", vjust= 0.3)) +
  theme(axis.text.y = element_text(size=8, colour = "black")) +
  theme(plot.title = element_text(lineheight=3, color="black", size=10, vjust=1,face="bold"))

mytheme2 <- theme_bw() + 
  theme(plot.margin=unit(c(0.1,0.1,0.1,0.4),"cm")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.text.y = element_text(size=8, colour = "black")) +
  theme(axis.title.x = element_blank()) +
  theme(axis.title.y = element_text(size=8, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_blank()) +
  theme(axis.ticks.x = element_blank())
#  theme(axis.text = element_text(size=8, colour = "black")) +
#  theme(axis.title.x = element_text(size=8, colour = "black",vjust=0))

mytheme3 <- theme_bw() + 
  theme(plot.margin=unit(c(-0.5,0.35,0.2,0.4),"cm")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.text = element_text(size=8, colour = "black")) +
  theme(axis.title.x = element_text(size=8, colour = "black",vjust=0)) +
  theme(axis.title.y = element_text(size=8, colour = "black", vjust=0.3))