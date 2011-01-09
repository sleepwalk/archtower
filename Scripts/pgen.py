#!/usr/bin/python

# Password Generator Script
# Written by: Lucian Adamson <lucian.adamson@yahoo.com>

try:
	from optparse import OptionParser as oparse
	import os, random
except ImportError as myErr:
	print("Error: The following import error occurred:")
	print(myErr)
	print("")
	print("Please fix this to continue.")
	quit()

pw_conf = {
	"alower" : True, 
	"aupper":True, 
	"numeric":True, 
	"punct":True, 
	"eliminate":True, 
	"howmany":5, 
	"length":8 
}

def Moronicator():
	randy = random.randint(0, 5)
	
	if randy == 0: moron = "Your a fucking idiot. Turn on the characters to generator a password."
	if randy == 1: moron = "Wow.. if common sense was money, you would be broke. Turn on one of the character sets to generate a password. Dumbass."
	if randy == 2: moron = "Another idiot bites the dust. Perhaps if you want a generated password, you should turn on one of the character sets?"
	if randy == 3: moron = "Great. Now I have to deal with another idiot.. which is YOU by the way. Turn on a character set, stupid."
	if randy == 4: moron = "Oh noes! Your an idiot!! Enable a character set dipshit."
	if randy == 5: moron = "By using all of these flags: lunp, you have became a self-proclaimed idiot! Congratulations!"
	
	return moron
	
def PasswordGenerator():
	global pw_conf
	
	charMap = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\\|'\";:/?.>,<"
	eliminator = "Il10Oij"
	newChar = ''
	Passwords = ''
	randy = random.randint
	
	if pw_conf['alower'] == True: newChar += charMap[0:26]
	if pw_conf['aupper'] == True: newChar += charMap[26:52]
	if pw_conf['numeric'] == True: newChar += charMap[52:62]
	if pw_conf['punct'] == True: newChar += charMap[62:94]
	
	if len(newChar) == 0:# if all the flags are disabled...
		print(Moronicator())
		quit()
	
	if pw_conf['eliminate'] == True:
		for each in eliminator:
			newChar=newChar.replace(each, "")
	
	for number_of_pws in range(0, pw_conf['howmany']):
		for length_of_pws in range(0, pw_conf['length']):
			Passwords += newChar[randy(0, len(newChar)-1)]
		Passwords += '\n'
	
	Passwords = Passwords.rstrip("\n")
	return Passwords
	

def Main():
	global pw_conf
	
	parser = oparse()
	parser.add_option("-l", "--alphalower", default=True, action="store_false", help="Use this flag to disable lowercase alpha characters",dest="use_loweralpha")
	parser.add_option("-u", "--alphaupper", default=True, action="store_false", help="Use this flag to disable uppercase alpha characters", dest="use_upperalpha")
	parser.add_option("-n", "--numeric", default=True, action="store_false", help="Use this flag to disable numeric characters", dest="use_numeric")
	parser.add_option("-p", "--punctuation", default=True,action="store_false",  help="Use this flag to disable punctuation characters", dest="use_punc")
	parser.add_option("-e", "--eliminate", default=True, action="store_false", help="Use this flag to turn off the elimination of look alikes", dest="eliminator")
	parser.add_option("-a", "--amount", default=5, help="The number of passwords to generate (default 5)", type="int", dest="numero")
	parser.add_option("-c", "--characters", default=8, help="How many characters a password should be", type="int", dest="lengthof")
	
	(options, args) = parser.parse_args()
	
	pw_conf['alower'] = options.use_loweralpha
	pw_conf['aupper'] = options.use_upperalpha
	pw_conf['numeric'] = options.use_numeric
	pw_conf['punct'] = options.use_punc
	pw_conf['eliminate'] = options.eliminator
	pw_conf['howmany'] = options.numero
	pw_conf['length'] = options.lengthof
	
	print(PasswordGenerator())
	return 0

Main()
