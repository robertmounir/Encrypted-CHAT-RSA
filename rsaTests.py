
import rsa as RSA



def EN_DE_test():
    e,d,n= RSA.keygen(auto_gen=False)
    msg= input("enter the msg you want to encrypt then decrypt: ")
    de_msg =RSA.decrypt(RSA.encrypt(msg,e,n,16),d,n)
    print("\n*$ The msg after decryption: "+ de_msg)


def CCA_test():
    e,d,n = RSA.keygen(auto_gen=False)
    msg= input("enter the msg: ")
    c=RSA.encrypt(msg,e,n,16)
    r= int(input("enter the value of r: "))
    A_msg =RSA.CCA(e,d,n,c,r)
    print("\n*$ The msg after CCA: "+ A_msg)
    

def BFA_test():
    e, d, n= RSA.keygen(16,auto_gen=False)
    privte_Key= RSA.Break_key(e,n)
    print((f"d: {d}, e: {e}, n: {n}"))
    print("\n*$ Broken private key: "+str(privte_Key))



while(True):
    x=  input(
        "\n\nEnter the number of the test\n"+
        "1. Encrypt msg then Decrypt it \n"+
        "2. Bruteforce Attack \n"+
        "3. CCA \n"
        "4. * Exit *\n"
    
    )


    if(x=="3"):
        CCA_test()
    elif(x=="1"):
        EN_DE_test()
    elif(x=="2"):
        BFA_test()
    else:
        print("# Exiting")
        break






