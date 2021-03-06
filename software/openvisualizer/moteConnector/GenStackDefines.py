##
# Standalone script to generate the StackDefines.py file.
#
# This script extracts all the information it needs from the openwsn.h
# header file (part of the openwsn-fw repository), and generate the
# StackDefines.py file (part of the openwsn-sw repository).
#
# To run it, just double-click on this file.
#
# \note To have to check out the openwsn-fw and openwsn-sw side-by-side, i.e.
#       you should have a directory with two subdirectories openwsn-fw/ and 
#       openwsn-sw/ somewhere on your computer.
#
# \author Thomas Watteyne <watteyne@eecs.berkeley.edu>, August 2010
#

import os
import re
import time

#============================ defines =========================================

INPUT_FILE    = os.path.join('..','..','..','..','openwsn-fw','firmware','openos','openwsn','openwsn.h')
OUTPUT_FILE   = 'StackDefines.py'

#============================ helpers =========================================

def genComponentCodes():
    
    # find components code in openwsn.h
    codesFound = []
    for line in open(INPUT_FILE,'r'):
        m = re.search('\s*COMPONENT_(\S*)\s*=\s*(\S*),\s*',line)
        if m:
            name = m.group(1)
            try:
                code = int(m.group(2),16)
            except ValueError:
                print "WARNING: {0} is not a hex number".format(m.group(2))
            else:
                codesFound.append((code,name))
    
    # turn into text
    output  = ["components = {"]
    output += ["{0:>4}: \"{1}\",".format(a,b) for (a,b) in codesFound]
    output += ["}"]
    output  = '\n'.join(output)
    
    return output

def genErrorDescriptions():
    
    # find components code in openwsn.h
    codesFound = []
    for line in open(INPUT_FILE,'r'):
        m = re.search('\s*ERR_(\S*)\s*=\s*(\S*),\s*\/\/\s*([\S\s]*)',line)
        if m:
            name = m.group(1)
            desc = m.group(3).strip()
            try:
                code = int(m.group(2),16)
            except ValueError:
                print "WARNING: {0} is not a hex number".format(m.group(2))
            else:
                codesFound.append((code,desc))
    
    # turn into text
    output  = ["errorDescriptions = {"]
    output += ["{0:>4}: \"{1}\",".format(a,b) for (a,b) in codesFound]
    output += ["}"]
    output  = '\n'.join(output)
    
    return output

#============================ main ============================================

def main():
    
    if os.path.exists(INPUT_FILE):
        # we can access the openwsn.h file
        
        # gather the information
        output  = []
        output += ["# DO NOT EDIT DIRECTLY!"]
        output += ["# This file was generated automatically by GenStackDefines.py"]
        output += ["# on {0}".format(time.strftime("%a, %d %b %Y %H:%M:%S"))]
        output += ["#"]
        output += [""]
        output += [genComponentCodes()]
        output += [""]
        output += [genErrorDescriptions()]
        output += [""]
        output  = '\n'.join(output)
        
        # write to file
        file = open(OUTPUT_FILE,'w')
        file.write(output)
        file.close
        
        print "{0} created successfully.".format(OUTPUT_FILE)
        
    else:
        # we can NOT access the openwsn.h file
        
        # print error message
        output  = []
        output += ["ERROR: could not open the following file"]
        output += ["   {0}".format(INPUT_FILE)]
        output += [""]
        output += ["Do you have the openwsn-fw and openwsn-sw repositories"]
        output += ["checked out side-by-side?"]
        output  = '\n'.join(output)
        print output
        
    raw_input('\nScript ended. Press enter to close.')

if __name__ == '__main__':
    main()