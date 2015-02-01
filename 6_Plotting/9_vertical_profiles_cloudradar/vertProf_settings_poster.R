guide2 = guide_colourbar(title=NULL,barwidth=0.4,barheight=4, label.theme = element_text(size = 8,angle=0))

mytheme1 <- theme_bw() +
  theme(plot.margin=unit(c(0.6,0,0.1,0.5),"cm")) +
  theme(axis.text.y = element_text(size=8, colour = "black")) +
  theme(axis.title.y = element_text(size=8, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_text(size=8, colour = "black")) +
  theme(axis.title.x = element_text(size=8, colour = "black",vjust=0))  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.3))  

mytheme2 <- theme_bw() +
  theme(plot.margin=unit(c(0.6,0.8,0.1,-0.1),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=8, colour = "black")) +
  theme(axis.title.x = element_text(size=8, colour = "black",vjust=0))  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.3)) +
  theme(axis.ticks.y = element_blank()) +
  theme(plot.title = element_blank())
#  theme(plot.title = element_text(lineheight=3, color="black", size=12, vjust=1.5))

mytheme3 <- theme_bw() +
  theme(plot.margin=unit(c(0.6,1.8,0.1,-1),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=8, colour = "black")) +
  theme(axis.title.x = element_text(size=8, colour = "black",vjust=0))  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.3)) +
  theme(axis.ticks.y = element_blank())

mytheme4 <- theme_bw() + 
  theme(plot.margin=unit(c(0.1,0,0.2,0.57),"cm")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.3)) +
  theme(axis.text.y = element_text(size=8, colour = "black")) +
  theme(axis.title.y = element_text(size=8, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_text(size=8, colour = "black")) +
  theme(axis.title.x = element_text(size=8, colour = "black",vjust=0))

