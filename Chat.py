import sys
import socket
import threading
import rsa as RSA

N_BITS = 16
auto_gen_key =False


def Server(host, port):

    port = int(port)

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)

        print ("# Waiting for The Clint to Connect... \n")
        conn, _ = server.accept()

    except socket.error as err:
        print ("socket creation failed with error %s" %(err))



    key = conn.recv(4094).decode()
    key = key.split(',')
    publicTuple = (key[0], key[1])
    print ("# Client\'s Public Key received ")

    e, d, c = RSA.keygen(N_BITS,auto_gen_key)
    privateTuple = (e, c)
    sendPublic = str(d) + ',' + str(c)
    conn.send(sendPublic.encode())
    print ("# Public Key sent ")
  

    data = conn.recv(4096).decode()
    data = decrypt(data, publicTuple)


    if data != f"Client:{publicTuple[0]},{publicTuple[1]}":
        print ("\n* Encryption could not be verified! Please try to reconnect... *\n")
        conn.send("ABORT".encode())
        connClose(conn)
        return

    data = f"Server:{sendPublic}"
    data = encrypt(data, privateTuple,N_BITS)
    conn.send(data.encode())


    print ("\n* Connected to chat *\n----------------------------")
    print ("** Type \'end()\' to leave the conversation\n")

    Reciver  = MyThread('recive', conn,privateTuple)
    Sender = MyThread('send', conn,publicTuple)

    Reciver.start()
    Sender.start()

    Reciver.join()
    print ("\n* Clint ends the Connection \n ")

    Sender.kill()
    Sender.join()

    print ("** Closing all sockets and exiting... ")

    connClose(conn)

    connClose(server)


def Client(host, port):

    port = int(port)

  
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print ("\n# Connecting to server... \n")

    e, d, c = RSA.keygen(N_BITS,auto_gen_key)
    privateTuple = (e, c)
    sendPublic = str(d) + "," + str(c)
    client.send(sendPublic.encode())
    print ("# Public Key sent ")

 
    key = client.recv(4094).decode()
    key = key.split(',')
    publicTuple = (key[0], key[1])
    print ("# Server\'s Public Key received *")




    data = f"Client:{sendPublic}"
    data = encrypt(data, privateTuple,N_BITS)
    client.send(data.encode())


    data = client.recv(4094).decode()


   

    if data != "ABORT":
        data = decrypt(data, publicTuple)


    if data != f"Server:{publicTuple[0]},{publicTuple[1]}":
        print ("\n* Encryption could not be verified! Please try to reconnect... *\n")
        client.send("ABORT".encode())
        connClose(client)
        return
    else:
        print ("\n# Encryption Verified! #")

    print ("\n* Connected to chat *\n----------------------------")
    print ("** Type \'end()\' and hit Enter to leave the conversation\n")

    Reciver = MyThread('recive', client, privateTuple)
    Sender = MyThread('send', client,publicTuple)

    Reciver.start()
    Sender.start()

    Reciver.join()
    print ("\n* The Server ends the Connection")

    Sender.kill()
    Sender.join()

    print ("** Closing all sockets and exiting... ")

    connClose(client)


def encrypt(data, public,N_BITS):

    encrypted_data=RSA.encrypt(data, int(public[0]),int( public[1]),N_BITS)
    return encrypted_data


def decrypt(data, private):


    decrypted_data = RSA.decrypt(data, int(private[0]),int(private[1]))
    return decrypted_data


def connClose(conn):
    try:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    except:
        pass


class MyThread(threading.Thread):


    def __init__(self, action, conn, key):
 
        threading.Thread.__init__(self)
        self.action = action.lower()
        self.conn = conn
        self.killed = False
        self.exitcode = "end()"
        self.key=key

    def run(self):
        if self.action == 'recive':
            self.read()
        elif self.action == 'send':
            self.write()


    def kill(self):
        self.killed = True

    def read(self):

        while (not self.killed):

            data = self.conn.recv(4094).decode()
            if(data=="END()"):
                self.kill()
                continue

                
            data = decrypt(data, self.key)

            if(data == self.exitcode):
                self.conn.send("END()".encode())
                self.kill()
                continue

            print ("<msg>", data)



    def write(self):
 
        while (not self.killed):

            data = input()
            if (data == self.exitcode):
                print ("\n# Leaving conversation... ")
                self.kill()

            data = encrypt(data, self.key,N_BITS)
            self.conn.send(data.encode())

  




print ("")
print ("------------------------------------------------------")
print ("                 ENCRYPTED CHAT                       ")
print ("------------------------------------------------------")


if (len(sys.argv) < 3):
    print ("\nERROR (MISSING PARMATERS): python3 Chat.py <hostname/IP> <port>\n")
    exit(0)


host = sys.argv[1]
port = sys.argv[2]


try:
    Client(host, port)
except socket.error:

    print ("# Creating server... ")
    try:
        Server(host, port)
    except socket.error as err:
        print ("ERROR :cannot creating server \n")
    

print ("\n*** Exiting...")
