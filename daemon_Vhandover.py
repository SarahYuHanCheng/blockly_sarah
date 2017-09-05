from websocket_server import WebsocketServer
import time
import threading
# -----------old Version -------------
# import _thread
# -----------old Version -------------
import socket
import os

#global variable
tcp_server_bind_ip = ""
tcp_server_bind_port = 17784
tcp_server_maxclientnum = 5

tcp_client_destination_ip = "127.0.0.1"
tcp_client_destination_port = 16673

websocket_server_port=9998

blockly_cmd=""
led_on_time=0
daemon_websocket_server = WebsocketServer(websocket_server_port)
tcpClient_list_connect=[]
tcpClient_list_name=[]

# -----------old Version -------------
# tcp_server_connect = None
# -----------old Version -------------

who_is_client=""

arduino_uno=             "arduinouno#####"
raspberry_pi=            "reaspberrypi###"
maxmsp=                  "maxmsp#########"
puredata=                "puredata#######"
tensorflow_img_recognize="tensorflowimg##"

selectedImg = 'noimage'


# -----------old Version -------------
# def judgeClient(wrapper_fileIsSend,tcp_server_recv):        

#     global who_is_client
#     who_is_client = tcp_server_recv[0:15] # arduinouno#####
#     print('client is ' + who_is_client)

#     if who_is_client.find(arduino_uno)!=-1:
#         daemon_websocket_server.send_message_to_all(tcp_server_recv)
#         pass
#     elif who_is_client.find(maxmsp)!=-1:
#         daemon_websocket_server.send_message_to_all(tcp_server_recv)
#         pass
#     elif who_is_client.find(puredata)!=-1:
#         daemon_websocket_server.send_message_to_all(tcp_server_recv)
#         pass
#     elif who_is_client.find(tensorflow_img_recognize)!=-1:
#         print('fileIsSend' + str(wrapper_fileIsSend[0]))
#         if wrapper_fileIsSend[0]==True: #sarah 什麼時候會是true           
#             daemon_websocket_server.send_message_to_all(tcp_server_recv)
#             print(tcp_server_recv)
#             if tcp_server_recv.find('saveToDbSuccessful') !=-1 :
#                 wrapper_fileIsSend[0]=False
#                 print('reset fileIsSend state to '+str(wrapper_fileIsSend))
                
#         else :
#             clientIsTensorflow(wrapper_fileIsSend)
# -----------old Version -------------


                    
        
def tcpclient_thread(tcp_server_connect,clientIp,clientPort,wrapper_fileIsSend):
    print("[+] New server socket thread started for " + clientIp + ":" + str(clientPort))
    tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('ISO-8859-1')
    global tcpClient_list_connect
    global tcpClient_list_name
    clientName = tcp_server_recv[0:15]
    print('client is ' + clientName)
    if clientName in tcpClient_list_name:
        tcpClient_list_connect[tcpClient_list_name.index(clientName)]=tcp_server_connect
        print("replace the connect info")

    else:
        # global tcpClient_list_connect
        tcpClient_list_connect.append(tcp_server_connect)
        tcpClient_list_name.append(clientName)
        print("append")

    daemon_websocket_server.send_message_to_all(clientName)#tcp_server_recv
    if clientName.find(tensorflow_img_recognize)!=-1:
        print('fileIsSend' + str(wrapper_fileIsSend[0]))
        if wrapper_fileIsSend[0]==True:            
            daemon_websocket_server.send_message_to_all(tcp_server_recv)
            print(tcp_server_recv)  # tensorflowimg##tensorflowPrediction#[5 5]


                
        else :
            clientIsTensorflow(wrapper_fileIsSend,tcp_server_connect)


    while True: # 若tensorflow close 這裡應該會跳excpt, why not？
        try:
            tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('ISO-8859-1')
            print("client(" + clientIp + ":" + str(clientPort) + ")said: " + tcp_server_recv)
            daemon_websocket_server.send_message_to_all(tcp_server_recv)
            if tcp_server_recv.find('saveToDbSuccessful') !=-1 :
                wrapper_fileIsSend[0]=False
                print('reset fileIsSend state to '+str(wrapper_fileIsSend))
                tcp_server_connect.close() # why not work?
                # thread.exit()
            # inputMsg = input("Enter response to client(" + clientIp + ":" + str(clientPort) + "): ")
            # tcp_server_connect.send(inputMsg.strip().encode('utf-8'))
        except:
            print("client disconnect! thread die") # thread die?
            break
