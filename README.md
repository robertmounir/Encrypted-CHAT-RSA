Encrypted CHAT RSA
===================

Chat with Server-Client Architecture
The Chat is Encrypted with RSA Asymmetric Encryption Algorithm   

How To Run
----------

* python3 Chat.py <hostname/IP> <port>
* "example" : python3 Chat.py localhost 3000



Dependencies
-------------------------
* standard Python libraries.
* pycrptodome library only to generate large prime numbers


RSA Algorithm
--------------

1. Chose two random prime numbers ->  p & q
2. Calculate n ->  n = p*q
3. Calculate phi -> phi = (p-1)*(q-1) 
4. Chose Public key (e) where it is coprime with phi 
5. Calculate Private key (d) where it is the inverse of (e) mod phi

### To encrypt 
* C= M^e mod n 
### To decrypt 
* M= C^d mod n

RSA Analysis
--------------

<img src="./Analysis_graphs\RSA-Encryption-Time.png" alt="Time of Encyrption" title="Time of Encyrption">



Brute Force Attack
------------------
* n = p*q
* phi = (p-1)*(q-1)
* Public key (e) is a coprime with phi
* Private key (d) is an inverse of (e) mod phi
### Given public key (e),(n):
We can perform prime factorization for n to get p and q by trying all prime
number from 2
Once we get p and q we can compute phi as phi = (p-1)*(q-1)
Then get the inverse of (e) mod phi by extended Euclid algorithm
## d = e-1 mod phi

<img src="./Analysis_graphs\Bruteforce-Attack.png" alt="Time of Brute force Attack" title="Time of Brute force Attack">


Chosen Cipher Text Attack
--------------------------
* C= M^e mod n
* M= C^d mod n
* Given: Cipher text (C), public key (e),(n)
### First we chose random number (r) and calculate ->
1. z=re mod n
2. t= r-1 mod n
3. x= z*c mod n
4. Then send x to be encrypted with private key (Y)
5. Y= xd mod n
### Therefore
* Y= (z*c)d mod n
* Y= (z^d mod n)*(cd mod n)
* z= r^e mod n
* Y= (r^e*d mod n)*(cd mod n)
* Y= (r * cd mod n)
### Multiply Y by r inverse (t)
* t*Y = t*r*cd mod n
* t*Y = 1*cd mod n
* M= t*Y = cd mod n


ScreenShots
--------------
<br>
<img src="ScreenShots\1.png">
<img src="ScreenShots\2.png">
<img src="ScreenShots\3.png">
<img src="ScreenShots\4.png">
<img src="ScreenShots\5.png">
<img src="ScreenShots\6.png">
<br>





