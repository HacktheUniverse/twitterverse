#! /usr/bin/env python

## 2014.11.08 - lia@space.mit.edu
## Modified to accept system input, automate orbit calculation

import sys 
args = sys.argv

print args

TSTEP        = 0.01
#ACCURACY     = 1.e-6

###################################################
## ORIGINAL CODE (where did we get this?)

import math
import rk4      # rk4.py contains 4-th order Runge-Kutta routines

G_m1_plus_m2 = 4 * math.pi**2

step_using_y = False

def equations(trv):
    t = trv[0]
    x = trv[1]
    y = trv[2]
    vx = trv[3]
    vy = trv[4]
    r = math.sqrt(x**2 + y**2)
    ax = - G_m1_plus_m2 * x / r**3
    ay = - G_m1_plus_m2 * y / r**3
    flow = [ 1, vx, vy, ax, ay ]
    if step_using_y:            # change independent variable from t to y
        for i in range(5):
            flow[i] /= vy
    return flow

def print_data(values):
    names = [ "t", "x", "y", "v_x", "v_y" ]
    units = [ "yr", "AU", "AU", "AU/yr", "AU/yr" ]
    for i in range (5):
        print " " + names[i] + "\t= " + str(values[i]) + " " + units[i]

def write_data(file, values):
    for value in values:
        file.write(str(value) + "\t")
    file.write("\n")

def integrate(trv, dt, t_max, file_name, accuracy=1e-6, adaptive=False):
    file = open(file_name, "w")
    print "\n Initial conditions:"
    print_data(trv)
    print " Integrating with fixed step size ..."
    step = 0
    dt_min = dt
    dt_max = dt
    while True:
        write_data(file, trv)
        y_save = trv[2]
        global step_using_y     # so next line does not create a local variable
        step_using_y = False
        if adaptive:
            dt = rk4.RK4_adaptive_step(trv, dt, equations, accuracy)
            dt_min = min(dt, dt_min)
            dt_max = max(dt, dt_max)
        else:
            rk4.RK4_step(trv, dt, equations)
        t, x, y, vx, vy = (trv[i] for i in range(5))
        if x > 0 and y * y_save < 0:
            step_using_y = True
            rk4.RK4_step(trv, -y, equations)
            write_data(file, trv)
            break
        if t > 10 * t_max:
            print " t too big, quitting ..."
            break
        step += 1
    file.close()
    print " Number of fixed steps = ", step
    if adaptive:
        print " Minimum dt = ", dt_min
        print " Maximum dt = ", dt_max
    print_data(trv)
    print " Trajectory data in", file_name

###############################################
##  Run the code

def run_orbit():

	try:
		r_aphelion   = float(args[1])
		eccentricity = float(args[2])
		filename     = args[3]
		print r_aphelion, eccentricity, filename
	except:
		print "ERROR: Check arguments"
		return
	
	a = r_aphelion / (1 + eccentricity)
	T = a**1.5
	vy0 = math.sqrt(G_m1_plus_m2 * (2 / r_aphelion - 1 / a))
	print " Semimajor axis a = ", a, " AU"
	print " Period T = ", T, " yr"
	print " v_y(0) = ", vy0, " AU/yr"
	dt  = TSTEP
	
	trv = [ 0, r_aphelion, 0, 0, vy0 ]
	integrate(trv, TSTEP, T, filename )
	#trv = [ 0, r_aphelion, 0, 0, vy0 ]
	#integrate(trv, TSTEP, T, filename, accuracy=ACCURACY)

	return
	
run_orbit()
