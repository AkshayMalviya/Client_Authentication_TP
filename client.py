import socket
import datetime
import pdb

def write_response(start, finish, artist, length):
    # This writes information to the log file 'client.log
    new_file = open("client.log", 'a+')
    new_file.write("Server took {} to complete the request for '{}' ".format(str(finish - start), artist))
    new_file.write("\nThe response length was {} bytes ".format(str(length)))
    new_file.write("\nThe response was received on {} \n".format(str(datetime.datetime.now())))
    new_file.write("\n\n")
    new_file.close()


class RunningConnection:
    def __init__(self):
        # Initialise the socket and address
        self.sock = socket.socket(socket.AF_INET)
        server_address = ('localhost', 6666) #change port number if necessary. If changed here you should also change it in the server.py program.
        print('connecting to %s on port %s' % server_address)
        try:
            # Set a timeout for the connection to allow it to fail if another client is already connected
            self.sock.settimeout(20)
            # Attempt to connect to the server
            self.sock.connect(server_address)
            user_name = input("UserName ")  #User input user_name
            password = input("Password ")   #User input password

            #Sending data to server in encoded format utf-8
            self.sock.send(user_name.encode()) 
            self.sock.send(password.encode())
            
            print("Waiting to connect to the server...")
            #Received response from server and if got code 0 at end in response then exit()
            res = self.sock.recv(1024).decode()
            print(res)     
            if res[-1:] == '0': exit() 
        except socket.timeout:
            # Catch a timeout error
            print("There was a timeout error, as another user is already connected to the server!")
            print("No other connections will be able to be made to the server whilst it is running.")
            exit()
        except socket.error:
            # Catch any other errors that may arise, such as the server not running
            print("There was an error connecting to the server as it is not available/running.")
            exit()

    def running(self):
        try:
           
			# Loop until the user inputs close or quit	
            while 1:
                message = ''
                # Loop until the user inputs a message (No blank message)
                while message == '':
                    message = input("What artist would you like to search for? ") # Getting the name of an artists from a user
                    
                    if message == '': # simple error checking
                        print("ERROR: You should not send an empty message!")

                # Send the message to the server
                self.sock.sendall(message.encode())
                # Set the time that the message was sent
                start_time = datetime.datetime.now()

                # If the user input 'quit' or 'close', exit the while loop and close the connection
                if message == 'quit' or message == 'close':
                    print("Disconnecting!")
                    break

                # Output what the user is sending to the terminal
                print('You are sending "%s" message to the server: ' % message)

                # Receive a response from the server
                data = self.sock.recv(39)
                print(data.decode())
                data = self.sock.recv(1024)

                # 'error' is returned if no songs are found, otherwise the songs are displayed on the terminal
                if data.decode() == 'error':
                    print("There are no songs under the author", message)
                else:
                    print("The songs made by ", message, "are:")
                    print(data.decode())

                # Set the finish time, and call the function to write to the log file
                finish_time = datetime.datetime.now()
                write_response(start_time, finish_time, message, len(data))
                print("\nType in 'quit' to disconnect, or 'close' to quit and shut down the server!\n")
        except socket.timeout:
            # Catch a timeout error
            print("There was a timeout error!")
            self.sock.sendall('quit'.encode())
            self.sock.close()
            exit()
        except socket.error:
            # Catch any other errors that may arise, such as the server not running
            print("There was an error with the connection!")
            exit()
        finally:
            # Close the connection
            self.sock.close()


connect_client = RunningConnection()
connect_client.running()
