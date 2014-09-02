#coding:utf-8
'''
Read a .AGF file,and plot the Abbe diagram
'''

from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6)) # facecolor='white'
ax = plt.axes()
# adds grid
plt.grid(True)
plt.locator_params(nbins=20) # grid size

#file = open('misc.agf','r')
file = open('schott.agf','r')
#file = open('cdgm.agf','r')
points_with_annotation = list() # data point with annotation
lines = file.readlines()

# Facecolor indicate the Status as same as Zemax indicated:Status is 0 for Standard,
# 1 for Preferred, 2 for Obsolete, 3 for Special, and 4 for Melt.
fc ={0:"black",1:"green",2:"red",3:"blue",4:"yellow"}

# add some lines to distinguish different sort of glasses accorint to SCHOTT abbe diagram
l = plt.axvline(x=62, ymax=0.323,linewidth=1, color='k')
l = plt.axvline(x=55, ymax=0.356,linewidth=1, color='k')
l = plt.axvline(x=50, ymin=0.17, linewidth=1, color='k')
l = plt.axvline(x=45, ymin=0.204,ymax=0.246,linewidth=1, color='k')
l = plt.axvline(x=43, ymin=0.264,ymax=0.432,linewidth=1, color='k')
l = plt.axvline(x=40, ymin=0.236,ymax=0.293,linewidth=1, color='k')
l = plt.axvline(x=35, ymin=0.307,ymax=0.379,linewidth=1, color='k')

l = plt.axhline(xmax=0.4, y=1.49, linewidth=1, color='k')
l = plt.axhline(xmin=0.21,xmax=0.474, y=1.54, linewidth=1, color='k')
l = plt.axhline(xmin=0.474,xmax=0.526, y=1.60, linewidth=1, color='k')
l = plt.axhline(xmin=0.263,xmax=0.4, y=1.626, linewidth=1, color='k')
l = plt.axhline(xmin=0.707, y=1.65, linewidth=1, color='k')
l = plt.axhline(xmin=0.674,xmax=0.728, y=1.74, linewidth=1, color='k')
l = plt.axhline(xmin=0.526,xmax=0.763, y=1.80, linewidth=1, color='k')

plt.plot([68, 55],[1.49, 1.60],  'k-', lw=1)
plt.plot([62, 50],[1.626, 1.6654], 'k-', lw=1)
plt.plot([62, 55],[1.49, 1.50],  'k-', lw=1)
plt.plot([55, 50],[1.54, 1.55],  'k-', lw=1)
plt.plot([55, 40],[1.50, 1.565],  'k-', lw=1)
plt.plot([50,36],[1.6654,1.74], 'k-', lw=1)
plt.plot([50,45],[1.55,1.572], 'k-', lw=1)
plt.plot([45,40],[1.572,1.605], 'k-', lw=1)
plt.plot([40,35],[1.605,1.665], 'k-', lw=1)
plt.plot([40,35],[1.565,1.615], 'k-', lw=1)
plt.plot([35,25],[1.615,1.77], 'k-', lw=1)
plt.plot([35,26.1],[1.665,1.821], 'k-', lw=1)
plt.plot([25,5],[1.77,2.418], 'k-', lw=1)
plt.plot([26.1,5],[1.821,2.55], 'k-', lw=1)

for line in lines:
	tmp = line.split()
#	vtmp = float(tmp[4])
#	ntmp = float(tmp[5])
	if tmp[0] == 'NM':
		point, = plt.plot(float(tmp[5]), float(tmp[4]), 'o', markersize=10)
#		point, = plt.plot(float(tmp[5]), float(tmp[4]), 'o', markersize=10, markerfacecolor=fc[float(tmp[7])])

		annotation = ax.annotate("%s $nd$=%f $vd$=%f" % (tmp[1],float(tmp[4]), float(tmp[5])),
			xy=(float(tmp[5]), float(tmp[4])), xycoords='data',
			xytext=(float(tmp[5])-2.5, float(tmp[4])), textcoords='data',
			horizontalalignment="left",
			bbox=dict(boxstyle="round", facecolor="w",
			edgecolor="0.5", alpha=0.9)
			)
# by default, disable the annotation visibility
		annotation.set_visible(False)
		points_with_annotation.append([point, annotation])

file.close()

ax.set_xlim(100,5)  # extend of abbe number(Vd)
ax.set_ylim(1.4, 2.1) # extend of index(Nd)
ax.set_title('Abbe diagram')
ax.set_xlabel('Abbe number $V$ ')
ax.set_ylabel('Refractive Index $n_d$ ($\lambda_d$=587.6nm) ')

# Thanks for  pelson(https://stackoverflow.com/users/741316/pelson) provide the  mathod in stackoverflow.com
# https://stackoverflow.com/questions/11537374/matplotlib-basemap-popup-box#new-answer
def on_move(event):
    visibility_changed = False
    for point, annotation in points_with_annotation:
        should_be_visible = (point.contains(event)[0] == True)

        if should_be_visible != annotation.get_visible():
            visibility_changed = True
            annotation.set_visible(should_be_visible)

    if visibility_changed:
        plt.draw()

on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.show()
