#!/usr/bin/env python

import os
import filecmp
from os import path
from filecmp import dircmp
import sys
import subprocess as sp
from os import path


#Compare two directories using the python filecpm.dircmp facility
def comp_with_fatts(d1, d2):
    print(" Comparing with pythons filecmp.dircmp - i.e. by unix file attributes.")
    filecmp.dircmp(d1,d2).report()
    #for name in dcmp.diff_files:
    #    print ("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
    #for sub_dcmp in dcmp.subdirs.values():
    #    print_diff_files(sub_dcmp)


#Compare the netcdf files among the two directories using GFDL's (Remiks) nccmp utility
def comp_with_nccmp (d1, d2):
    extension_nc = '.nc'
    cmpCommand = 'nccmp'

    # Create a list of all the files with the specified extension
    nc_files = [f for f in os.listdir(d1) if f.endswith(extension_nc)]
    dcount = 0
    fcount = 0
    
    #Iterate over the files to compare
    for nc_name in nc_files :
        global files_compared, files_failed
        f1 = d1 + '/' + nc_name
        f2 = d2 + '/' + nc_name
        fcount += 1
        files_compared += 1
    
        print("-------------------------")
        print("Starting nccmp compare of " + nc_name)

        ##nccmp -d only prints first diff in file; -df prints more'
        # Fields of make_hgrid output: x,y,dx,dy,angle_dx,angle_dy,arcx,area
        #other_args = ' --variable=angle_dx,angle_dy --tolerance=1.0e-8 '
        #other_args = ' --Tolerance=1.0e-10 '
        #other_args = ' --tolerance=1.0e-7 '
        other_args = ' '
        finCommand = cmpCommand + ' -d ' + other_args  
        
        p = sp.Popen(finCommand +  f1 + ' ' + f2 , stdout=sp.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if (p_status != 0):
            dcount += 1
            files_failed += 1

    print("-----------------------------")
    print("nccmp comparisons finshed.")
    print("Dir 1 :" + os.path.abspath(d1));
    print("Dir 2 :" + os.path.abspath(d2));
    if(len(nc_files) > 0):
        print("Comparison command: " + finCommand)
        print("[# files compared, # files differing]: [" + str(fcount) + ", " + str(dcount) +"]")
    else:
        print("no files compared for " + os.path.abspath(d1))
        
    print("-----------------------------")

#Compare the netcdf files among all corresponding subdirectories of the
# the two directories using GFDL's (Remiks) nccmp utility
def comp_with_nccmp_subdirs (d1, d2):
    subdirs =  [f.name for f in os.scandir(d1) if f.is_dir()]
    print("Subdirectories to compare:")
    for element in subdirs:
        print (element)

    print("-----------------------------")
    global files_failed 
    global files_compared
    files_failed = 0
    files_compared = 0
    for element in subdirs:
        comp_with_nccmp(d1 + '/' + element, d2 + '/' + element)

    print("[total files compared, total files differing]: [" + str(files_compared) + ", " + str(files_failed) +"]")

if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print('Usage: dircompnc.py director1 directory 2')
        sys.exit(-1)

    dirA = sys.argv[1]
    dirB = sys.argv[2]
    print('Directory A: ', dirA)
    print('Direcotry B: ', dirB)
    if (path.exists(dirA) == False):
        print(dirA, 'does not exist...bye')
        sys.exit(-1)
    if (path.exists(dirB) == False):
        print(dirB, 'does not exist...bye')
        sys.exit(-1)
    if (path.isdir(dirA) == False):
        print(dirA, 'is not a directory. ... bye ...')
        sys.exit(-1)
    if (path.isdir(dirB) == False):
        print(dirB, 'is not a directory. ... bye ...')
        sys.exit(-1)

    comp_with_fatts(dirA, dirB)

#comp_with_nccmp(dirA, dirB)
    comp_with_nccmp_subdirs(dirA, dirB)
    print("All comparisons fininshed")

