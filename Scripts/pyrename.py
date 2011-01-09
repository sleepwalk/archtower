#!/usr/bin/python

# Script Name: pyrename
# Author: Lucian Adamson <lucian.adamson@yahoo.com>
# Version: 2.0
# Date: 09/07/2010


# IMPORT LIBRARYS
import os, sys, random
from optparse import OptionParser

# GENERATE CLI OPTIONS
parser = OptionParser()
parser.add_option("-f", "--filetype", metavar="filetype",default=".jpg", help="Choose file type to rename", type="string", dest="ren_filetype")
parser.add_option("-p", "--prefix", metavar="prefix", default="Pictures", help="Choose a filename prefix", type="string", dest="ren_prefix")
parser.add_option("-s", "--startcount", metavar="startcount", default=1, help="Choose what number to start counting from", type="int", dest="ren_startcount")
parser.add_option("-d", "--directory", metavar="directory", default=".", help="Define a different directory besides the working directory", type="string", dest="ren_directory")

#PARSE OPTIONS
(options, args) = parser.parse_args()

# ASSIGN TO SHORTER VARIABLES
ren_filetype = options.ren_filetype
ren_prefix = options.ren_prefix
ren_startcount = options.ren_startcount
ren_directory = options.ren_directory

#GENERATE A RANDOM NUMBER
randint = random.randint(10000, 100000)

#GET DIRECTORY LISTING
directoryListing=os.listdir(ren_directory)
#GET COUNT ON LISTING
listingCount = len(directoryListing)
#GET NUMBER OF DIGITS IN LIST COUNT
zeroCount = len(str(listingCount))

# RENAME FILES TO SOMETHING RANDOM
# Explanation: If you start to rename a directory of jpgs that are in this 
#                     format: IllinoisTrip-##.jpg and are using the same prefix
#                     then if this step is skipped, you will lose some files due to
#                     the renaming convention using already existing file names.
#                     To prevent that, we create temp files then rename using the
#                     prefix desired. Therefore, solving the dilemma.
for tmp in directoryListing[:]:
	if tmp.endswith(ren_filetype):
		zeroMaker = ('%(#)0' + str(zeroCount) + 'd') % {"#":ren_startcount}
		os.rename(tmp, 'd' + zeroMaker + ren_filetype)
		ren_startcount += 1

# Reset our variables, getting a new listing, list count and digit count
# as well as resetting the starting count
directoryListing=os.listdir(ren_directory)
listingCount = len(directoryListing)
zeroCount = len(str(listingCount))
ren_startcount = options.ren_startcount

# Go ahead and rename files accordingly
for renLoop in directoryListing[:]:
	if renLoop.endswith(ren_filetype):
		zeroMaker = ('%(#)0' + str(zeroCount) + 'd') % {"#":ren_startcount}
		os.rename(renLoop, ren_prefix + '-' + zeroMaker + ren_filetype)
		ren_startcount += 1
	
