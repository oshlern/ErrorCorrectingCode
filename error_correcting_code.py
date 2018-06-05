import math, re, random, copy
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

def choose(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n-r))
    
# Representation of number
class Message(object):
    def __init__(self, m, base=None, split=None):
        if type(m) == list:
            if any([type(mi) != int for mi in m]):
                raise TypeError("Message must be list of integers!")

            self.bits = m
            self.length = len(self.bits)
            self.size = 2**self.length
            self.split = split

            calculated_base = max(m) + 1
            if base == None:
                self.base = calculated_base
            else:
                if calculated_base > base:
                    raise Exception("Invalid base passed!")
                self.base = base
            self.base = max(self.base, 2) # at least 2

            self.number = sum([self.base**i * m[i] for i in range(self.length)]) #m[self.length-i-1]

        elif type(m) == int:
            self.number = m

            if base == None:
                base = 2 # default base is 2
            self.base = max(base, 2) # at least 2

            self.bits = []
            while m > 0:
                self.bits.append(m % self.base)
                m //= self.base
            self.length = len(self.bits)
            self.size = 2**self.length
        
        else:
            raise TypeError("Message must be integer or list of digits")

    def __str__(self):
        return "Number: {}, y:{},len:{},size:{}".format(self.number, self.base, self.length, self.size) # Bits: {}

def random_mesage(length, base=2):
    return Message([random.randint(0,base-1) for i in range(length)], base=base)

            
# error correcting code that encodes M to C, and can correct up to t bit errors
class ECC(object):
    def __init__(self, max_errors, parameters=[]):
        self.t = max_errors
        self.P = parameters
        # self.alg = alg
    
    # def in_M(self, m):
    #     if type(m) != list:
    #         return False
    #     for mi in m:
    #         if mi not in range(self.y):
    #             return False
    #     return True
    
    def encode(self, m): # specifics are irrelevant, can use
        def ReedMuller_encoded_length(m,t):
            N = t
            k = 0
            while k < m.length:
                N += 1
                r = N - 1 - int(math.floor(math.log(t+1, m.base))) # not optimized, for readability
                k = sum([choose(N, i) for i in range(1,r+1)]) 
                # print(N, k, r)
                # t = 2^(N-r-1)-1
                # m = sum([for i in range(r)])
                # r = N-log2(t+1)-1
            return 2**(N-1)
        encoded_length = ReedMuller_encoded_length(m, self.t)
        padded_bits = m.bits + [0]*(encoded_length - m.length)
        return Message(padded_bits, base=m.base) #random_mesage(encoded_length, base=m.base)
    
    def decode(self, c):
        depadded_bits = copy.deepcopy(c.bits)
        while depadded_bits[-1] == 0:
            depadded_bits.pop()
        return Message(depadded_bits, c.base)

def prime_encode(m,t):
    num = 1
    for i in range(m.length):
        num *= primes[i]**m.bits[i]
    lower_bound = 2*primes[m.length]**(2*t)
    upper_bound = 2*lower_bound
    p = primes[-1]
    for pi in primes[m.length:]:
        if lower_bound<pi<upper_bound:
            p = pi
            break
    return num % p

class Extended_ECC(ECC):
    def __init__(self, max_errors, parameters=[]):
        self.t = max_errors
        self.P = parameters
        # self.alg = alg
    
    # def in_M(self, m):
    #     if type(m) != list:
    #         return False
    #     for mi in m:
    #         if mi not in range(self.y):
    #             return False
    #     return True
    
    def encode(self, m): # specifics are irrelevant, can use
        c = prime_encode(m, self.t)
        return Message(m.bits + super(Extended_ECC, self).encode(c).bits, base=m.base, split=m.length)
      
    def decode(self, c):
        
        new_m, c_encoded = c.bits[:c.split], c.bits[c.split:]
        cm = super(Extended_ECC, self).decode(c_encoded)
        c_new_m = prime_encode(new_m, self.t)
        # diff = simplify_a_over_b_mod(cm/c_new_m, p)
        # e = convert_to_prime_bits(diff)
        # m = new_m ^ e
        # return m
        

RD = ECC(7)
m = random_mesage(163)
#Message([1,1,1,1,0,1,1,1,1,0,1])#[0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,])
c = RD.encode(m)
out = RD.decode(c)

print(m)
print(c)
print(out)

