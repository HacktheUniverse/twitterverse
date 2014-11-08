#! /usr/bin/env python

## 2014.11.08 - lia@space.mit.edu
## Plot the orbits

import sys
args = sys.argv

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

###############################################

t, x, y, vx, vy  = [], [], [], [], []

def add_row( row_array ):
	t.append( row_array[0] )
	x.append( row_array[1] )
	y.append( row_array[2] )
	vx.append( row_array[3] )
	vy.append( row_array[4] )
	return

def read_orbit_file( filename ):
	ff = open(filename, 'r')
	
	for line in ff:
		ltemp    = line.strip().split('\t')
		rowvals  = []
		for i in range(5):
			rowvals.append( float(ltemp[i]) )
		add_row( rowvals )
	
	ff.close()
	return (t, x, y, vx, vy)

def make_3d_coords( x, y, theta ):
	xnew = x * np.cos(theta)
	ynew = y * np.cos(theta)
	znew = x * np.sin(theta)
	return (xnew, ynew, znew)

def plot_orbit( x, y, z, **kwargs ):
	fig  = plt.figure()
	ax   = fig.add_subplot(111, projection='3d')
	ax.plot( x, y, z, **kwargs )
	fig.show()
	return

def save_orbit( x, y, z, filename ):
	ff = open( filename + '.3d', 'w' )
	for i in range(len(x)):
		ff.write( np.str(x[i]) + "," +
				  np.str(y[i]) + "," +
				  np.str(z[i]) + "\n" )
	ff.close()
	return

################################################
## Run the code

def run_plot():
	
	try:
		filename = args[1]
		read_orbit_file( filename )
	
	except:
		print "ERROR: Check input arguments"
		return
		
	theta   = np.random.uniform() * 2.0*np.pi
	(xp, yp, zp) = make_3d_coords( np.array(x), np.array(y), theta )
	plot_orbit( xp, yp, zp, ls='-', lw=2 )
	
	save_orbit( xp, yp, zp, filename )
	return

run_plot()



