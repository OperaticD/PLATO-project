#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 16:15:22 2022

@author: daria
"""
import os, sys
import PySimpleGUI as sg
import numpy as np

varExists = True
projectDir = '/Users/daria/.conda/envs/platosim'
workDir = '/Users/daria/Desktop/DEUP/Work_Directory'
# workDir = '/Volumes/My Passport/PLATO Project'

globals()['projectDir'] = '/Users/daria/.conda/envs/platosim'
globals()['PLATO_WORKDIR']  = '/Users/daria/Desktop/DEUP/Work_Directory'
# globals()['PLATO_WORKDIR']  = '/Volumes/My Passport/PLATO Project'
if not 'projectDir' in globals():
    varExists = False
    print ("The global variable projectDir does not exist, set projectDir to the proper location in your environment.")

if not 'PLATO_WORKDIR' in globals():
    varExists = False
    print ("The global variable workDir does not exist, set workDir to the proper location in your environment.")

if varExists:
    os.environ['PLATO_PROJECT_HOME'] = projectDir
    os.environ['PLATO_WORKDIR'] = workDir
    sys.path.append(projectDir + "/python")

del(varExists)

from platosim.simulation import Simulation
# sim = Simulation('test', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
#                  , outputDir = workDir)
# sim.run(removeOutputFile=True)
# print(np.random.rand())
# print("Done 1")


# sim = Simulation('test2', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
#                  , outputDir = workDir)
# sim.run(removeOutputFile=True)
# print(np.random.rand())
# print("Done 3")

# sim = Simulation('test3', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
#                  , outputDir = workDir)
# sim.run(removeOutputFile=True)
# print(np.random.rand())
# print("Done 3")

# sim = Simulation('test4', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
#                  , outputDir = workDir)
# sim.run(removeOutputFile=True)
# print(np.random.rand())
# print("Done 3")

# sim = Simulation('test5', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
#                  , outputDir = workDir)
# sim.run(removeOutputFile=True)
# print(np.random.rand())
# print("Done 3")

# sim = Simulation('test6', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
#                  , outputDir = workDir)
# sim.run(removeOutputFile=True)
# print(np.random.rand())
# print("Done 3")


sim = Simulation('0-7E-S_m9_b', configurationFile = '/opt/anaconda3/pkgs/platosim-3.5.3-py37_0/inputfiles/inputfile.yaml'
                 , outputDir = workDir)
sim.run(removeOutputFile=True)
print(np.random.rand())
print("Done")

sg.popup('Simulation finished', font=("Arial, 13"))