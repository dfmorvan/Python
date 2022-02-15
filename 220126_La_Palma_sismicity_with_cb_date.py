# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:55:21 2017

#○AJOUTER TRANSIITON VUE WEST, ANGLE 15°


#211007 added energy formula to size
#211012 modify script to show EQ by magnitude
#211012 resserré image (modif filtre lat long)-added trick for dates in title
#try bbox_inches='tight',pad_inches = 0 to remove margins with pad_inches = 0
#  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   
#changé les alpha des surfaces
#211102 ajout contour sur surface Z
#211102 ajout -15 sur dernière vue, modif sur 720 au lieu de 360, alphaold=0.2 au lieu de 0.1
#211105 correction position entre 2 séquences i+180
#211109 ajout filtre profondeur
#211111 correction filtre profondeur (valeur filtre positive)
#211204 correction formule énergie - modification angle de vue mobile dernière rotation
#211210 ajout transition entre vue west et vue avec angle de la rotation, changement rythme oescillation rotation finale
#211210 modification axes, correstion filtre profondeur sismoold, ajout prof min et prof max
#211222 ajout seismes référence, resserement topographie ajout minlat maxlat
#211213 test colorbar
#211230  x_values = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in Date]
# color=mdates.date2num(x_values)
# loc = mdates.AutoDateLocator()
#  cb.ax.xaxis.set_major_locator(loc)
#  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
#il faut un mappble - ici base -  pour que la colorbar se retrouve automatiquement
#AJOUTER AXES CENTRES
(#220114 ajout tight layout)
 #220115 rationalisation déclaration colormaps ds les boucles
 #FOR DAY IN DATE
@author: morvan
"""
#import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.mlab as ml
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import os
import datetime
from mpl_toolkits.axes_grid1 import make_axes_locatable


import matplotlib.dates as mdates
#from scipy.interpolate import griddata
counter=0
counter2=0
counter3=0
counter4=0
counter5=0
counter6=0
counter7=0
counter8=0


#REGLAGES
alphaold=0.2

PROFmin=0
PROFmax=45

magmax=round(0,1)

#les n plus gros évènements
n=20
#multiplicateur surface event
multi=200

alph=0.5


#long : durée de la première vue, nombre de vues    
long1=50

#définition des colormpas
cmt=cm.terrain
cmcb='seismic'



#lire le fichier etopo
data = pd.read_csv("lapalma.csv", delimiter=',')

#D2fini les limites pour la carte et les seismes
minLong=-18
maxLong=-17.7
minLat=28.45
maxLat=28.85

#filtrer les données selon lat long

dataf=data.loc[(data.iloc[:,0]>minLong) &(data.iloc[:,0]<maxLong) & (data.iloc[:,1]>minLat) & (data.iloc[:,1]<maxLat)]
#211105 ajout profondeur limitée à 200 m
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
sismoold=pd.read_fwf('catalogo2000.csv')
#catalogue sismos depuis 2000-31/08/2021
#indique la magnitude min prise en compte

#critère de profondeur en km





#magnitude max choisie
sismof=sismo.loc[(sismo.iloc[:,4]>minLong) &(sismo.iloc[:,4]<maxLong) & (sismo.iloc[:,3]>minLat) & (sismo.iloc[:,3]<maxLat)&(sismo.iloc[:,6].notnull())&(sismo.iloc[:,6]>PROFmin)&(sismo.iloc[:,6]<PROFmax)&(sismo.iloc[:,8]>=magmax)]
#filtre selon lat long et ne prend pas les Z=NaN et selon une magnitude magmax

sismofold=sismoold.loc[(sismoold.iloc[:,4]>minLong) &(sismoold.iloc[:,4]<maxLong) & (sismoold.iloc[:,3]>minLat) & (sismoold.iloc[:,3]<maxLat)&(sismoold.iloc[:,6].notnull())&(sismoold.iloc[:,6]>PROFmin)&(sismoold.iloc[:,6]<PROFmax)]
#filtre sur la palma, pas de filtre sur la mag enlève les profondeurs nulles

#print(sismof)
sismof=sismof.reset_index(drop=True)
sismofold=sismofold.reset_index(drop=True)

X=sismof.iloc[:,4]
Y=sismof.iloc[:,3]
Z=sismof.iloc[:,6]*-1000
#Annee=sismo[:,8]
#Mois=sismo[:,9]
#jour=sismo[:,10]
mag=sismof.iloc[:,8]
Date=sismof.iloc[:,1]
hour=sismof.iloc[:,2]

Xold=sismofold.iloc[:,4]
Yold=sismofold.iloc[:,3]
Zold=sismofold.iloc[:,6]*-1000
#Annee=sismo[:,8]
#Mois=sismo[:,9]
#jour=sismo[:,10]
magold=sismofold.iloc[:,8]
Dateold=sismofold.iloc[:,1]
hourold=sismofold.iloc[:,2]


#tri des valeurs selon la magnitude - objectif : montrer les valeurs les plus fortes et le reste sous forme d'enveloppe
sortmag=sismof.sort_values(by="Mag.",ascending=False)



first=sortmag.head(n)
print(first)#calcul taille point selon nrj séisme
Xfirst=first.iloc[:,4]
Yfirst=first.iloc[:,3]
Zfirst=first.iloc[:,6]*-1000
magfirst=first.iloc[:,8]
Datefirst=first.iloc[:,1]


si=10**((5.24+1.44*(mag)))/1000000000000
siold=10**((5.24+1.44*(magold)))/1000000000000
sifirst=10**((5.24+1.44*(magfirst)))/1000000000000

#taille des seismes de référence
#ajustement de la taille


si5=10**((5.24+1.44*(5)))/1000000000000*multi
si4=10**((5.24+1.44*(4)))/1000000000000*multi
si3=10**((5.24+1.44*(3)))/1000000000000*multi
si2=10**((5.24+1.44*(2)))/1000000000000*multi

# C1=[datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in Date]
#extrait les dates sous format
#le choix de la fenetre de date se fait via le catalogue 
# minDate=min(C1)
# maxDate=max(C1)



#récupère l'année
date1 = pd.DatetimeIndex(Date).date
print(date1)
#long1,lat1 = np.meshgrid(long,lat)

#charge le filtre pour year and month
# minyear=2017
# maxyear=2020

#extraction des dates sous format
x_values = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in Date]
color=mdates.date2num(x_values)

#refait la grille de couleur pour les valeurs de first - sinon les tailles sont différentes
x_valuesf = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in Datefirst]
colorf=mdates.date2num(x_valuesf)
#print(x_values)
#création figure
#year=datetime.strftime(x_values, " %Y")
#print(year)#
#
# cmap = plt.cm.get_cmap("jet")
# color = [cmap(float(i)/(len(X))) for i in range(len(X))]


#reprise de la normalisation couleur
  #vue de dessus
  #fig = plt.figure()
#fig = plt.figure(figsize=(12,12),dpi=300)

# for i in range(len(X)):

#taille des points - augmentation par rapport à 750 précédemmet car baisse intensité sismique
sioldsize=siold*multi
sisize=si*multi
sifirstsize=sifirst*multi

fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(1):
# for date1 in date  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  #déclaration de la source de la cmap
  #permet d'avoir la colorbar en alpha = 1
  #on devrait faire une seule image avec la base et ensuite passer à la vue de dessus.....
  
  base=ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=1)
  # ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)

  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.3,
                       linewidth=0, antialiased=True)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  
  
  #reférence seismes
  # ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  # ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  # ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  # ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  # ax.text(-17.99,28.8,-5000, " MAG 5")
  # ax.text(-17.99,28.8 ,-10000, " MAG 4")
  # ax.text(-17.99,28.8 ,-15000, " MAG 3")
  # ax.text(-17.99,28.8 ,-20000, " MAG 2")

  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  #shrink joue sur la longueur de la cb et sur son épaisseur 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  
  
  ax.view_init(azim = 270,elev =90)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  #ax.set_zlabel("depth-  m", fontsize=20)  
  ax.zaxis.set_ticks([])
  
  #permet de réduire les marges au minimum
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0) 


  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n MAG >= " +str(format(magmax)), fontsize=25)
  # plt.subplots_adjust(wspace=0.5, hspace=0.5,left=0.1,top=1,right=0.9,bottom=0.8)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  print(index)
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter=counter+1
 
  plt.clf()
plt.close('all')

#image fixe pour finir le plan, VUE DE DESSUS
fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(long1):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  #déclaration de la source de la cmap
  #permet d'avoir la colorbar en alpha = 1
  #on devrait faire une seule image avec la base et ensuite passer à la vue de dessus.....
  
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  # ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)

  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.3,
                       linewidth=0, antialiased=True)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  
  
  #reférence seismes
  # ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  # ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  # ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  # ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  # ax.text(-17.99,28.8,-5000, " MAG 5")
  # ax.text(-17.99,28.8 ,-10000, " MAG 4")
  # ax.text(-17.99,28.8 ,-15000, " MAG 3")
  # ax.text(-17.99,28.8 ,-20000, " MAG 2")

  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  #shrink joue sur la longueur de la cb et sur son épaisseur 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  
  
  ax.view_init(azim = 270,elev =90)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  #ax.set_zlabel("depth-  m", fontsize=20)  
  ax.zaxis.set_ticks([])
  
  #permet de réduire les marges au minimum
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0) 


  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n MAG >= " +str(format(magmax)), fontsize=25)
  # plt.subplots_adjust(wspace=0.5, hspace=0.5,left=0.1,top=1,right=0.9,bottom=0.8)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  print(index)
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter2=counter2+1
 
  plt.clf()
plt.close('all')


#TRansition entre vue de dessus et vue de côté

fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(90):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.3,
                       linewidth=0, antialiased=True)
  cset = ax.contour(LONG, LAT, ALT, zdir='z', offset=min(Z)-1000, cmap=cm.terrain)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  #reférence seismes
  # ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  # ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  # ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  # ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  # ax.text(-17.99,28.8,-5000, " MAG 5")
  # ax.text(-17.99,28.8 ,-10000, " MAG 4")
  # ax.text(-17.99,28.8 ,-15000, " MAG 3")
  # ax.text(-17.99,28.8 ,-20000, " MAG 2")
  
  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
  
  
  
  
  ax.view_init(azim = 270,elev =90-i)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  # ax.set_zlabel("depth-  m", fontsize=20)
  ax.xaxis.set_ticks([])
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   

  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n view from the South MAG >= " +str(format(magmax)), fontsize=25)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  # print(str(format(index))+" /" +str(format(2*len(X)+400+720)))
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter3=counter3+1
  print(index)
  plt.clf()
plt.close('all')

#TRansition entre vue de côté az 270 et az 180

fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(90):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.3,
                       linewidth=0, antialiased=True)
  cset = ax.contour(LONG, LAT, ALT, zdir='z', offset=min(Z)-1000, cmap=cm.terrain)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  
  #reférence seismes
  ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  ax.text(-17.99,28.8,-5000, " MAG 5")
  ax.text(-17.99,28.8 ,-10000, " MAG 4")
  ax.text(-17.99,28.8 ,-15000, " MAG 3")
  ax.text(-17.99,28.8 ,-20000, " MAG 2")
  
  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
  
  
  
  ax.view_init(azim = 270-i,elev =0)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  #ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  ax.set_zlabel("depth-  m", fontsize=20)
  ax.xaxis.set_ticks([])
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   

  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n  MAG >= " +str(format(magmax)), fontsize=25)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  # print(str(format(index))+" /" +str(format(2*len(X)+400+720)))
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter4=counter4+1
  print(index)
  plt.clf()
plt.close('all')


#vue de côté depuis l'OUEST

#plan fixe pourla dernière image


fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(long1):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.3,
                       linewidth=0, antialiased=True)
  cset = ax.contour(LONG, LAT, ALT, zdir='z', offset=min(Z)-1000, cmap=cm.terrain)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  #reférence seismes
  ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  ax.text(-17.99,28.8,-5000, " MAG 5")
  ax.text(-17.99,28.8 ,-10000, " MAG 4")
  ax.text(-17.99,28.8 ,-15000, " MAG 3")
  ax.text(-17.99,28.8 ,-20000, " MAG 2")
  
  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
  
  
  
  ax.view_init(azim = 180,elev =0)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  #ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  ax.set_zlabel("depth-  m", fontsize=20)
  ax.xaxis.set_ticks([])
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   

  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n view from the West MAG >= " +str(format(magmax)), fontsize=25)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  # print(str(format(index))+" /" +str(format(2*len(X)+400+720)))
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter5=counter5+1
  print(index)
  plt.clf()
plt.close('all')

fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(20):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.3,
                       linewidth=0, antialiased=True)
  cset = ax.contour(LONG, LAT, ALT, zdir='z', offset=min(Z)-1000, cmap=cm.terrain)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  #reférence seismes
  ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  ax.text(-17.99,28.8,-5000, " MAG 5")
  ax.text(-17.99,28.8 ,-10000, " MAG 4")
  ax.text(-17.99,28.8 ,-15000, " MAG 3")
  ax.text(-17.99,28.8 ,-20000, " MAG 2")
  
  #transition entre vue west et vue avec angle 20°
  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
  
  
  
  ax.view_init(azim = 180,elev =0+i)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  #ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  ax.set_zlabel("depth-  m", fontsize=20)
  ax.xaxis.set_ticks([])
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   

  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n view from the West MAG >= " +str(format(magmax)), fontsize=25)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  # print(str(format(index))+" /" +str(format(2*len(X)+400+720)))
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter6=counter6+1
  print(index)
  plt.clf()
plt.close('all')





  
#rotation
fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(720):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=0.5,
                       linewidth=0, antialiased=True)
  cset = ax.contour(LONG, LAT, ALT, zdir='z', offset=min(Z)-1000, cmap=cm.terrain)
  #ax.contour3D(LONG,LAT,ALT,  cmap=cm.terrain)
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  #reférence seismes
  ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  ax.text(-17.99,28.8,-5000, " MAG 5")
  ax.text(-17.99,28.8 ,-10000, " MAG 4")
  ax.text(-17.99,28.8 ,-15000, " MAG 3")
  ax.text(-17.99,28.8 ,-20000, " MAG 2")
  
  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
  
  
  
  
  ax.view_init(azim = i+180,elev =20)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  ax.set_zlabel("depth-  m", fontsize=20)
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   
  

  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n MAG >= " +str(format(magmax)), fontsize=25)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7
  # print(str(format(index))+" /" +str(format(2*len(X)+400+720)))
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter7=counter7+1
  print(index)
  plt.clf()
plt.close('all')


fig = plt.figure(figsize=(12,12),dpi=300)
for i in range(720):
  
  ax = fig.add_subplot(111, projection='3d')
  #cmap = plt.cm.get_cmap("jet")
    #fig = plt.figure()
    #plt.figure(i)
   #set color equal to a variable
  
  # ax.scatter(X[0:i],Y[0:i],Z[0:i],c=color[0:i],cmap='jet')
  ax.scatter(X,Y,Z,s=sisize,c=color,cmap=cmcb,alpha=alph)
  #'ancien catalogue avant 01/01/2000-31/09/2021
  ax.scatter(Xold,Yold,Zold,s=sioldsize,color='k',alpha=alphaold)
  ax.plot_surface(LONG,LAT,ALT,rstride=1,cstride=1,cmap=cmt,alpha=.8,
                       linewidth=0, antialiased=True)
  ax.scatter(Xfirst,Yfirst,Zfirst,s=sifirstsize,c=colorf,cmap=cmcb,alpha=1)
  cset = ax.contour(LONG, LAT, ALT, zdir='z', offset=min(Z)-1000, cmap=cm.terrain)

  
  ax.scatter(-17.866833,28.616268,1000,s=400,c='magenta',marker='^') 
  ax.text(-17.866833,28.616268 ,1200, "  TajoGaite")
  #plt.colorbar () 
    # ax.plot_surface(long1,lat1,alt)
  #ax.scatter(long,lat,alt,marker='.')

  #plt.axis([-22.9, -22.15, 63.75, 63.95])
  #reférence seismes
  ax.scatter(-17.95,28.8,-5000,s=si5,c='red')
  ax.scatter(-17.95,28.8,-10000,s=si4,c='red')
  ax.scatter(-17.95,28.8,-15000,s=si3,c='red')
  ax.scatter(-17.95,28.8,-20000,s=si2,c='red')

  
  
  ax.text(-17.99,28.8,-5000, " MAG 5")
  ax.text(-17.99,28.8 ,-10000, " MAG 4")
  ax.text(-17.99,28.8 ,-15000, " MAG 3")
  ax.text(-17.99,28.8 ,-20000, " MAG 2")
  
  cb=plt.colorbar (mappable=base,ax=ax,orientation="horizontal",fraction=0.1,pad=0,shrink=0.5) 
  cb.set_label('Date')
  loc = mdates.AutoDateLocator()
  cb.ax.xaxis.set_major_locator(loc)
  cb.ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
  
  
  ax.view_init(azim = i+180,elev =10*np.sin(i*0.01))#0.05-0.02 (bien)
  # ax.set_xlim3d(min(long),max(long))
  # ax.set_ylim3d(min(lat),max(lat))
  ax.set_zlim3d(min(Z),max(alt)+500)
  ax.set_xlabel("longitude", fontsize=20)
  ax.set_ylabel("latitude", fontsize=20)
  ax.set_zlabel("depth-  m", fontsize=20)
  #maintenir l'axe des x en bas
  ax.set_axisbelow(True)
  
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   

  
  fig.suptitle("La Palma earthquake activity - "+str(Date[0])+" to "+str(Date[len(X)-1])+"\n MAG >= " +str(format(magmax)), fontsize=25)
  index=counter+counter2+counter3+counter4+counter5+counter6+counter7+counter8
  # print(str(format(index))+" /" +str(format(2*len(X)+400+720)))
  fig.savefig("sortie"+str(format(index, '04d'))+".png")
  counter8=counter8+1
  print(index)
  plt.clf()
plt.close('all')
  #ajout videoend() 
#animation.save(movie1.mp4)  changé de 10 à 20 après -r
os.system("ffmpeg -r 40 -i sortie%04d.png -vcodec mpeg4 movieLaPalma220117-2-seismic-MAG0-20.mp4")



