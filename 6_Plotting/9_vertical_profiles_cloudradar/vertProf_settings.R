guide2 = guide_colourbar(title=NULL,barwidth=1,barheight=9, label.theme = element_text(size = 14,angle=0))

mytheme1 <- theme_bw() +
  theme(plot.margin=unit(c(1.5,0.1,0.8,0.57),"cm")) +
  theme(axis.text.y = element_text(size=14, colour = "black")) +
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0))  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5))  

mytheme2 <- theme_bw() +
  theme(plot.margin=unit(c(1.5,1,0.8,0),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0))  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank()) +
  theme(plot.title = element_blank())
#  theme(plot.title = element_text(lineheight=3, color="black", size=18, vjust=3))

mytheme3 <- theme_bw() +
  theme(plot.margin=unit(c(1.5,2.8,0.8,-1),"cm")) +
  theme(axis.text.y = element_blank()) +
  theme(axis.title.y = element_blank())+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0))  +  
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.ticks.y = element_blank())

mytheme4 <- theme_bw() + 
  theme(plot.margin=unit(c(0.1,0,0.53,0.57),"cm")) +
  theme(panel.grid.major=element_line(color="lightgrey",size=0.5)) +
  theme(axis.text.y = element_text(size=14, colour = "black")) +
  theme(axis.title.y = element_text(size=14, colour = "black",vjust= 0.3))+
  theme(axis.text.x = element_text(size=14, colour = "black")) +
  theme(axis.title.x = element_text(size=14, colour = "black",vjust=0))