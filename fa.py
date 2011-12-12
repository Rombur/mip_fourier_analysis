#! /usr/bin/env python
#----------------------------------------------------------------------------#
# Python code
# Author: Bruno Turcksin
# Date: 2011-11-11 17:48:03.487349
#----------------------------------------------------------------------------#

import numpy as np
import QUADRATURE
import DOF_HANDLER
import TRANSPORT
import utils

grid_x = np.array([0.,0.5,1.,0.,0.4,1.,0.,0.5,1.])
grid_y = np.array([0.,0.,0.,0.5,0.4,0.5,1.,1.,1.])
nx_cells = 2
ny_cells = 2
#grid_x = np.array([0.,1.,0.,1.])
#grid_y = np.array([0.,0.,1.,1.])
#nx_cells = 1
#ny_cells = 1
N = 10
solver_type = "SI"
condition_number = False
sn = 4
# CANNOT BE DIFFERENT THAT 0. Otherwise problem when D and M have to be
# multiplied
L_max = 0
galerkin = False
fe_type ="PWLD"  
prec = False
filename = "transport"
# First element of cross section is the total cross section. The rest is the
# scattering cross section
cross_section = np.array([1.,1.])

if grid_x.shape!=grid_y.shape :
  utils.abort("size of grid_x is not equal to size grid_y.")

quad = QUADRATURE.QUADRATURE(sn,L_max,galerkin)
dof_handler = DOF_HANDLER.DOF_HANDLER(nx_cells,ny_cells,grid_x,grid_y,fe_type)
transport = TRANSPORT.TRANSPORT(dof_handler,quad,cross_section,solver_type,
    prec)

lambda_x = np.linspace(0,2*np.pi,N)
lambda_y = np.linspace(0,2*np.pi,N)
rho = np.zeros((N,N))

if condition_number==True :
  kappa = np.zeros((N,N))

for i in xrange(0,N) :
  for j in xrange(0,N) :
    eig = transport.Compute_largest_eigenvalue(lambda_x[j],lambda_y[i])
    if eig.imag<1e-12 and eig.imag>-1e-12 :
      print eig
      rho[i,j] = np.abs(eig.real)
    else :
      print ("The eigenvalue is complex "+str(eig))
      rho[i,j] = np.abs(eig)
    if condition_number==True :
      kappa[i,j] = transport.Compute_condition_number()

if condition_number==False :
  np.savez(filename,lambda_x=lambda_x,lambda_y=lambda_y,rho=rho)      
else :
  np.savez(filename,lambda_x=lambda_x,lambda_y=lambda_y,rho=rho,kappa=kappa) 
