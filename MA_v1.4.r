library(WindR)
w.start(showmenu=F)

MA_SHORT=0;
MA_LONG=0;
LMA_SHORT=0;
LMA_LONG=0;

hold=0;       #-1  空仓     0   没有持仓     1   多仓
cost=0;
profit=0;
log=list("");
plot_point=0;

MA_SHORTNUM = 20;
MA_LONGNUM = 60;

case = 7;

while(case == 7){
	if(case == 1){
		print('T1703');
		codes='T1703.CFE';
		begintime= "2016-11-11";
		endtime= "2017-02-11";
	}

	if(case == 2){
		print('T1706');
		codes='T1706.CFE';
		begintime= "2017-02-11";
		endtime= "2017-05-11";
	}

	if(case == 3){
		print('T1709');
		codes='T1709.CFE';
		begintime= "2017-05-11";
		endtime= "2017-08-11";
	}

	if(case == 4){
		print('T1712');
		codes='T1712.CFE';
		begintime= "2017-08-11";
		endtime= "2017-11-11";
	}
	
	if(case == 5){
		print('T1803');
		codes='T1803.CFE';
		begintime= "2017-11-11";
		endtime= "2018-02-11";
	}
	
	if(case == 6){
		print('T1806');
		codes='T1806.CFE';
		begintime= "2018-02-11";
		endtime= "2018-05-11";
	}
	if(case == 7){
		print('T1809');
		codes='T1809.CFE';
		begintime= "2018-05-11";
		endtime= "2018-08-11";
	}
	if(case == 8){
		print('T1812');
		codes='T1812.CFE';
		begintime= "2018-08-11";
		endtime= "2018-11-11";
	}
	if(case == 9){
		print('T1903');
		codes='T1903.CFE';
		begintime= "2018-11-11";
		endtime= "2018-12-10";
	}
	fields='close';
	bardata= w.wsi(codes,fields,begintime,endtime,'BarSize=5');

	for(i in MA_LONGNUM:(length(bardata$Data$close))){
		bartime=unlist(strsplit(bardata$Data$DATETIME[i]<-as.character(bardata$Data$DATETIME[i]),split=" "))
		
		#忽略最后一个bar
		if(TRUE){
			if(bartime[2]=="15:15:00" | bartime[2]=="11:30:00"){
				next;
			}
		}
		
		j = i-MA_SHORTNUM+1;
		LMA_SHORT = MA_SHORT;
		MA_SHORT=0;
		while(j <= i){
			MA_SHORT =MA_SHORT+bardata$Data$close[j];
			j=j+1;
		}
		MA_SHORT=MA_SHORT/MA_SHORTNUM;
		
		j = i-MA_LONGNUM+1;
		LMA_LONG = MA_LONG;
		MA_LONG=0;
		while(j <= i){
			MA_LONG =MA_LONG+bardata$Data$close[j];
			j=j+1;
		}
		MA_LONG=MA_LONG/MA_LONGNUM;
		
		#买开
		if(LMA_LONG > LMA_SHORT && MA_LONG <= MA_SHORT){
			if(hold == -1){
				profit = profit+(-bardata$Data$close[i]+cost);
				plot_point=c(plot_point,profit*50*0.0002*1000000);
				cost = 0;
				hold =0;
				log=list(bardata$Data$DATETIME[i],"close_sell@",-bardata$Data$close[i],"profit=",profit, "LMA_LONG", LMA_LONG,"LMA_SHORT",LMA_SHORT,"MA_LONG",MA_LONG,"MA_SHORT",MA_SHORT );
				write.table(log, file = "C:/Users/Administrator/Desktop/Rstrategy/1.txt", append=TRUE,row.name=F,quote=F)
			}
			if(hold == 0){
				cost = -(bardata$Data$close[i]);
				hold =1;
				log=list(bardata$Data$DATETIME[i],"buy_open@",cost,"LMA_LONG", LMA_LONG,"LMA_SHORT",LMA_SHORT,"MA_LONG",MA_LONG,"MA_SHORT",MA_SHORT);	
				write.table(log, file = "C:/Users/Administrator/Desktop/Rstrategy/1.txt", append=TRUE,row.name=F,quote=F)
			}
			
		}
		#卖开
		else if(LMA_LONG < LMA_SHORT && MA_LONG >= MA_SHORT){
			if(hold == 1){
				profit = profit+(bardata$Data$close[i]+cost);
				plot_point=c(plot_point,profit*50*0.0002*1000000);
				cost = 0;
				hold =0;
				log=list(bardata$Data$DATETIME[i],"close_buy@",-bardata$Data$close[i],"profit=",profit, "LMA_LONG", LMA_LONG,"LMA_SHORT",LMA_SHORT,"MA_LONG",MA_LONG,"MA_SHORT",MA_SHORT );
				write.table(log, file = "C:/Users/Administrator/Desktop/Rstrategy/1.txt", append=TRUE,row.name=F,quote=F)
			}
			if(hold == 0){
				cost = bardata$Data$close[i];
				hold =-1;
				log=list(bardata$Data$DATETIME[i],"sell_open@",cost,"LMA_LONG", LMA_LONG,"LMA_SHORT",LMA_SHORT,"MA_LONG",MA_LONG,"MA_SHORT",MA_SHORT);	
				write.table(log, file = "C:/Users/Administrator/Desktop/Rstrategy/1.txt", append=TRUE,row.name=F,quote=F)
			}
			
		}
	}
	
	if(hold == 1){
		profit = profit+(bardata$Data$close[i-1]+cost);
		plot_point=c(plot_point,profit*50*0.0002*1000000);
		#print(plot_point)
		cost = 0;
		hold =0;
		log=list(bardata$Data$DATETIME[i],"force_close_buy@",bardata$Data$close[i-1],"profit=",profit);
		write.table(log, file = "C:/Users/Administrator/Desktop/Rstrategy/1.txt", append=TRUE,row.name=F,quote=F)
	}
	if(hold == -1){
		profit = profit+(-bardata$Data$close[i-1]+cost);
		plot_point=c(plot_point,profit*50*0.0002*1000000);
		#print(plot_point)
		cost = 0;
		hold =0;
		log=list(bardata$Data$DATETIME[i-1],"force_close_sell@",-bardata$Data$close[i-1],"profit=",profit);
		write.table(log, file = "C:/Users/Administrator/Desktop/Rstrategy/1.txt", append=TRUE,row.name=F,quote=F)
	}
	case = case + 1;
}


sample=1;
for(i in 2:length(plot_point))
	sample=c(sample,i);
plot(plot_point~sample,pch=15,col="DarkTurquoise",ylab="profit",main="Profit")#pch表示散点用什么形状表示，col表示颜色，ylim表示Y轴范围，ylab表示Y轴标题，main表示图片标题
lines(plot_point,col="RosyBrown",lty=1)#lty=1表示用实线连起来