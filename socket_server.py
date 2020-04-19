import socket
from datetime import datetime
from threading import Timer
ibutton = 0
sendKeepConnect_flg = 0
def sendKeepConnectTimer(inc):
    global sendKeepConnect_flg 
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    msg = "connect client successfully\r\n"
    #返回信息
    #注意 python3.x以上，网络数据的发送接收都是byte类型
    #如果发送的数据是str型，则需要编码
    #conn.send(msg.encode())
    sendKeepConnect_flg = 1
    t = Timer(inc,sendKeepConnectTimer,(inc,))
    t.start()

def run(svr_status):
    global ibutton,connect_status
    #sendKeepConnectTimer(5)
    #默认tcp方式传输
    #sendKeepConnectTimer(5)
    sk=socket.socket()
    #绑定IP与端口
    ip_port=('127.0.0.1',9999)
    #ip_port=('192.168.1.124',9999)
    #绑定监听
    sk.bind(ip_port)
    #最大连接数
    sk.listen(5)
    #不断循环 接受数据
    while True:
        #提示信息
        print("waiting for connect client...")
        #接受数据  连接对象与客户端地址
        conn, address = sk.accept()
        print(address)
        #定义信息
        msg = "connect server successfully\r\n"
        #返回信息
        #注意 python3.x以上，网络数据的发送接收都是byte类型
        #如果发送的数据是str型，则需要编码
        conn.send(msg.encode())
        #不断接收客户端发来的消息
        while True:
            print("waiting for receiving client data...")
            try:
                #接收客户端消息
                Rev_data = conn.recv(1024)
                print(Rev_data.decode())
            except:
                    conn.close()
                    print("client CLOSE & disconnect\r\n")
                    break
            else:
                
                #default as 0: LED Off
                if Rev_data == b'ibutton=0':
                    ibutton=0
                    print("ibutton:",ibutton)
                #1: LED On
                elif Rev_data == b'ibutton=1':
                    ibutton=1
                    print("ibutton:",ibutton)
                #接收到退出指令
                elif not Rev_data:
                    print("jump loop1")
                    break
                elif Rev_data == b'!exit#':
                    print("jump loop1_exit")
                    break
                #处理客户端信息 本实例直接将接收到的消息重新发回去
                if Rev_data == b'get ibutton':
                    send_data = b'ibutton='+str(ibutton).encode()+b'\r\n'
                    conn.send(send_data)
        #主动关闭连接
        conn.close()
        print("& disconnect client\r\n")
        if Rev_data == b'!exit#':
            print("Jump out intern loop2\r\n")
            break
    sk.close()
    print("socket CLOSE\r\n")
if __name__ == "__main__":
	#sendKeepConnectTimer(5)
    run(0)