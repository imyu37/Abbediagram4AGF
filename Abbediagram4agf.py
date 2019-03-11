#coding:utf-8
# tested with python 3.7.0
'''
1.名称：Abbediagram4agf.py
2.目的：Plot the Abbe diagram of the input glass catalog
3.参考资料：
  3.1 https://stackoverflow.com/questions/11537374/matplotlib-basemap-popup-box#new-answer
  3.2 https://stackoverflow.com/users/741316/pelson
4.作者：YONG(wanyong_37@hotmail.com)
5.版本：
  v0.3 20190311 
  1. 以plt.text()的方式加入legend

  v0.2 20190303 
  1. 输入玻璃目录的名称
  2. 阿贝图中显示玻璃目录名
'''

from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6)) # facecolor='white'
ax = plt.axes()
# adds grid
plt.grid(True)
plt.locator_params(nbins=20) # grid size

#file = open('cdgm.agf','r')
ngc = input('Please input the name of the glass catalog existed: ')
file = open(ngc+'.agf','r')
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

# Add "legend" with plt.text
plt.text(99, 2.06, ' Color : Status   ',color='black',fontsize='x-large', fontweight='bold')
plt.text(97, 2.02, ' blue    : Standard  ',color='blue',ha='left')
plt.text(97, 1.98, ' green  : Preferred ',color='green',ha='left')
plt.text(97, 1.94, ' red      : Obsolete  ', color='red',ha='left')
plt.text(97, 1.90, ' violet  : Special   ', color='violet',ha='left')
plt.text(97, 1.86, ' black  : Melt      ', color='black',ha='left')

file.close()

ax.set_xlim(100,5)  # extend of abbe number(Vd)
ax.set_ylim(1.4, 2.1) # extend of index(Nd)
ax.set_title('Abbe diagram of '+ngc+' glasses')
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
