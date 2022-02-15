# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:55:49 2021

@author: DFM
"""
# 03/11/21 changé alpha 0.1->0.2
# augmenté taille police axes 10-25
#211031 ajout s=si[o:i] pour la taille du point
#211108 vitesse dééfilement plus élevée et ligne gris au lieu de silver
#allongement séquence finale fixe
#211114 ajouté   fig.autofmt_xdate()-réduit taille fonte date 25->20
#211115 réglé pb affichage dates (1 date /2)
#211117 changé ordre, commece par vue fixe.
#211208 ajoute les magnitudes référence et les tailles de point & grid
#211217 ajout heure dernier évènement auto - str( sismof.iloc[-1,2])
#211219 changement position repère ajout ligne verticale date éruption
#211224 changement round à 2 chiffres
#courbe energy(#220103 ajout modifications sur video)
#220115 ajout ligne fin d'éruption 
#faire alpha bas et 10-15 plus gros events
#220115 ajout ligne fin éruption
#220122 orientation verticale texte

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.mlab as ml
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import os
import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as md
# from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#from scipy.interpolate import griddata
counter=0
counter2=0
counter3=0
counter4=0
counter5=0


#loc=('D:/Users/Public/Documents/Python Scripts/Python_2020/La Palma/NRJ')
#o"s.chdir(loc)


#lire le fichier etopo
data = pd.read_csv("lapalma.csv", delimiter=',')
#filtrer les données selon lat long
dataf=data.loc[(data.iloc[:,0]>-18.1) &(data.iloc[:,0]<-17.65) & (data.iloc[:,1]>28.4) & (data.iloc[:,1]<28.95)]
#création des 3 coordonnées
long=dataf.iloc[:,0]
lat=dataf.iloc[:,1]
alt=dataf.iloc[:,2]
#interpolation long/lat
#interpolation long/lat
#Generate a regular grid to interpolate the data.

xi = np.linspace(min(long), max(long),num=200)
yi = np.linspace(min(lat), max(lat),num=200)
LONG, LAT = np.meshgrid(xi, yi)



ALT = griddata((long, lat), alt, (LONG, LAT),method='linear')

#Lire de fichier sismique

#FWF() c'est la solution pour importer direftement le fichier de l'IGN
sismo = pd.read_fwf('catalogo28.csv')#,col_list)
#indique la magnitude min prise en compte
magmax=round(0,1)
#magnitude max choisie
#filtre selon lat long et ne prend pas les Z=NaN et selon une magnitude magmax
sismof=sismo.loc[(sismo.iloc[:,4]>-18.2) &(sismo.iloc[:,4]<-17.6) & (sismo.iloc[:,3]>28.4) & (sismo.iloc[:,3]<29)&(sismo.iloc[:,6].notnull())&(sismo.iloc[:,8]>=magmax)]



#print(sismof)
sismof=sismof.reset_index(drop=True)

X=sismof.iloc[:,4]
Y=sismof.iloc[:,3]
Z=sismof.iloc[:,6]*-1000
#Annee=sismo[:,8]
#Mois=sismo[:,9]
#jour=sismo[:,10]
mag=sismof.iloc[:,8]
Date=sismof.iloc[:,1]
hour=sismof.iloc[:,2]


#calcul taille point selon nrj séisme (MJ)
#si=np.exp(2.303*(5.24+1.44*(mag)))/1000000000000
si=10**((5.24+1.44*(mag)))/1000000000000
#Calcul des énergies pour mag 5,4,3 pour représentation taille points
si5=10**((5.24+1.44*(5)))/1000000000000
si4=10**((5.24+1.44*(4)))/1000000000000
si3=10**((5.24+1.44*(3)))/1000000000000


maxy=0 #- pour déterminer la valeur max de l'abscisse

for i in range(len(X)):
    maxy=maxy+np.cumsum(si[i])

C1=[datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in Date]
#extrait les dates sous format
#le choix de la fenetre de date se fait via le catalogue 
minDate=min(C1)
maxDate=max(C1)



#récupère l'année
an = pd.DatetimeIndex(Date).year
print(an)
#long1,lat1 = np.meshgrid(long,lat)


#extraction des dates sous format
x_values = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in Date]
#print(x_values)
#création figure
#year=datetime.strftime(x_values, " %Y")
#print(year)#
#
cmap = plt.cm.get_cmap("jet")
color = [cmap(float(i)/(len(X))) for i in range(len(X))]


#A REVOIR
alph=[]
for i in range(len(X)):
  if mag[i]>=4:
        alph.append(0.5)
    
  else :
        alph.append(0.2)
    



#CALCUL DE LA VARIATION - OBJECTIF MOYENNE MOBILE

# For Date in Date :
    
#     DayEnergy=
#fixed view
fig = plt.figure(figsize=(30,8),dpi=300)
for i in range(1200):
  
  ax = fig.add_subplot(111)
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  
  ax.scatter(x_values,np.cumsum(si),s=si*750,color=color,edgecolor='face',alpha=alph[i])
  ax.plot(x_values,np.cumsum(si),c='grey')
  ax.scatter(x_values[4],70,s=si5*750,color='r',alpha=1)
  ax.scatter(x_values[4],60,s=si4*750,color='r',alpha=1)
  ax.scatter(x_values[4],50,s=si3*750,color='r',alpha=1)
  #ajoute les magnitudes
  ax.text(x_values[0],70, 'Mag 5', size=24, ha='center', va='center')
  ax.text(x_values[0],60, 'Mag 4', size=24, ha='center', va='center')
  ax.text(x_values[0],50, 'Mag 3', size=24, ha='center', va='center')
 #place le text au niveau de la date de l'éruption 
  ax.text(x_values[1450],50, 'Eruption', size=24, ha='center', va='center',rotation=90)
  ax.text(x_values[8900],50, 'End of \nEruption', size=24, ha='center', va='center',rotation=90)
#boite avec dernière valeur (len(X)-1) de l'nrj
  ax.text(x_values[(len(X)-1)],maxy-5, np.round(maxy,2), bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
  #indique la valeur max sur le graph, ajout boite bbox, format 2 chiffres après la virgule
  plt.xticks(rotation=90)
  ax.set_xlabel("Date", fontsize=20)
  ax.set_ylabel("Cumulative Earthquake Energy (TJ - $10^{12}$ J)", fontsize=25)
  ax.legend(("Plot by @dfmorvan1 \n - Data from @IGNSpain", "Dot area proportional to NRJ\n Last event "+str(sismof.iloc[-1,2])+" UTC"),loc='upper left',fontsize=15)

  plt.axvline( x_values[1247], color = "green", label = "Eruption",linestyle='dotted', linewidth=5) # Plotting a single vertical line
  plt.axvline( x_values[8577], color = "red", label = "End of \nEruption",linestyle='dotted', linewidth=5)
  ax.xaxis.set_major_locator(md.DayLocator(interval=2))
# set formatter
  ax.xaxis.set_major_formatter(md.DateFormatter('%d-%m-%Y'))
  #ticks à gauche
  ax.yaxis.set_ticks_position('right')
  ax.grid(which='both')

  ax.grid(which='minor', alpha=0.5, linestyle='--')
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  
  
  # ax.view_init(azim = i,elev =0)
  # ax.set_xlim3d(min(long),max(long))
  ax.set_ylim(0,maxy+3)
  # ax.set_zlim3d(min(Z),max(alt)+500)
  # ax.set_xlabel("longitude", fontsize=20)
  # ax.set_ylabel("latitude", fontsize=20)
  # ax.set_zlabel("depth-  m", fontsize=20)  

  fig.suptitle("La Palma earthquake cumulative energy  - \n"+str(Date[0])+" to "+str(Date[len(X)-1]), fontsize=25)
#    fig.suptitle("La Palma earthquake cumulative energy (MJ) - \n"+str(Date[0])+" to "+str(Date[len(X)-1]), fontsize=25)

  index=counter+counter2+counter3+counter4+counter5
  print(index)
  fig.savefig("sortienrj"+str(format(index, '04d'))+".png")
  counter5=counter5+1
  plt.clf()
plt.close('all')




fig = plt.figure(figsize=(30,8),dpi=300)
for i in sismof.index:
  
        
  ax = fig.add_subplot(111)
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  #ax.scatter(Date[0:i],si[0:i],s=100,c=color[0:i],alpha=0.5)
  ax.scatter(x_values[0:i],np.cumsum(si[0:i]),s=si[0:i]*750,c=color[0:i],edgecolor='face',alpha=alph[i])
  ax.plot(x_values[0:i],np.cumsum(si[0:i]),c='grey')
  plt.xticks(rotation=90)
  ax.set_ylim(0,maxy+3)
  ax.set_xlabel("Date", fontsize=20)
  ax.set_ylabel("Cumulative Earthquake Energy (TJ - $10^{12}$J)", fontsize=25)
  ax.scatter(x_values[1],70,s=si5*750,color='r',alpha=1)
  ax.scatter(x_values[1],60,s=si4*750,color='r',alpha=1)
  ax.scatter(x_values[1],50,s=si3*750,color='r',alpha=1)
  #ajoute les magnitudes
  ax.text(x_values[0],70, 'Mag 5', size=24, ha='center', va='center')
  ax.text(x_values[0],60, 'Mag 4', size=24, ha='center', va='center')
  ax.text(x_values[0],50, 'Mag 3', size=24, ha='center', va='center')

  ax.text(x_values[1455],50, 'Eruption', size=24, ha='center', va='center')

  ax.text(x_values[(len(X)-1)],maxy-5, np.round(np.cumsum(si[0:2])), bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
  
  ax.xaxis.set_major_locator(md.DayLocator(interval=2))
# set formatter
  ax.xaxis.set_major_formatter(md.DateFormatter('%d-%m-%Y'))

  # ax.xaxis.set_major_locator(DayLocator())
  # #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
  # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
  ax.yaxis.set_ticks_position('right')
  ax.grid(which='both')

  ax.grid(which='minor', alpha=0.2, linestyle='--')
  
  
  #fig.autofmt_xdate()
  
  #cbar=plt.colorbar(I,ax,shrink=0.5,extend='both')
  
  
  
  
  
  
  
  #ax.vline(Date = 19/10/2021, color = "green", label = "Eruption") # Plotting a single vertical line
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  # Create empty plot with blank marker containing the extra label
  # ax.legend( ("Plot by dfm \n Size of dot proportional to NRJ Data from @IGNSpain"),loc='upper left')
  ax.legend(("Plot by @dfmorvan1 \n - Data from @IGNSpain", "Dot area proportional to NRJ\n Last event "+str(sismof.iloc[-1,2])+" UTC"),loc='upper left',fontsize=15)
  
  # ax.view_init(azim = i,elev =0)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  # ax.set_zlim3d(min(Z),max(alt)+500)
  # ax.set_xlabel("longitude", fontsize=20)
  # ax.set_ylabel("latitude", fontsize=20)
  # ax.set_zlabel("depth-  m", fontsize=20)  

  fig.suptitle("La Palma earthquake cumulative energy - \n"+str(Date[0])+" to "+str(Date[i]) , fontsize=25)
  index=counter+counter2+counter3+counter4+counter5
  print(index)
  fig.savefig("sortienrj"+str(format(index, '04d'))+".png")
  counter5=counter5+1
  plt.clf()
plt.close('all')












os.system("ffmpeg -r 160 -i sortienrj%04d.png -vcodec mpeg4 LaPalma_cumulative_EQ-NRJ_220103.mp4")
