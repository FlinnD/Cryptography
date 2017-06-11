###################################################################
import math
import collections
import random
val = []
tags = []
correctTags = ['a','b','x_1','y_1', 'n', 'h', 'p']
outputx = [] 
outputy = []
# unlike before we will create a named tuple 'Point'
#and make our functions accept it as input.
Point = collections.namedtuple('Point', 'x_1 y_1')

#reads input3.txt and puts inputs into list named val
def readInput():
	i = 0
	inp = open('input3.txt','r')
		
	for line in inp:
			
		if not line.strip(): #ignores whitespace lines
			continue
		else:	
			ans = line.split()
			x = ans[-1]
			if ";" == x[-1] and len(ans) == 3:
				#gives val array the character before ; in each line
				val.append(x[:-1]) 
				#gives the variable tag to tags
				tags.append(ans[0])
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
					if x == len(correctTags)-1: 
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
	

def composeDict(): #puts together a dictionary of values from input file
	res = [int(i) for i in val]	
	dictionary = dict(zip(tags,res))
	return dictionary

	
def checkCurve(point): #checks points lie on the elliptic curve specified
	p = dictionary['p']
	a = dictionary['a']
	b = dictionary['b']
	if (point.y_1**2) % p != (point.x_1**3 + a*point.x_1 + b) % p:
		raise ValueError("Point P does not lie on curve with equation y^2 = x^3 + ax + b") 	
	
	else:
		return 0
			
def ellipticAddType(p1,p2):#decides how to add points on elliptic curves
	if p1.x_1 == float('inf') and p2.x_1 == float('inf'):
		return 4
	if p1.x_1 == float('inf') or p2.x_1 == float('inf'):
		return 0
	elif p1.x_1 != p2.x_1:
		return 1
	
	elif p1.x_1 == p2.x_1 and p1.y_1 != p2.y_1:
		return 2
	
	elif p1.x_1 == p2.x_1 and p1.y_1 == p2.y_1 and p1.y_1 != 0:
		return 3
	
	elif p1.x_1 == p2.x_1 and p1.y_1 == p2.y_1 and p1.y_1 == 0:
		return 4
	
	else:
		return	5			

def invmod(a,p):#calculates an integer's inverse modulo some p
    '''
	This function is a modification of code at: 
	http://code.activestate.com/recipes/576737-inverse-modulo-p/.
	
    The multiplicitive inverse of a in the integers modulo p.
    Return b s.t.
    a * b == 1 mod p
    '''
    for d in xrange(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d
	

def addEllip(p1, p2):#adds points (of named tuple) on an elliptic curve.
#unlike before we will return points not print them
	dictionary = composeDict()
	type = ellipticAddType(p1,p2)
	x_1 = p1.x_1
	x_2 = p2.x_1
	y_1 = p1.y_1
	y_2 = p2.y_1
	a = dictionary['a']
	b = dictionary['b']
	p = dictionary['p']
	if type == 1:
		m = (y_2 - y_1)*invmod(x_2 - x_1,p)
		x = (m**2 - x_1 - x_2)%p
		y = ((x_1 - x)*m - y_1)%p
		#print("x coordinate is: {}".format(x),"y coordinate is: {}".format(y))
		return x, y
		
	elif type == 2:
		#print("the Point is the identity O")
		return float('inf'), float('inf')

	elif type == 3:
		m = (3*((x_1)**2) + a)*invmod(2*y_1,p)
		x = (m**2 - 2*x_1)%p
		y = ((x_1 - x)*m - y_1)%p
		#print("x coordinate is: {}".format(x),"y coordinate is: {} ".format(y))
		return x, y
		
	elif type ==4:
		#print("the Point is the identity O")
		return float('inf'), float('inf')
	elif type == 0:
		if x_1 == float('inf'):
			return x_2, y_2
		else:
			return x_1, y_1
	else:
		raise ValueError("Something went wrong")

def scalM(r, point):#performs multiplication by a scalar of a point.
# we will return output rather than write to file.
	a = dictionary['a']
	b = dictionary['b']
	p = dictionary['p']
	basex = point.x_1
	basey = point.y_1
	x_1 = point.x_1
	y_1 = point.y_1
	outputx.append(basex)
	outputy.append(basey)
	if r == 0:
		return float('inf'), float('inf')
	else:
		for s in xrange(r-1):
			if x_1 == 0 and y_1 == 0:
				outputx.append(basex)
				outputy.append(basey)
				x_1, y_1 = basex, basey
				continue

			elif basex == x_1 and basey == y_1 and x_1 != 0  and y_1 != 0:
				m = (3*(basex)**2 + a)*invmod(2*basey,p)
			elif basex == x_1: #at most two points with same x.
				outputx.append(float('inf'))
				outputy.append(float('inf'))
				x_1, y_1 = 0, 0
				continue		
			else:
				m = (y_1 - basey)*invmod((x_1-basex),p) 

			x = (m**2 - x_1 - basex) % p
			y = (m*(basex - x) - basey) % p

			outputx.append(x)
			outputy.append(y)

			x_1, y_1 = x, y

		return outputx[-1], outputy[-1]
	
def genKeypair():#calculates private and public keys.
		private = random.randrange(1, dictionary['n'])
		public  = scalM(private, basepoint)
		
		return private, public


def genHash():
		
		#simulates generating a hash.
		#Remember hashing is basically for fixing length in ECDSA
		#so the message need not mean anything.
		#Doing it this way also demonstrates the pair (r,s)
		#being different every time the script is run.
		z = random.getrandbits(dictionary['n'])
		
		
		return z

def sign(private):#creates the pair (r,s)		
	z = genHash()
	
	r = 0
	s = 0
	while not r or not s:#run until r,s are non zero
		k = random.randrange(1, dictionary['n'])
		x, y = scalM(k, basepoint)
		
		r = x % dictionary['n']
		s = (invmod(k,dictionary['n'])*(z+r*private))% dictionary['n']
		#print(r,s,z)
	return r, s, z

def verify(public, signature):#signature verification
	r, s, z = signature #grab the information from signature tuple
	#that the signer has released
	w = invmod(s,dictionary['n'])
	
	u_1 = (z*w)% dictionary['n']
	
	u_2 = (r*w)% dictionary['n']
	
	x, y = scalM(u_1, basepoint)
	p1 = Point(x_1= x, y_1= y,)
	x, y = scalM(u_2, public)
	p2 = Point(x_1= x, y_1= y,)
	x, y = addEllip(p1, p2)
	#finally verify the signature
	if((r % dictionary['n'])== (x % dictionary['n'])):
		return 0
		
	else:
		return 1
		
		
		
	
readInput()
checkTags()
dictionary = composeDict()
#intializing basepoint in the format the functions accept.
basepoint = Point(x_1 = dictionary['x_1'], y_1 = dictionary['y_1'],)
checkCurve(basepoint)

priv, pub = genKeypair()
#
public = Point(x_1 = pub[0], y_1= pub[1],)


signature = sign(priv)

print('Signature is ({},{})'.format(signature[0],signature[1]))

if verify(public, signature)==0:
	print('Signature verified successfully')

else:
	print('Verification has failed')
	
###################################################################