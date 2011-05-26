

from dnagen import *

class DnaSol():
    def __init__(self, L=None, p=None, e=None, sequence=None):
        self.t = len(sequence)
        self.T = np.zeros((L, L))
        self.z = np.zeros((self.t, L))
        self.f = np.ones((4, L))
        self.e = e
        self.p = p
        self.data = sequence
        self.L = L
        # set up transition matrix
        for i in xrange(0,L):
            for j in xrange(0,L):
                if i==j-1:
                    self.T[i,j] = p
                elif i==j+1:
                    self.T[i,j] = 1-p
        self.T[0,1] = 1
        self.T[L-1,L-1] = 1
        self.T[L-1,L-2] = 0
        
        # set up z[0]
        self.z[0,0] = 1
        # set up z[L-1]
        self.z[self.t-1,L-1] = 1

    def forward(self):
        # forward chaining
        for i in xrange(0, self.t):
            if i > 0:
                for j in xrange(0,self.L):
                    self.z[i] += self.z[i-1,j] * self.T[j]
                self.z[i] /= sum(self.z[i])
            print i,self.z[i]
        for i in xrange(0,self.t):
            #print "the %dth variable has distribution %s" %(i, str(self.z[i]))
            for k in xrange(0,4):
                if self.data[i] == k:
                    self.f[k]+=self.z[i]*self.e
                else:
                    self.f[k]+=self.z[i]*((1-self.e)/3)
            # print self.f
        for i in xrange(0,self.L): self.f[:,i] /= sum(self.f[:,i])
        logging.info("sum to one across all time points: %s" % str(sum(self.f)))
        
    def backward(self, num=10):
        print self.f
        # backward sampling
        sample = np.zeros((num,self.L))
        for i in xrange(0,num):
            for j in xrange(0,self.L):
                r = random()
                for k in xrange(0,4):
                    if self.f[k,j] >= r:
                        sample[i,j] = k
                        break
                    else:
                        r -= self.f[k,j]
        return sample

p = 0.6
e = 1
length = 5
dna = DnaGen(length, p, e)
print dna.dna
print dna.data
# let the generating sequence be 
# let the data be 
#dna = [0,1,2,2,2,3,2,1,2,2,1,1,0,0,1,2,1,2,3,0,2]
#data = [0,1,2,2,2,3,2,3,2,1,2,1,2,2,1,1,0,1,0,0,1,2,1,2,1,2,3,2,3,0,2]
sol = DnaSol(length, p, e, dna.data)
sol.forward()
sample = sol.backward()
print sample
print sum(sample == dna.dna)
