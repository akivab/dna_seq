import logging
import numpy as np
from random import *

class DNA_Generator():
    def __init__(self, length=None, p=None, e=None):
        f = open("output.log", "w")
        f.close()
        logging.basicConfig(filename="output.log", level=logging.DEBUG)

        logging.info("initializing DNA with length %d" % length)
        dna = [randint(1,4) for i in xrange(0,length)]
        logging.info("dna has length %d" % len(dna))
        data = []

        t = 0
        z = [0]
        
        while z[t] < length:
            logging.info("at position %d at time %d" % (z[t], t))
            rand = random()
            if rand < e:
                data.append(dna[z[t]])
            else:
                b = range(1,5)
                b.remove(dna[z[t]])
                data.append(choice(b))

            rand = random()
            if rand < p:
                z.append(z[t]+1)
            else:
                z.append(max(0,z[t]-1))
            t += 1
        self.dna = dna
        self.data = data
        
class DNA_Solver():
    def __init__(self, length=None, p=None, e=None, sequence=None):
        self.length = length
        self.p = p
        self.e = e
        self.data = sequence
        self.obslength = len(sequence)

    def setup(self):
        length = self.length
        self.T = np.zeros((length, length))
        for i in xrange(1, length-1):
            self.T[i][i+1] = p
            self.T[i][i-1] = 1-p
        self.T[0][1] = 1
        self.T[length-1][length-2] = 1

        logging.info("initial transition matrix: %s" % str(self.T))

    def forward(self):
        length = self.length
        
        self.s = np.diag(self.e*np.ones((length,1)))
        for i in xrange(0,4):
            for j in xrange(0,length):
                for k in xrange(0,length):
                    if j==k:
                        self.A[i][j][k] = self.e
                    else:
                        self.A[i][j][k] = (1-self.e) / 3

        self.f = np.zeros((self.obslength, length))
        self.c = np.zeros((self.obslength, 1))
        
        # at time 1, probability we're at position 0 in sequence is 1
        self.f[1][0] = 1
        logging.info("initial forward counts: %s" % str(self.f))

        for t in xrange(2, length):
            self.f[t] = self.f[t-1]*self.A[data[t]]


p = 0.75
e = 0.99
length = 40
template = DNA_Generator(length=length, p=p, e=e)
guess = DNA_Solver(length=length,p=p,e=e,sequence=template.data)
guess.setup()
guess.forward()
print guess.T