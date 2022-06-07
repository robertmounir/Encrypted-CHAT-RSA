import random



def gcd(a, b):

    if (b == 0):
        return a
    else:
        return gcd(b, a % b)


def get_coprime(x):
    while (True):
        e = random.randrange(2, x)

        if (gcd(e, x) == 1):
            return e


def Ex_gcd(a, b):

    if b == 0:
        return (1, 0)
    (x, y) = Ex_gcd(b, a % b)
    k = a // b
    return (y, x - k * y)

def get_inverse(a,n):
    (b, x) = Ex_gcd(a, n)
    if b < 0:
        b = (b % n + n) % n 
    return b

def mod_pow(a, n, mod): 
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = mod_pow(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
          return b
        else:
          return b * a % mod



def gen_prime(n): 
    try:
        from Crypto.Util import number
    except:
        print("To generate large random numbers you need to install pycryptodome using 'pip install pycryptodome'\n** OR You can enter the prime numbers manually ** ")
        exit(-1)
   
    return number.getPrime(n)


def is_prime(p):
    if p==2 or p==3:
        return True

    if p%2==0 or p<2:
        return False

    for i in range(3,int(p**0.5)+1,2):   
        if p%i==0:
            return False  
         
    return True




def keygen(n=64,auto_gen=True):

    x="n"
    if(n<8):
        n= 8

    

    if auto_gen==False:  
        x= input("if you want to enter the key manually enter 'y' else 'n' ")
        if (x=="y"):
            while(True):
                a= int(input("enter P -> "))
                b= int(input("enter Q -> "))
                if(not (is_prime(a) and is_prime(b))):
                    print("ERROR : P & Q must be prime numbers -- Try again \n")
                    continue
                if(a==b):
                    print("ERROR : P cannot be equal Q -- Try again  \n")
                    continue
                    
                break
                

        else:
            a = gen_prime(n)
            b = gen_prime(n)
            while a == b:
                b = gen_prime(n)



      

  
    c = a * b
    phi = (a - 1) * (b - 1)
  
    e = get_coprime(phi)
    d = get_inverse(e, phi)
    

    return (e, d, c)



def ConvertToInt(message_str):
  res = 0
  for i in range(len(message_str)):
    res = res * 256 + ord(message_str[i])
  return res

def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def encrypt(string,e, c,n=64):

    if(n<8):
        n=8

    block=n//4
    encrypted=""
    for i in range(len(string)//block+1) :
        m= ConvertToInt(string[i*block:(i+1)*block])
        encrypted+=str(mod_pow(m, e, c))+' '
        
    return encrypted



def decrypt(string,d, c):
    M=string.split(' ')
    msg=""
    for m in M:
        if (m=='' or m== '0'):
            continue

        msg+=ConvertToStr(mod_pow(int((m)), d, c))

    return msg





def Prime_Factorization(n):
 
    factors = []
    prime = 2
    while n != 1:
        if n % prime == 0 and prime % 2 > 0:
            factors.append(prime)
            n /= prime
            prime += 1
        else:
            prime += 1
    return factors[0], factors[1]



def Break_key(e, n):

    a, b = Prime_Factorization(n)
    phi = (a - 1) * (b - 1)
    d = get_inverse(e, phi)
    return d


def CCA(e,d,n ,c , r ):
    c= c.split(' ')

    t=get_inverse(r,n)
    z= mod_pow(r,e,n)
    text=""
    for ci in c:
        if(ci==''):
            continue
        x=mod_pow(z*int(ci),1,n)
        Y=mod_pow(x,d,n)
        m=mod_pow(t*Y,1,n)
        text+=ConvertToStr(m)
    return text





















