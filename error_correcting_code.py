import math,re
# import primes to use from document
def getPrimes(n=None):
    primes=open("prime_list","r")
    primes=primes.read()
    # remove brackets
    primes=primes[1:len(primes)-2]
    # remove spaces
    primes=re.sub('[ ]','',primes)
    # split between commas to recreate array from string
    primes=primes.split(',')
    if n==None or n<1 or n>len(primes):
        n=len(primes)
    for i in range(n):
        primes[i]=int(primes[i])
    return primes

primes = getPrimes()
#[2,3,5,7]
# error correcting code that encodes M to C, and can correct up to t bit errors
class Message:
    def __init__(self, m):
        if type(m) == list:
            max_elem = 1
            if any([type(mi) != int for mi in m]):
                raise TypeError("Message must be list of integers!")
            self.y = max(m) + 1  # base
            # for mi in m:
            #     if type(mi) != int:
                    
            #     if mi > max_elem:
            #         max_elem = mi
            # self.y = max_elem + 1 # base
            

class ECC:
    def __init__(self, max_errors, base=2):
        self.y = base
        self.t = max_errors
    
    def in_M(self, m):
        if type(m) != list:
            return False
        for mi in m:
            if mi not in range(self.y):
                return False
        return True
    
    def encode(self, m): # specifics are irrelevant, can use
        def ReedMuller(m,t):
            # t = 2^(N-r-1)-1
            # m = sum([for i in range(r)])
            # r = N-log2(t)
            return 2^N
        return m, c