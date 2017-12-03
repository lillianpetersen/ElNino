# Lillian Petersen
# Science Fair Project 2015

from pylab import *
import csv
from math import sqrt
from sys import exit
from numpy import polyfit,array
#cd \Users\lilli_000\Documents\Science_Fair_2015_El_Nino\Science_Fair_Code

###############################################
# Make Functions
###############################################
def C2Flist(c):  #converts C to F
    f=[]
    for k in range(len(c)):
        f.append(9./5.*c[k]+32.)
    return f
    
def AvgList(x):   #function to average a list
    xAvg=0.
    for k in range(len(x)):
        xAvg=xAvg+x[k]
    xAvg=xAvg/(k+1)
    return xAvg 
    
def stdDev(x):   #function to compute standard deviation
    xAvg=AvgList(x)
    xdev=0.
    for k in range(len(x)):
        xdev=xdev+(x[k]-xAvg)**2
    xdev=xdev/(k+1)
    xdev=sqrt(xdev)
    return xdev
    
def corr(x,y):   
    # function to find the correlation of two lists
    xAvg=AvgList(x)
    yAvg=AvgList(y)
    rxy=0.
    n=min(len(x),len(y))
    for k in range(n):
        rxy=rxy+(x[k]-xAvg)*(y[k]-yAvg)
    rxy=rxy/(k+1)
    stdDevx=stdDev(x)
    stdDevy=stdDev(y)
    rxy=rxy/(stdDevx*stdDevy)
    return rxy

###############################################
# El Nino Functions
###############################################   
def smooth3(x):   #Average 3 months in a row
    y=[(x[0]+x[1])/2.]
    for k in range(1,len(x)-1):
        y.append((x[k-1]+x[k]+x[k+1])/3.)
    y.append((x[k+1]+x[k])/2.)
    return y

def ninoClass(x):   #function to classify El Ninos and La Ninas
    y=0 #N
    if min(x)>=.5:
        y=.5 #WE
    if min(x)>=1:
        y=1 #ME
    if min(x)>=1.5:
        y=1.5 #SE
    if max(x)<=-.5:
        y=-.5 #WL
    if max(x)<=-1:
        y=-1 #ML
    if max(x)<=-1.5:
        y=-1.5 #SL
    return y

###############################################
# Read in Enso Data
###############################################
fileID=open('Data/detrend.nino34.csv',"rb")
reader=csv.reader(fileID)

a=csv.reader
j=0
nino=[]
yearN=[]
monthN=[]
dateN=[]
for row in reader:
    if j==0:
        header=row
    else:
        nino.append(float(row[4]))
        yearN.append(float(row[0]))
        monthN.append(float(row[1]))
    j=j+1
    
for k in range(len(yearN)):
    dateN.append(yearN[k]+(monthN[k]-.50)/12.0)

# Take 3 Month Average
ninoSmooth=smooth3(nino)

#Round El Nino to nearest tenth  
ninoSmoothRnd=[]
for k in range(len(nino)):
    ninoSmoothRnd.append(round(ninoSmooth[k],1))
    
#El Nino classification by month   
nino3=[]
for k in range(len(nino)):
    tmp=ninoClass(ninoSmoothRnd[k:k+3])
    nino3.append(tmp)
    
#El Nino classification by year 
ninoYr=[]
ninoYrDate=[]
im=6
for iy in range(1950,2014):
    maxN=max(nino3[im:im+12])
    minN=min(nino3[im:im+12])
    if maxN>=abs(minN):
        ninoYr.append(maxN)
    else:
        ninoYr.append(minN)
    ninoYrDate.append(iy)
    im=im+12
    
ninoArray=zeros([65,12])  # years,months

for k in range(len(nino)):
    iy=yearN[k]-1950
    im=monthN[k]-1
    ninoArray[iy,im]=nino[k]

###############################################
# Initialize Variables
###############################################
#cityList=['Albuquerque','Akron_Colorado','Boulder_Colorado',
#    'New_York_L','Washington_State',
#    'Los_Alamos','Cincinnati',
#    'Santa_Fe','Seattle_Washington',
#    'Colorado','Colorado_Springs','Florida']

#cityList=['South_California','North_Dakota','Louisiana','Nebraska','California','Oregon',
#        'South_Carolina','New_York_C']

cityList=['Los_Alamos']

