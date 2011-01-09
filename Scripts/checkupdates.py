#!/usr/bin/python

# Script Name: checkupdates.py
# Author: Lucian Adamson <lucian.adamson@yahoo.com>
# What This Script Does: Formats how the output of pacman updates in conky looks
#
# Examples:
# Say you want to output your pacman updates to conky but only want the top 5 to show
# using the colors red, blue, and green for each line and you wish to have the number of updates
# in a header, you would do this:
#
# ${execpi 900 /path/to/checkupdates.py -e 'Updates ($n):' -c 'red,blue,green' -n 5}
# OR using long options
# ${execpi 900 /path/to/checkupdates.py --header='Updates ($n):' --colors='red,blue,green' --number-of-updates=10}
#
# This function can be run from the command line and there is a -h, --help option
# /path/to/checkupdates.py --help
#
# You can use this script to just output the number of updates like this:
# /path/to/checkupdates.py -g
#
# Sample output of checkupdates.py --colors='red,white,blue' -e '$n updates'
#
#6 updates
#${color red}chromium 5.0.375.125-1$color
#${color white}libpciaccess 0.11.0-1$color
#${color blue}mutagen 1.19-1$color
#${color red}orc 0.4.6-1$color
#${color white}q4wine 0.119-1$color
#${color blue}wine 1.3.0-1$color


from sys import argv as gv
from optparse import OptionParser as op
import re

onecolor = False # Variable that will change if more than one color is given

#--------------------------- Run a shell command and retrieve output --------------------------
class Command(object):
	def __init__(self, command):
		self.command = command
	def run(self, shell=True):
		import subprocess as sp
		process = sp.Popen(self.command, shell = shell, stdout = sp.PIPE, stderr = sp.PIPE)
		self.pid = process.pid
		self.output,self.error = process.communicate()
		self.failed = process.returncode
		return self
	
	@property
	
	def returncode(self):
		return self.failed

# ------------------------ Parse command line options and arguments ------------------------
parser = op()
parser.add_option('-c', '--colors', action='store', default='orange,red', help='Supply either one or more colors in comma separated values. Example: orange,red,blue')
parser.add_option('-n', '--number-of-updates', action='store', default=10, type='int', help='The number of maximum updates to display in Conky.')
parser.add_option('-g', '--get-number', action='store_true', default=False, help='Returns the number of updates available through pacman.')
parser.add_option('-e', '--header', action='store', default='', help='Sets a header for your conky output. Replacable variables are $n for number of updates.')
(options, args) = parser.parse_args()

# --------------------------------------------- The -g flag ------------------------------------------------

theupdates = Command("pacman -Qu").run()
theupdates_ord = theupdates.output
theupdates_ord = theupdates_ord.decode('ascii')
theupdates = theupdates_ord.split("\n") # Split output of -Qu by line
numdates = len(theupdates) # Count the lines
if numdates > 0: # if there are actually updates
	try:
		theupdates.remove('') #remove the blank line at end
		numdates=len(theupdates) # recount
	except ValueError:
		pass # If error because there is no blank line, keep going
if options.get_number:
	print(numdates)
	quit()

# ------------------------------------------ Set Variables -------------------------------------------
numupdates = options.number_of_updates #Variables set by optparse
colors = options.colors
header = options.header
# ----------------------------------------- Parse the Colors -----------------------------------------

colors = colors.lower() # convert text to lowercase
if re.search(',', colors): # if more than one color
	colors = colors.split(',') # split them
	for x in range(0, len(colors), 1): # loop through and remove unnec spaces
		colors[x] = colors[x].strip(' ')
	colorlist_len = len(colors) # This counts the colors
else:
	onecolor = True

# --------------------------------------------- The Code -----------------------------------------------

pacup_split = theupdates 

i = 1
pHolder = ''
totalnow = 1
if not header=='': # If there is a header...
	header = header.replace("$n", str(numdates)) #...replace $n with num of updates
	pHolder = header + '\n' # and append if to pHolder variable for output with actual updates
	
if onecolor == True: # if there is only one color
	for each in pacup_split: # loop through
		if not totalnow > numupdates: # makes sure we only display the alloted number of updates
			pHolder = pHolder + "${color " + colors + "}" + each + "$color\n"
		else:
			pHolder = pHolder.rstrip('\n') + '...\n' #if there are more, we recognize that by adding 3 periods
			break
		totalnow += 1
	print(pHolder.rstrip('\n')) # strip off the remaining new line to conserve our conky space
	quit() #we're done so quit the script

for newout in pacup_split: # this is the code for more than one color
	if i > colorlist_len: i = 1 # if i is greater than number of colors, then reset i
	if not totalnow > numupdates:
		pHolder = pHolder + '${color ' + colors[i - 1] + '}' + newout + '$color\n'
	else:
		pHolder = pHolder.rstrip('\n') + '...\n' # we put a \n to conform to line of code above
		break
	i += 1 # increase i by one until it is reset
	totalnow += 1 # helps make sure we only display the correct number of updates

print(pHolder.rstrip('\n')) #print the updates without the trailing \n