def clientIsTensorflow(wrapper_fileIsSend,tcp_server_connect):
    
    print('fileIsSend' +  str(wrapper_fileIsSend[0]))
    while not  wrapper_fileIsSend[0]:
         
        tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('utf-8')# sarah 會在這裡等訊息傳來嗎
        print("not wait")# sarah
        print(tcp_server_recv)
        if tcp_server_recv.find('fileBufferIsReady')!=-1:
            img_size = os.stat(selectedImg).st_size
            print('file size=' + str(img_size))

            mb = float(img_size) / 1024
            mb = mb + 1
            print(mb)
##                            tcp_server_connect, address = tcp_server_socket.accept()
            while True:
                filename=selectedImg
                f = open(filename,'rb')
                l = f.read(1024)

                while (l and mb>0):
                       mb = mb-1         
                       print(mb)
                       tcp_server_connect.send(l)
                       #print('Sent ',repr(l))  
                       l = f.read(1024)
                       if mb<0:
                            f.close()
                            print('Done sending')
                            # casue error    
                            #tcp_server_connect.send('Thank you for connecting')
                                                                       
                            tcp_server_connect.close()
                            tcp_server_recv=None
                if tcp_server_recv==None:
                        wrapper_fileIsSend[0]=True
                        
                        break        

# task: tcp server
def tcp_server():

        tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #for udp
        tcp_server_socket.bind((tcp_server_bind_ip,tcp_server_bind_port))
        threads = []
        fileIsSend=False
        wrapper_fileIsSend=[fileIsSend]
        while True:
            tcp_server_socket.listen(tcp_server_maxclientnum)
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            (tcp_server_connect, (clientIp,clientPort)) = tcp_server_socket.accept()

            childThread_tcpclient_thread = threading.Thread(target=tcpclient_thread, args=(tcp_server_connect,clientIp,clientPort,wrapper_fileIsSend))
            childThread_tcpclient_thread.start()
            threads.append(childThread_tcpclient_thread)

        for t in threads:
# sarah2 why after while need this, is it excuted? join() would block process until done
            t.join()

# -----------old Version -------------
#         if tcp_server_connect!=None:
#                 # note user that client(Arduino,PD,Max/Msp...) has connect with daemon(tcp_server)
#                 # print client's (ip,port)
#                 print("client" + str(address) + " in!")
#                 print("-----------------------")
#         fileIsSend=False
#         wrapper_fileIsSend=[fileIsSend] #sarah only used by tensorflow
#         while True:
#             # can't put in here, otherwise can only recv one message
# ##            global tcp_server_connect
# ##            tcp_server_connect, address = tcp_server_socket.accept()
            
#             try:
#                 if tcp_server_connect!=None:
#                         tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('utf-8')
#                 print("client said: " + tcp_server_recv)
#                 # check the connection with client(Arduino,PD,Max/Msp...)
#                 if tcp_server_recv!=None and tcp_server_connect!=None: #為什麼不是寫在上一個判斷裡面？只要沒有remove應該就不會等於None，client斷線他應該也不改變？
#                     if tcp_server_recv != "":
#                         print("client said: " + tcp_server_recv)
#                         #send client's(Arduino,PD,Max/Msp...) response to blcokly by websocket
                   
#                         judgeClient(wrapper_fileIsSend,tcp_server_recv)

#                     # in case of connection had fail (Max/Msp)
#                     elif tcp_server_recv=="":
#                         tcp_server_connect, address = tcp_server_socket.accept()
#                         # print client's (ip,port)
#                         print("(elif)client reconnect" + str(address) + " success!")
#                     else :
#                         tcp_server_connect, address = tcp_server_socket.accept()
#                         print("(else)client reconnect" + str(address) + " success!")
#             except socket.error as msg:
#                 print("connection failed, reconnecting...")
#                 tcp_server_connect, address = tcp_server_socket.accept()

