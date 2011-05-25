import logging
import numpy as np
from random import *

class DnaGen():
    def __init__(self, length=None, p=None, e=None):
        f = open("output.log", "w")
        f.close()
        logging.basicConfig(filename="output.log", level=logging.DEBUG)

        logging.info("initializing DNA with length %d" % length)
        dna = [randint(0,3) for i in xrange(0,length)]
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
                b = range(0,4)
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


