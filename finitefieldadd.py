import math
import decimal
import fractions
import dateutil
#import numpy as np
import matplotlib.pyplot as plt
#need to use generators rather than lists
#overhaul of functions
val = []
tags = []
correctTags = ['a','b','x_1','y_1','p','r']
outputx = []
outputy = []


#reads input1.txt and puts inputs into list named val
def readInput():
	i = 0
	inp = open('input1.txt','r')
		
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
				raise ValueError("Line: {} formatted incorrectly.".format(line))
				
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
			
			
def tagDup():#checks for duplicate variable names	
	reg = []
	for x in tags:
		if x in reg:
			return True
		reg.append(x)	
	return False
	

def composeDict(): 
	res = [int(i) for i in val]	
	dictionary = dict(zip(tags,res))
	return dictionary

	
def checkCurve():
	if (basey**2) % p != (basex**3 + a*basex + b) % p:
		raise ValueError("Point P does not lie on curve with equation y^2 = x^3 + ax + b") 	
	
	else:
		return 0


def writeOutput():
	with open('output.txt', 'w') as output:
		i = 1
		#output.write('\nP = ({},{})'.format(dictionary['x_1'],dictionary['y_1']))
		for s,t in zip(outputx,outputy):

			output.write('\n{}P = ({},{})'.format(i,s,t))
			i += 1


def invmodp(a):
    '''
    NOT MINE!!!!!
	Credit:http://code.activestate.com/recipes/576737-inverse-modulo-p/
    The multiplicitive inverse of a in the integers modulo p.
    Return b s.t.
    a * b == 1 mod p
	NOT MINE!!!!!
    '''
    
    for d in xrange(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d			




readInput()
checkTags()
dictionary = composeDict()
x_1 = dictionary['x_1']
y_1 = dictionary['y_1']
a = dictionary['a']
b = dictionary['b']
p = dictionary['p']
r = int(dictionary['r']) #ugly typecast so i can use it for xrange
basex = x_1
basey = y_1
checkCurve()
outputx.append(basex)
outputy.append(basey)

for s in xrange(r-1):
	if x_1 == 0 and y_1 == 0:
		outputx.append(basex)
		outputy.append(basey)
		x_1, y_1 = basex, basey
		continue

	elif basex == x_1 and basey == y_1 and x_1 != 0  and y_1 != 0:
		m = (3*(basex)**2 + a)*invmodp(2*basey)
	elif basex == x_1: #at most two points with same x.
		outputx.append(float('inf'))
		outputy.append(float('inf'))
		x_1, y_1 = 0, 0
		continue		

	else:
		m = (y_1 - basey)*invmodp((x_1-basex)) 

	x = (m**2 - x_1 - basex) % p
	y = (m*(basex - x) - basey) % p

	outputx.append(x)
	outputy.append(y)

	x_1, y_1 = x, y

writeOutput()	

fig = plt.figure() 
#ax = fig.add_subplot(111)
fig.canvas.set_window_title('y^2 = x^3 + {}x + {} over Z/{}Z'.format(a,b,p))
plt.scatter(outputx, outputy) 
#for xy in zip(outputx, outputy):                                       # <--
    #ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
#plt.xlim(xmin = 0)
#plt.ylim(ymin = 0)
#plt.xticks(np.arange(min(outputx), max(outputx)+1, 1.0)) #min() and max() return floats so range() can't be used
#plt.yticks(np.arange(min(outputy), max(outputy)+1, 1.0))
plt.suptitle('m({},{}) for m varying over 1-{}'.format(basex,basey,r),fontsize = '12')
plt.show()
