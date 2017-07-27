from websocket_server import WebsocketServer
import time
import _thread
import socket
import os

#global variable
tcp_server_bind_ip = "192.168.1.179"
tcp_server_bind_port = 17784
tcp_server_maxclientnum = 5

websocket_server_port=9998


# blockly_cmd="192.168.1.179"
led_on_time=0
daemon_websocket_server = WebsocketServer(websocket_server_port)
tcp_server_connect = None

who_is_client=""

def judgeClient(wrapper_fileIsSend,tcp_server_recv):        

    global who_is_client
    who_is_client = tcp_server_recv[0:15]
    daemon_websocket_server.send_message_to_all(tcp_server_recv)
    print("send to client: " +who_is_client)

# task: tcp server
def tcp_server(threadName):
        global who_is_client
        print("\n%s" % threadName)

        tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_server_socket.bind((tcp_server_bind_ip,tcp_server_bind_port))
        tcp_server_socket.listen(tcp_server_maxclientnum)

        global tcp_server_connect
        tcp_server_connect, address = tcp_server_socket.accept()

        if tcp_server_connect!=None:
                # note user that client(Arduino,PD,Max/Msp...) has connect with daemon(tcp_server)
                # print client's (ip,port)
                print("client" + str(address) + " in!")
                print("-----------------------")
        fileIsSend=False
        wrapper_fileIsSend=[fileIsSend] 
        while True:
            # can't put in here, otherwise can only recv one message
#
            try:
                if tcp_server_connect!=None:
                        tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('utf-8')
                # print("client said: " + tcp_server_recv)
                # check the connection with client(Arduino,PD,Max/Msp...)
                if tcp_server_recv!=None and tcp_server_connect!=None:
                    if tcp_server_recv != "":
                        print("client said: " + tcp_server_recv)
                        #send client's(Arduino,PD,Max/Msp...) response to blcokly by websocket
                   
                        judgeClient(wrapper_fileIsSend,tcp_server_recv)
                    # in case of connection had fail (Max/Msp)
                    elif tcp_server_recv=="":
                        tcp_server_connect, address = tcp_server_socket.accept()
                        # print client's (ip,port)
                        print("(elif)client reconnect" + str(address) + " success!")
                    else :
                        tcp_server_connect, address = tcp_server_socket.accept()
                        print("(else)client reconnect" + str(address) + " success!")
            except socket.error as msg:
                print("connection failed, reconnecting...")
                tcp_server_connect, address = tcp_server_socket.accept()

                # resend the msg before the reconnection
##                tcp_server_connect.send(str(led_on_time))
                tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('utf-8')
                if tcp_server_recv!=None and tcp_server_connect!=None:
                    print("recv from client: " + tcp_server_recv)
                    print("(except)client said: "+str(address))
                    judgeClient(wrapper_fileIsSend,tcp_server_recv)
                continue




def new_client(client, server):
        
        blocky_client = client
#       print("client id %d" % client['id'])
#       daemon_websocket_server.send_message_to_all("defg")
        print("-----------------------")
        print("blockly in!"+str(client['address']))

def client_left(client, server):
#       print("Client(%d) disconnected" % client['id'])
        print("left")

# WebSocketerver recv  noted by sarah 0712
def message_received(client, server, message):
        if len(message) > 200:
                message = message[:200]+'..'
        global blockly_cmd
        blockly_cmd = message
        global led_on_time
##        led_on_time = (int)(filter(str.isdigit, blockly_cmd))

        print("blockly said: %s" % (blockly_cmd))
        
        #check the connection with client(Arduino,PD,Mas/Msp...)
        if tcp_server_connect != None :
            end=""
            tcp_server_connect.send((blockly_cmd+end).encode('utf-8'))
            print('client is:'+who_is_client)
            # print("send to client: " + blockly_cmd + end)
        else:
            print("check the client with client.")
# task: websocket server
def my_websocket_server(threadName):
##    while 1:
        print("\n%s" % threadName)
        daemon_websocket_server.set_fn_new_client(new_client)
        print("daemon is ready!")
        print("wait for blockly")
        daemon_websocket_server.set_fn_client_left(client_left)
        daemon_websocket_server.set_fn_message_received(message_received)
        daemon_websocket_server.run_forever()

try:
        #blockly will connect to websocket server
        _thread.start_new_thread(my_websocket_server,("task: websocket server",))
        #client(Arduino,PD,Max/Msp...) will connect to tcp server
        # _thread.start_new_thread(tcp_server,("task: tcp server",))
##        thread.start_new_thread(tcp_client,("task: tcp client",))

except:
        print("error: thread fail")
while 1:
        pass