#                 # resend the msg before the reconnection
# ##                tcp_server_connect.send(str(led_on_time))
#                 tcp_server_recv = (tcp_server_connect.recv(1024)).strip().decode('utf-8')
#                 if tcp_server_recv!=None and tcp_server_connect!=None:
#                     print("recv from client: " + tcp_server_recv)
#                     print("(except)client said: "+str(address))
#                     judgeClient(wrapper_fileIsSend,tcp_server_recv)
#                 continue

##        tcp_server_connect.close()
##        if msg=="quit":
##          os._exit()
# -----------old Version -------------

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
        print(str(tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)]))
        if cmdToWho == maxmsp:
            tcpClient_list_connect.remove(tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)])
            tcpClient_list_name.remove(cmdToWho)
            tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)].send((str(blockly_cmd)+'\n').encode('utf-8'))
        elif cmdToWho.find(tensorflow_img_recognize)!= -1:
            if blockly_cmd.find('sendImgToTensorflow')!=-1:
                    tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)].send((tensorflow_img_recognize+'readyTheFileBuffer').encode('utf-8'))
                    global selectedImg
                    selectedImg = blockly_cmd[blockly_cmd.index('file://')+6:len(blockly_cmd)]
                    print('select image: ' + selectedImg)
                    print('daemon send to client: readyTheFileBuffer')
            else:
                tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)].send(blockly_cmd.encode('utf-8'))
                print("send to client: " + blockly_cmd)
        else:    
            print("send to client: " + blockly_cmd)
            tcpClient_list_connect[tcpClient_list_name.index(cmdToWho)].send((str(blockly_cmd)+'\n').encode('utf-8'))

# ----------- old Version -------------
        # #check the connection with client(Arduino,PD,Mas/Msp...)
        # if tcp_server_connect != None :
        #     end=""

        #     #pure data need follow FUDI protocol which need add a ";" at the end of message
        #     if who_is_client.find(puredata)!=-1:
        #         end=";"
        #         tcp_server_connect.send((blockly_cmd+end).encode('utf-8'))# sarah
        #     if who_is_client.find(tensorflow_img_recognize)!=-1:
        #         # recv from blockly:(example) tensorflowimg##sendImgToTensorflow#file:\D:\images\tofu.jpg
        #         if blockly_cmd.find('sendImgToTensorflow')!=-1:
        #             tcp_server_connect.send((tensorflow_img_recognize+'readyTheFileBuffer').encode('utf-8'))
        #             global selectedImg
        #             selectedImg = blockly_cmd[blockly_cmd.index('file://')+6:len(blockly_cmd)]
        #             print('select image: ' + selectedImg)
        #             print('daemon send to client: readyTheFileBuffer')
        #         else:
        #             tcp_server_connect.send(blockly_cmd.encode('utf-8'))
        #             print("send to client: " + blockly_cmd)
        #     else:                            
        #         #send the blockly cmd to client
        #         #client means puredata, arduino, raspberry pi...
        #         tcp_server_connect.send((blockly_cmd+end).encode('utf-8'))                            
        #         print("send to client: " + blockly_cmd + end)
        # else:
        #     print("check the client with client.")
# ----------- old Version -------------

# task: websocket server
def my_websocket_server():
##    while 1:
        daemon_websocket_server.set_fn_new_client(new_client)
        print("daemon is ready!")
        print("wait for blockly")

        daemon_websocket_server.set_fn_client_left(client_left)
        daemon_websocket_server.set_fn_message_received(message_received)
        daemon_websocket_server.run_forever()




mainThread_websocket_server = threading.Thread(target=my_websocket_server, args=())
mainThread_websocket_server.start()
mainThread_tcp_server = threading.Thread(target=tcp_server, args=())
mainThread_tcp_server.start()

mainThread_tcp_server.join()
mainThread_websocket_server.join()

# -----------old Version -------------
# try:
#         #blockly will connect to websocket server
#         _thread.start_new_thread(my_websocket_server,("task: websocket server",))
#         #client(Arduino,PD,Max/Msp...) will connect to tcp server
#         _thread.start_new_thread(tcp_server,("task: tcp server",))
# ##        thread.start_new_thread(tcp_client,("task: tcp client",))

# except:
#         print("error: thread fail")
# while 1:
#         pass
# -----------old Version -------------