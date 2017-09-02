import threading
from websocket_server import WebsocketServer
import time
import socket
import os
import random
import ftplib

tcp_server_bind_ip = ""
tcp_server_bind_port = 17789
tcp_server_maxclientnum = 5

websocket_server_port=9998

blockly_cmd=""
daemon_websocket_server = WebsocketServer(websocket_server_port)

tcpClient_list_connect=[]
tcpClient_list_name=[]

tensorflow_img_recognize = "tensorflowimg##"
maxmsp_cmdStart= "maxmsp#########"

# def clientIsTensorflow(clientName,tcp_server_recv):

isRpiMode = False
feature_takephoto = "takephoto"
photo_name = []


# task: tcp server
def tcpclient_thread(tcp_server_connect,clientIp,clientPort):
    print("[+] New server socket thread started for " + clientIp + ":" + str(clientPort))
    tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('ISO-8859-1')

    clientName = tcp_server_recv[0:15]
    print('client is ' + clientName)

    global tcpClient_list_connect
    tcpClient_list_connect.append(tcp_server_connect)
    global tcpClient_list_name
    tcpClient_list_name.append(clientName)

    daemon_websocket_server.send_message_to_all(tcp_server_recv)


    while True:
        try:
            tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('ISO-8859-1')
            print("client(" + clientIp + ":" + str(clientPort) + ")said: " + tcp_server_recv)
            daemon_websocket_server.send_message_to_all(tcp_server_recv)

            # inputMsg = input("Enter response to client(" + clientIp + ":" + str(clientPort) + "): ")
            # tcp_server_connect.send(inputMsg.strip().encode('utf-8'))
        except:
            print("client disconnect!")
            break
            
def tcp_server():
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind((tcp_server_bind_ip,tcp_server_bind_port))
    threads = []
    while True:
        tcp_server_socket.listen(tcp_server_maxclientnum)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (tcp_server_connect, (clientIp,clientPort)) = tcp_server_socket.accept()
        print('('+clientIp + ":" + str(clientPort)+')tcp_server_connect:' +tcp_server_connect)
#sarah3 what's this?

        childThread_tcpclient_thread = threading.Thread(target=tcpclient_thread, args=(tcp_server_connect,clientIp,clientPort))
        childThread_tcpclient_thread.start()
        threads.append(childThread_tcpclient_thread)

    for t in threads:
# sarah2 why after while need this, is it excuted? join() would block process until done
        t.join()

def my_websocket_server():
    daemon_websocket_server.set_fn_new_client(new_client)
    print("daemon is ready!")
    print("wait for blockly")
    daemon_websocket_server.set_fn_client_left(client_left)
    daemon_websocket_server.set_fn_message_received(message_received)
    daemon_websocket_server.run_forever()


def new_client(client, server):
#       print("client id %d" % client['id'])
#       daemon_websocket_server.send_message_to_all("defg")
        print("-----------------------")
        print("blockly in!")

def client_left(client, server):
#       print("Client(%d) disconnected" % client['id'])
        print("")


def message_received(client, server, message):
        if len(message) > 200:
                message = message[:200]+'..'
        global blockly_cmd
        blockly_cmd = message

        print("blockly said: %s" % (blockly_cmd))
        cmdToWho = blockly_cmd[0:15]
        print('cmd to who? ' + cmdToWho)
        if blockly_cmd.find(feature_takephoto):
            photo_name.append(random.randrange(9999999))
            os.system("raspistill -w 100 -h 100 -o "+str(photo_name[len(photo_name)-1])+".jpg")
            print("take photo: "+str(photo_name[len(photo_name)-1])+".jpg")
            session = ftplib.FTP('192.168.43.180','sarahcheng','tuhbnygj') 
            file = open(str(photo_name[len(photo_name)-1])+".jpg",'rb')
            session.storbinary('STOR '+"~/Desktop/tensorflow_db/rpi"+str(photo_name[len(photo_name)-1])+".jpg",file) 
            file.close()
            session.quit()
            daemon_websocket_server.send_message_to_all(str(photo_name[len(photo_name)-1])+".jpg")
            print("send photo successful")

        if not isRpiMode:
            print(str(tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)]))
            tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)].send((str(blockly_cmd)+'\n').encode('utf-8'))
            if cmdToWho == maxmsp_cmdStart:
# zeo1 why remove?
                tcpClient_list_connect.remove(tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)])
                tcpClient_list_name.remove(cmdToWho)
            print("send to client: " + blockly_cmd)
os.system("uname "+"-a > myEnv.txt")
if os.system("grep raspberry myEnv.txt") == 0:
    print("RPI mode!")
    isRpiMode = True

mainThread_websocket_server = threading.Thread(target=my_websocket_server, args=())
mainThread_websocket_server.start()
mainThread_tcp_server = threading.Thread(target=tcp_server, args=())
mainThread_tcp_server.start()

mainThread_tcp_server.join()
mainThread_websocket_server.join()