for icity in range(len(cityList)):
    city=cityList[icity]
    j=0
    Tmax=[]
    Tmin=[]
    snowd=[]
    snow=[]
    precip=[]
    date=[]
    year=[]
    month=[]
    day=[]
    TmaxAvgM=[0.]
    TminAvgM=[0.]
    snowdAvgM=[]
    snowAvgM=[0.]
    precipAvgM=[0.]
    dateAvgM=[]
    yearAvgM=[]
    monthAvgM=[]
#    clf()

###############################################
# Read in Weather Data
###############################################
    filename='Data/'+city+'.csv'
    fileID=open(filename,"rb")
    reader=csv.reader(fileID)
    a=csv.reader
    
    for row in reader:
        if j==0:
            header=row
        else:
            tmp=row[1]
            ytmp=float(tmp[0:4])
            mtmp=float(tmp[4:6])
            if ytmp==2014 and mtmp==11:
                break
            if ytmp>=1950:
                Tmax.append(float(row[5])/10.)
                Tmin.append(float(row[6])/10.)
                snowd.append(float(row[3])/2.54)
                snow.append(float(row[4])/10./2.54) # cm
                precip.append(float(row[2])/100./2.54) # cm
                tmp=row[1]
                year.append(float(tmp[0:4]))
                month.append(float(tmp[4:6]))
                day.append(float(tmp[6:8]))
        j=j+1
    ###############################################
    # Replace Bad Data
    ###############################################
    for k in range(len(year)):
        date.append(year[k]+(month[k]-1)/12.0+(day[k]-1)/365)
        if Tmax[k]<-90:
            Tmax[k]=Tmax[k-1]
        if Tmin[k]<-90:
            Tmin[k]=Tmin[k-1]
        if precip[k]<-1:
            precip[k]=0
        if snow[k]<-90:
            snow[k]=0
    
    ###############################################
    # Make Monthly Averages
    ###############################################       
    dateAvgM.append(year[0]+(month[0]-.5)/12)
    n=0  #day counter
    im=0 #month counter     
    for k in range(len(year)):  #loop over days
        if month[k]!=month[k-1] and k>0: #test for new month
            TmaxAvgM[im]=TmaxAvgM[im]/n
            TminAvgM[im]=TminAvgM[im]/n
            n=0
            TmaxAvgM.append(0.)
            TminAvgM.append(0.)
            precipAvgM.append(0.)
            snowAvgM.append(0.)
            dateAvgM.append(year[k]+(month[k]-.5)/12)
            im=im+1
        TmaxAvgM[im]=TmaxAvgM[im]+Tmax[k]
        TminAvgM[im]=TminAvgM[im]+Tmin[k]
        precipAvgM[im]=precipAvgM[im]+precip[k]
        snowAvgM[im]=snowAvgM[im]+snow[k]
        n=n+1
    TmaxAvgM[im]=TmaxAvgM[im]/n
    TminAvgM[im]=TminAvgM[im]/n
    
    ###############################################
    # Compute Correlations
    ############################################### 
    tmpcorr=corr(nino,precipAvgM)
    print city,tmpcorr
    
    ###############################################
    # Convert C to F
    ###############################################    
    Tmaxf=C2Flist(Tmax)
    Tminf=C2Flist(Tmin)
    TmaxAvgMf=C2Flist(TmaxAvgM)
    TminAvgMf=C2Flist(TminAvgM)
    
    ###############################################
    # Group Data For El Nino
    ###############################################
    nc=[-1.5,-1,-.5,0,.5,1,1.5] #El Nino category
    ncName=['SL','ML','WL','N','WE','ME','SE']
    snowNC=zeros(7) 
    yearsNC=zeros(7)
    TmaxNC=zeros(7) 
    TminNC=zeros(7) 
    precipNC=zeros(7)
    counterNC=zeros(7) 
    iN=[]
    #assign El Nino Index
    for k in range(len(ninoYr)):
        if ninoYr[k]==1.5:  # SE
            iN.append(6)
        elif ninoYr[k]==1:  # ME
            iN.append(5)
        elif ninoYr[k]==.5:  # WE
            iN.append(4)
        elif ninoYr[k]==0:  # N
            iN.append(3)
        elif ninoYr[k]==-.5:  # WL
            iN.append(2)
        elif ninoYr[k]==-1:  # ML
            iN.append(1)
        elif ninoYr[k]==-1.5:  # SL
            iN.append(0)
    
    for k in range(len(ninoYr)):
        yearsNC[iN[k]]+=1
    
    dateAvgM.append(year[0]+(month[0]-.5)/12)
    n=0  #day counter
    iy=0 #year counter 
    snowSumY=zeros(64)
    dateY=zeros(64)
    dateY[0]=1950   
    for k in range(200,len(Tmax)):  #loop over days
        if month[k]!=month[k-1] and month[k]==7: #test for july 1
          #  print k, iy, year[k]-1, snowSumY[iy]
            if year[k]==2014:
                break
            iy=int(year[k]-1950)
            dateY[iy]=year[k]
            if year[k]-iy!=1950:
                print 'invalid data ',city, iy, year[k]
               # exit
        snowNC[iN[iy]]+=snow[k]
        snowSumY[iy]+=snow[k]
        if month[k]==12 or month[k]==1 or month[k]==2:
            counterNC[iN[iy]]+=1
            TmaxNC[iN[iy]]+=Tmax[k]
            TminNC[iN[iy]]+=Tmin[k]
            precipNC[iN[iy]]+=precip[k]
    TmaxNC=TmaxNC/counterNC
    TminNC=TminNC/counterNC
    precipNC=precipNC/yearsNC 
    snowNC=snowNC/yearsNC
    TmaxNCf=C2Flist(TmaxNC)
    TminNCf=C2Flist(TminNC)     
    
    ###############################################
    # Plot Results
    ###############################################
    
    elNinoMonthStr=['January','February','March','April',
    'May','June','July','August','September','October',
    'November','December']
    
    for k in range(len(elNinoMonthStr)): 
        m,b=polyfit(ninoArray[0:64,k],snowSumY,1)
        x=array([-2.5,2.5])
        yfit=m*x+b
        
        Xnino=ninoArray[0:64,k]
        SnowSumYFit=m*Xnino+b
        error=snowSumY-SnowSumYFit
        stdDevError=stdDev(error)
        print stdDevError
        yfitTop=m*x+b+stdDevError
        yfitBot=m*x+b-stdDevError
        
        corrNinoSnow=corr(ninoArray[:,k],snowSumY)
        corrNinoSnow=round(corrNinoSnow,2)
        slope=round(m,2)
        
        plot(ninoArray[0:64,k],snowSumY, '*',x,yfit,x,yfitTop,'--g',
        x,yfitBot,'--g')
        xlabel('El Nino Index, Previous '+elNinoMonthStr[k])
        ylabel('Total Snowfall for following winter, inches')
        legend(['Yearly Snowfall','Best Fit Line','Line +/- std dev'],loc='upper left')
        title(city+ ': ' + 'Correlation =' + str(corrNinoSnow)+ ', '
        +'Slope ='+ str(slope))
        yt=.5
        text(-.2,yt,'neutral')
        text(-1.5,yt,'La Nina')
        text(1,yt,'El Nino')
        grid(True)
        axis([-2.5,2.5,0,max(snowSumY)])
        savefig('plots/'+city+'_month'+str(k)+
        '_El_Nino_Fit_Correlation_Fit_Line_stdDev.png')
        show()
        clf()
    exit() 
    m,b=polyfit(nc,snowNC,1)
    x=array([-1.5,1.5])
    yfit=m*x+b
    slope=round(m,2)
    
    corrNcSnow=corr(nc,snowNC)
    print city,corrNcSnow
    corrNcSnow=round(corrNcSnow,2)
    
    plot(nc,snowNC,'*-',x,yfit)
    xlabel('El Nino Category for every year, July-June')
    ylabel('Average Snowfall, inches, December-Feburary')
    title(city+' Snowfall, Slope ='+ str(slope)
    +', Correlation='+str(corrNcSnow))
    yt=min(snowNC)
    text(-.1,yt,'neutral')
    text(-1.1,yt,'La Nina')
    text(.8,yt,'El Nino')
    legend(['Average Snowfall','Best Fit Line'],'upper left')
    grid(True)
    savefig('plots/'+city+'_snowNC.png')
    show()
    clf()
    

    
    m,b=polyfit(nc,precipNC,1)
    x=array([-1.5,1.5])
    yfit=m*x+b
    slope=round(m,2)
    
    corrNcPrecip=corr(nc,precipNC)
    print city,corrNcPrecip
    corrNcPrecip=round(corrNcPrecip,2)
    
    plot(nc,precipNC,'*-',x,yfit)
    xlabel('El Nino Category for every year, July-June')
    ylabel('Average Precipitation, inches, December-Feburary')
    title(city+' Precipitation, Slope ='+ str(slope)
    +', Correlation='+str(corrNcPrecip))
    yt=min(precipNC)
    text(-.1,yt,'neutral')
    text(-1.1,yt,'La Nina')
    text(.8,yt,'El Nino')
    legend(['Average Precipitation','Best Fit Line'],'upper left')
    grid(True)
    savefig('plots/'+city+'_precipNC.png')
    show()
    clf()
    
     
    
    m,b=polyfit(nc,TmaxNCf,1)
    x=array([-1.5,1.5])
    yfit=m*x+b
    slope=round(m,2)
    
    corrNcTmax=corr(nc,TmaxNCf)
    print city,corrNcTmax
    corrNcTmax=round(corrNcTmax,2)
    
    plot(nc,TmaxNCf,'b*-',x,yfit,'g-')
    xlabel('El Nino Category for every year, July-June')
    ylabel('Average Maximum Temperature, F, December-Feburary')
    title(city+' Max Temperature, Slope ='
    + str(slope)+', Correlation ='+ str(corrNcTmax)+'0')
    yt=min(TmaxNCf)
    text(-.1,yt,'neutral')
    text(-1.1,yt,'La Nina')
    text(.8,yt,'El Nino')
    legend(['Average Daily Max Temperature',
    'Best Fit Line'],'upper right')
    grid(True)
    savefig('plots/'+city+'_TmaxNCf.png')
    show()
    clf()
    
     
    
    m,b=polyfit(nc,TminNCf,1)
    x=array([-1.5,1.5])
    yfit=m*x+b
    slope=round(m,2)
    
    corrNcTmin=corr(nc,TminNCf)
    print city,corrNcTmin
    corrNcTmin=round(corrNcTmin,2)
    
    plot(nc,TminNCf,'b*-',x,yfit,'g-')
    xlabel('El Nino Category for every year, July-June')
    ylabel('Average Minimum Temperature, F, December-Feburary')
    title(city+' Min Temperature, Slope ='
    + str(slope)+', Correlation ='+ str(corrNcTmin))
    yt=min(TminNCf)
    text(-.1,yt,'neutral')
    text(-1.1,yt,'La Nina')
    text(.8,yt,'El Nino')
    legend(['Average Daily min Temperature',
    'Best Fit Line'],'upper right')
    grid(True)
    savefig('plots/'+city+'_TminNCf.png')
    show()
    clf()
    
