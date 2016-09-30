import math
import decimal
import fractions
#use generators rather than lists

val = []
tags = []
correctTags = ['a','b','x_1','y_1','x_2','y_2']



#reads input.txt and puts inputs into list named val
def readInput():
	i = 0
	inp = open('input.txt','r')
		
	for line in inp:
			
		if not line.strip(): #ignores whitespace lines
			continue
		else:	
			ans = line.split()
			x = ans[-1]
			if ";" == x[-1] and len(ans) == 3:
				val.append(x[:-1]) #gives val array the character before ; in each line
				tags.append(ans[0]) #gives the variable tag to tags
			else:
				inp.close
				raise ValueError("Line:",line ,"Formatted incorrectly")
				
		i+= 1
		
	inp.close	
			

def checkTags(): #checks variables have compatible tags
	for tag in tags:
		if  tagDup() == False:
			for x in range(0,len(correctTags)):
				if tag == correctTags[x]:
					break
				else:
					if x == len(correctTags)-1: #Quite nested but solves the problem. May change.
						raise ValueError("inputed variable ",tag, "is not a valid variable")
		else:
			raise ValueError("two variables named the same thing")
			
			
def tagDup():	
	reg = []
	for x in tags:
		if x in reg:
			return True
		reg.append(x)	
	return False
	

def composeDict(): 
	res = [fractions.Fraction(i) for i in val]	
	dictionary = dict(zip(tags,res))
	return dictionary

def ellipticAddType():
	if dictionary['x_1'] != dictionary['x_2']:
		return 1
	
	elif dictionary['x_1'] == dictionary['x_2'] and dictionary['y_1'] != dictionary['y_2']:
		return 2
	
	elif dictionary['x_1'] == dictionary['x_2'] and dictionary['y_1'] == dictionary['y_2'] and dictionary['y_1'] != 0:
		return 3
	
	elif dictionary['x_1'] == dictionary['x_2'] and dictionary['y_1'] == dictionary['y_2'] and dictionary['y_1'] == 0:
		return 4
	
	else:
		return	0
	
	
	
def checkCurve():
	if y_1**2 != x_1**3 + a*x_1 + b or y_2**2 != x_2**3 + a*x_2 + b:
		raise ValueError("Point P or Q does not lie on curve with equation y^2 = x^3 + ax + b") 	
	
	else:
		return 0



readInput()
checkTags()
dictionary = composeDict()
type = ellipticAddType()
x_1 = dictionary['x_1']
x_2 = dictionary['x_2']
y_1 = dictionary['y_1']
y_2 = dictionary['y_2']
a = dictionary['a']
b = dictionary['b']
checkCurve()
if type == 1:
	m = fractions.Fraction((y_2 - y_1),(x_2 - x_1))
	x = m**2 - x_1 - x_2
	y = (x_1 - x)*m - y_1
	print("x coordinate is: {}".format(x),"y coordinate is: {}".format(y)) 
elif type == 2:
	print("the Point is the identity O")

elif type == 3:
	m = fractions.Fraction((3*((x_1)**2) + a),(2*y_1))
	x = m**2 - 2*x_1
	y = (x_1 - x)*m - y_1
	
	print("x coordinate is: {}".format(x),"y coordinate is: {} ".format(y)) 
elif type ==4:
	print("the Point is the identity O")
	
else:

	Print("Something went wrong")

			