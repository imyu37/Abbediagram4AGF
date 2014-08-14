#coding:utf-8
'''
Read a .AGF file,and plot the Abbe diagram
'''

from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6))
ax = plt.axes()

#file = open('misc.agf','r')
file = open('schott.agf','r')
#file = open('cdgm.agf','r')
points_with_annotation = list() # data point with annotation
lines = file.readlines()

# Facecolor indicate the Status as same as Zemax indicated:Status is 0 for Standard,
# 1 for Preferred, 2 for Obsolete, 3 for Special, and 4 for Melt.
fc ={0:"black",1:"green",2:"red",3:"blue",4:"yellow"}

for line in lines:
	tmp = line.split()
#	vtmp = float(tmp[4])
#	ntmp = float(tmp[5])
	if tmp[0] == 'NM':
		point, = plt.plot(float(tmp[5]), float(tmp[4]), 'o', markersize=10, markerfacecolor=fc[float(tmp[7])])
#		plt.legend(('black', 'green', 'red', 'blue', 'yellow'),loc=2)

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

ax.set_xlim(100,5)
ax.set_ylim(1.4, 2.05)
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
