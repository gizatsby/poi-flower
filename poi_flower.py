'''
Poi Flower Visualization (1.0.0)
7 Feb. 2018

Leonardo Cisija
nardocisija@gmail.com

Please include this header when using/modifying.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

### Set Values ###
# input
freq = int(input('Enter the spinning frequency (integer, negative is anti-spin) '))    # how many times the poi is spun for each cycle (not entirely float-friendly yet, hence the 'int')
r1 = float(input('Enter the length of the inner radius (the "arm") '))
r2 = float(input('Enter the length of the outer radius (the "poi") '))
loops = abs(float(input('Enter the number of loops before clearing the trail ')))      # this will also control the number of frames drawn. 1 loop = 100 frames
showCircles = input('Show circles? (Y/N) ').lower()                                    # whether or not the guiding circles are shown

# account for variations in showCircles input. non-yes strings are interpreted as 'no'
if showCircles in ['y','yes']:
    showCircles = 'yes'
else:
    showCircles = 'no'

t = np.linspace(0,2,100*abs(freq))    # generates 100*|freq| evenly-spaced ts from 0 to 2 (for parametric functions)

### Define Functions ###
# Convert Polar (r,theta) to Cartesian x
def CartX(X,Y):
    CartX = Y * np.cos(X)
    return CartX

# Convert Polar (r,theta) to Cartesian y
def CartY(X,Y):
    CartY = Y * np.sin(X)
    return CartY

# Position of Poi
def X1(X):
    X1 = CartX(X*np.pi - 0.5*np.pi, r1) + CartX(X*freq*np.pi - 0.5*np.pi, r2)
    return X1

def Y1(X):
    Y1 = CartY(X*np.pi - 0.5*np.pi, r1) + CartY(X*freq*np.pi - 0.5*np.pi, r2)
    return Y1

# Position of Hands
def X2(X):
    X2 = CartX(X*np.pi - 0.5*np.pi, r1)
    return X2

def Y2(X):
    Y2 = CartY(X*np.pi - 0.5*np.pi, r1)
    return Y2

### Things to Animate ###
# Position of Poi (Line)
def PoiX(X):
    PoiX = X1(X),X2(X)
    return PoiX

def PoiY(X):
    PoiY = Y1(X),Y2(X)
    return PoiY

# Position of Arm (Line)
def ArmX(X):
    ArmX = 0,X2(X)
    return ArmX

def ArmY(X):
    ArmY = 0,Y2(X)
    return ArmY

# Poi Trail
def TrailX(X):
    TrailX = CartX(np.pi*(X-0.5),r1) + CartX(np.pi*(X*freq - 0.5),r2)
    return TrailX

def TrailY(X):
    TrailY = CartY(np.pi*(X-0.5),r1) + CartY(np.pi*(X*freq - 0.5),r2)
    return TrailY

# Circles
circle1 = plt.Circle((0,0), r1, color='k', fill=False, ls='--')         # parameters are black, no fill, dashed line
circle2 = plt.Circle((X2(0),Y2(0)), r2, color='b', fill=False, ls='--') # parameters are blue, no fill, dashed line

### Set Up Animation ###
fig, ax1 = plt.subplots(figsize=(6,6))    # 6x6 window
ax1.axis([-0.25*(r1+r2)-r1-r2,0.25*(r1+r2)+r1+r2,-0.25*(r1+r2)-r1-r2,0.25*(r1+r2)+r1+r2])    # looks like a mess but the scale of plot is just the combined radius + 25%

poi, = ax1.plot(PoiX(0), PoiY(0), 'bo-')                    # parameters are blue, circle markers, solid line
arm, = ax1.plot(ArmX(0), ArmY(0), 'ko-')                    # parameters are black, circle markers, solid line
trail, = ax1.plot(TrailX(0), TrailY(0), 'bo', alpha=0.5)    # parameters are blue, circle markers, and opacity is 0.5

ax1.text(0, r1+r2, 'frequency = {0}\ninner radius = {1}\nouter radius = {2}\nloops = {3}\nshow circles = {4}'.format(freq,r1,r2,loops,showCircles))    # text box display

if showCircles == 'yes':
    ax1.add_artist(circle1)
    ax1.add_artist(circle2)

    def init():        # initial frame of animation
        poi.set_data(PoiX(0),PoiY(0))
        arm.set_data(ArmX(0),ArmY(0))
        trail.set_data(TrailX(0),TrailY(0))
        circle2.center = (X2(0),Y2(0))
        return poi, arm, trail, circle2

    def animate(i):        # animation rule
        poi.set_data(PoiX(i/50),PoiY(i/50))
        arm.set_data(ArmX(i/50),ArmY(i/50))
        trail.set_data(TrailX(t[:int((i)*abs(freq))]), TrailY(t[:int((i)*abs(freq))]))
        circle2.center = (X2(i/50),Y2(i/50))
        return poi, arm, trail, circle2
else:
    def init():        # initial frame of animation
        poi.set_data(PoiX(0),PoiY(0))
        arm.set_data(ArmX(0),ArmY(0))
        trail.set_data(TrailX(0),TrailY(0))
        return poi, arm, trail,

    def animate(i):        # animation rule
        poi.set_data(PoiX(i/50),PoiY(i/50))
        arm.set_data(ArmX(i/50),ArmY(i/50))
        trail.set_data(TrailX(t[:int(i*abs(freq))]), TrailY(t[:int(i*abs(freq))]))
        return poi, arm, trail,


### Animate and Show ###
ani = animation.FuncAnimation(fig, animate, int(100*loops), init_func=init, interval=25, blit=True)
plt.show()
