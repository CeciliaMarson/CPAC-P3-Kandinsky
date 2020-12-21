#%% Echo server program
import socket
import numpy as np

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    array=np.array([[100,50,120],[20,30,200]])
    print(array.shape)
    arr=''
    for i in range(0,array.shape[0]):
            a=str(array[i])
            arr=arr+a+' '
    
    #arr='25 55 86'
    print(arr)
    conn.send(str.encode(arr))
    conn.send(str.encode(str(array.shape[0]))) 
    data = conn.recv(1024)
    if not data: break
    print(data) # Paging Python!
    # do whatever you need to do with the data
   
conn.close()
# optionally put a loop here so that you start 
# listening again after the connection closes
# %%