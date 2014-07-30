#coding:utf-8
'''
read Abbe number and refractive index in a .agf file,and plot the Abbe diagram
'''

from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt

file = open('schott.agf','r')
#file = open('cdgm.agf','r')
gname = list() #glass name
vd = list() #Abbe number
nd = list() #index of d line
lines = file.readlines()
for line in lines:
	tmp = line.split()
	if tmp[0] == 'NM':
		gname.append(tmp[1])
		vd.append(float(tmp[4]))
		nd.append(float(tmp[5]))

file.close()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, axisbg='#FFFFFF')
ax.plot(nd,vd,'o',color='#33FF00')
ax.set_xlim(90,5)
ax.set_ylim(1.4, 2.05)
ax.set_xlabel('Abbe number $V$ ')
ax.set_ylabel('Refractive Index $n_d$ ($\lambda_d$=587.6nm) ')

# Turn on for lableing every data point with glassname
for i, txt in enumerate(gname):
	ax.annotate(txt, (nd[i],vd[i]))

cursor = Cursor(ax, useblit=True, color='red', linewidth=2 )

plt.show()