exit()
m,b=polyfit(nc,precipNC,1)
x=array([-1.5,1.5])
yfit=m*x+b
slope=round(m,2)

plot(nc,precipNC,'b*-',x,yfit, 'g-')
xlabel('El Nino Category for every year, July-June')
ylabel('Average Precipatation, inches, December-Feburary')
title(city+', Linear Fit Slope ='+ str(slope))
text(-.1,1.62,'neutral')
text(-1.1,1.62,'La Nina')
text(.8,1.62,'El Nino')
legend(['Average Precipatation','Best Fit Line'],'upper left')
grid(True)
savefig('plots/'+city+'_precipNC.png')
show()
clf()

    

plot(dateY,snowSumY)
xlabel('Time, Year')
ylabel('Yearly Snowfall, Inches')
title('Yearly Snowfall, July to June')
grid(True)
axis([1950,2013,0,160])
savefig('plots/Yearly_Snowfall.png')
show()

plot(dateAvgM[0:778],snowAvgM)
xlabel('Time, Year')
ylabel('Monthly Snowfall, Inches')
title('Monthly Snowfall')
grid(True)
axis([1950,2015,0,70])
savefig('plots/Monthly_Snowfall.png')
show()

plot(dateN,ninoSmooth)
xlabel('Time, Year')
ylabel('El Nino Index')
text(1951,2.1,'El Nino')
text(1951,-1.9,'La Nina')
title('El Nino Data')
grid(True)
axis([1950,2015,-2,2.5])
savefig('plots/El_Nino_Data.png')
show()

plot(date,snow)
xlabel('Time, Year')
ylabel('Daily Snowfall, Inches')
title('Daily Snowfall')
grid(True)
axis([1950,2015,0,25])
savefig('plots/Daily_Snowfall.png')
show()
