#!/usr/bin/env python
#coding=utf-8

import socket
import re

HOST = '127.0.0.1'
PORT = 8000
ibutton = 0
#Read index.html, put into HTTP response data
index_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

'''

file = open('G:\working\python\web-server\Http\index.html', 'r')
index_content += file.read()
file.close()

#Read reg.html, put into HTTP response data
reg_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

'''

file = open('G:\working\python\web-server\Http\plain.html', 'r')
reg_content += file.read()
file.close()

#read ibutton value
ibutton_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

'''
file = open('G:\working\python\web-server\Http\Michael_button.html', 'r')
ibutton_content += file.read()
file.close()

def run(svr_status):
    global ibutton,index_content,reg_content,ibutton_content
    #Configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)
     
    while True:
        print("waiting for connect client...")
        # maximum number of requests waiting
        conn, addr = sock.accept()
        print(addr)
            #define info connect server successfully
        msg = "connect server successfully\r\n"
        conn.send(msg.encode())
        #infinite loop
        while True:
            try:
            #global ibutton
                request_o = conn.recv(1024)
                print(request_o.decode())
                request = str(request_o)
            except:
                msg = "disconnect server\r\n"
                conn.send(msg.encode())
                conn.close()
                print("client CLOSE & disconnect\r\n")
                break
            else:
                if not request_o:
                    msg = "will disconnect server\r\n"
                    conn.send(msg.encode())  
                    print("jump loop1")
                    break
                elif request_o == b'!exit server#':
                    msg = "will disconnect server\r\n"
                    conn.send(msg.encode())  
                    print("jump loop1_exit")
                    break
                print ('Request is:\n', request)
                method = request.split(' ')[0]
                print ('method is:\n', method)
                src  = request.split(' ')[1]


                print ('src is:\n', src)


                #deal wiht GET method
                if method == 'GET':
                    if src == '/index.html':
                        content = str(index_content).encode()
                    elif src == '/plain.html':
                        content = reg_content
                    elif src == '/Michael_button.html':
                        content = ibutton_content
                    elif re.match('/ibutton', src):
                        entry = 'ibutton'+str(ibutton)   # main content of the request
                        content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
                        content += entry
                        content += '<br /><font color="green" size="7">register successs!</p>'
                    else:
                        continue

                
                #deal with POST method  
                elif method == 'POST':
                    form = request.split('\r\n')
                    if re.match('/ibutton', form):
                        ibutton = 1
                    entry = form[-1]      # main content of the request
                    content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
                    content += entry
                    content += '<br /><font color="green" size="7">register successs!</p>'
                
                ######
                # More operations, such as put the form into database
                # ...
                ######
                
                else:
                    continue

                conn.sendall((str(content)).encode)      
        conn.close()
        print("& disconnect client\r\n")
        if request_o == b'!exit server#':
            print("Jump out intern loop2\r\n")
            break        
    sock.close()
    print("socket CLOSE\r\n")
if __name__ == "__main__":
	#sendKeepConnectTimer(5)
    run(0)