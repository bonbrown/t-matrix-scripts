#!/usr/bin/python

import os
import re

#------------------------------------------------------------------------------#
#
#   tasks: * write t-matrix code with new particle size, recompile and run
#          * read output and write horizontal and vertical reflectivity to
#               to lookup table by size
#          * loop over sizes, perhaps look over hydrometeor types
#
#   Bonnie Brown, December 2014, University at Hawaii Manoa
# 
#------------------------------------------------------------------------------#

pth = '/Users/brbrown/tools/t-matrix/'
ltfile = 'lookup.txt'
#outfile = 'test'

#fmt = '%7.5f %11.5e %11.5e %11.5e %11.5e\n'
# format for julia complex numbers
fmt = '%7.5f [%11.5e+(%11.5e)im] [%11.5e+(%11.5e)im]\n'

os.system('rm '+pth+ltfile)
os.system('touch '+pth+ltfile)
lt = open(pth+ltfile,'a')
os.chdir(pth)

sizes = [0.25,0.50,0.75,1.0,1.25,1.50,1.75,2.0,2.25,2.50,2.75,3.0,3.25,3.50,3.75,4.0] # particle size in mm

for r in sizes:
    
    # ampld.lp.f takes radius, but reflectivity etc schemes take diameter
    rs = str(r)
    ds = str(r*2)
    print 'Compiling and calculating t-matrix values for a drop with equal area sphere radius of ' + rs + 'mm'
    newfile = ds+'mm'
    
    # recompile for various sizes and run
    #os.system('rm ampld.lp.f')
    os.system('touch '+newfile)
    os.system('./write_newsize_tmatrix.sh '+rs+' \\\''+newfile+'\\\'')
    os.system('./makeit')
    #os.system('rm test')
    os.system('./t-matrix')


    # read t-matrix output and write to lookup table
    ot = open(pth+newfile,'r')
    
    x =   ot.read()
    
    s =   re.search('(?<=S11=).*',x) # horizontal 
    s11 = s.group(0)
    # check for negative signs in the second term
    k = re.search('i\*-',s11)
    s11e = s11.replace('D','E')
    if k:
        s11i = s11e.replace('+ i*-','-')
    else:
        s11i = s11e.replace('i*','')
    s11s = s11i.replace(' ','')
    s11c = complex(s11s+'j')
    s11re = s11c.real
    s11im = s11c.imag
    
    s =   re.search('(?<=S22=).*',x) # vertical
    s22 = s.group(0)
    m = re.search('i\*-',s22)
    s22e = s22.replace('D','E')
    if m:
        s22i = s22e.replace('+ i*-','-')
    else:
        s22i = s22e.replace('i*','')
    s22s = s22i.replace(' ','')
    s22c = complex(s22s+'j')
    s22re = s22c.real
    s22im = s22c.imag
    
    s =   re.search('(?<=-SPHERE RADIUS= ).*',x) # particle equal surface area sphere radius in mm
    psize = 2*float(s.group(0)) # same as ds
    
    # write values to lookup table in formate particle size, real part of S11, imaginary part of S11, real S22, imaginary S22
    row = (psize,s11re,s11im,s22re,s22im)
    lt.write(fmt % row)
    ot.close()

lt.close()
   
    
