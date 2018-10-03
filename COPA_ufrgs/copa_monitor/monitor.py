import socket
import json
from control import StateMachine
from pprint import pprint

if __name__ == '__main__':
    host = "0.0.0.0"
    port = 5000
    state_machine = StateMachine()
    
    my_socket = socket.socket()
    my_socket.bind((host,port))

    #while True:
    my_socket.listen(1)
    
    while True:
        try:
            print("State: "+state_machine.get_state())

            if state_machine.get_state() == "not_connected":
                print("Waiting connection...")
                conn, addr = my_socket.accept()
                print("Connection from: " + str(addr))
                state_machine.set_state("wait_register")
                state_machine.set_experimentserver(addr[0])

            data = conn.recv(1024).decode()

            if not data:
                state_machine.set_state("not_connected")
                conn.close()
                state_machine.loopthread.stop_thread()
                state_machine.loopthread.join()
                continue
            else:
                data = json.loads(data)
            
            response = state_machine.do_action(data["action"], data["data"])
            
            print ("from connected  user: " + str(data))
            print ("sending: " + str(response))
            conn.send(json.dumps(response).encode())

        except:
            if conn:
                conn.close()
            
            my_socket.close()
            
            state_machine.loopthread.stop_thread()
            state_machine.loopthread.join()
            break
            
    