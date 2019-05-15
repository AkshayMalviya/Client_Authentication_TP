import socket
import re
import datetime
import pdb
import get_from_table


def write_startup():
    # Write information to the log file 'server.log'
    new_file = open("server.log", 'a+')
    new_file.write("Server started {} \n".format(str(datetime.datetime.now())))
    new_file.close()

def write_connection():
    # Write information to the log file

    new_file = open("server.log", 'a+')
    new_file.write("Client connected at {} ".format(str(datetime.datetime.now())))
    new_file.write("\nConnection was successful! ")
    new_file.close()

def write_disconnection(start):
    # Write information to the log file
    new_file = open("server.log", 'a+')
    connection = datetime.datetime.now() - start
    new_file.write("\nClient was connected for {} \n".format(str(connection)))
    new_file.write("\n")
    new_file.close()

def write_data(data):
    # Write information to the log file
    new_file = open("server.log", 'a+')
    new_file.write("\nClient requested songs under the artist name {} ".format(data))
    new_file.close()

class ReadingFile:
    def __init__(self):
        # Create regex that will be used for reading the file 'songs.txt
        self.start_line = re.compile('\S')
        self.end_line = re.compile('\d')

    def read_file(self, f_name):
        all_songs_dictionary = {}
        new_file = open(f_name, 'r')
        i = 0
        # Adds 100 songs to the dictionary
        while i < 100:
            hold = new_file.readline()
            # Calls the check function
            test = self.check(hold)

            # Adds the song and artist/artists to the dictionary
            if test == 'full':
                song = hold[4:34].strip()
                author = hold[35:-6].strip()
                for x in author.split('/'):
                    for y in x.split(' featuring '):
                        all_songs_dictionary.setdefault(y, []).append(song)
                i += 1
            elif test == 'name':
                song = hold[4:-1].strip()
                author = new_file.readline()[:-6].strip()
                all_songs_dictionary.setdefault(author, []).append(song)
                i += 1
        new_file.close()
        return all_songs_dictionary

    def check(self, full_line):
        # Uses the regex created previously to check that a line is valid
        if self.start_line.match(full_line[:1]):
            if self.end_line.match(full_line[-4:]):
                # This is when a full line has all the information
                return 'full'
            # This is when 2 lines contain all the information
            return 'name'
        else:
            # This is when the line is not required
            return 'none'


class Server:
    def __init__(self, songs):
        # Initialise the socket and address
        self.server_socket = socket.socket(socket.AF_INET)
        server_address = ('localhost', 6666) ## change if necessary, if changed here you should also change in the client.py program.
        print('Starting up on %s port %s' % server_address)
        try:
            # Attempt to start the server
            self.server_socket.bind(server_address)
            write_startup()
            # Listen for a connection
            self.server_socket.listen(0)
        except socket.error:
            # Catch any errors, such as the port being in use
            print("The server failed to initialise as the socket is already in use!")
            exit()
        self.song_dictionary = songs

    def running(self):	    
        # Wait for a connection
        # The while loops means that the server will keep listening after a client disconnects, unless they send 'close'		
        while 1:
            print('Waiting for a connection')
            connection, client_address = self.server_socket.accept()

            #Received request from client decoding in utf-8
            uName = connection.recv(1024).decode()
            uPass = connection.recv(1024).decode()
            #Authenticating user from database if valid user then continue else exit
            valid_user = get_from_table.AuthenticateUser(uName,uPass)            
            if valid_user.validate_user():
                connection.send("Successful connection! 1".encode())                
            else:
                connection.send("Authentication Failed! 0".encode())                
            try:
                # Output that a client has connected
                print('connection from', client_address)
                write_connection()
                # Set the time that the client connected
                start_time = datetime.datetime.now()
		
                # Loop until the client disconnects from the server
                while 1:
                    # Receive information from the client
                    data = connection.recv(1024).decode()
                    if (data != 'quit') and (data != 'close'):
                        print('received "%s" ' % data)
                        connection.send('Your request was successfully received!'.encode())
                        write_data(data)
                        # Check the dictionary for the requested artist name
                        # If it exists, get all their songs and return them to the user
                        if data in self.song_dictionary:
                            songs = ''
                            for i in range(len(self.song_dictionary.get(data))):
                                songs += self.song_dictionary.get(data)[i] + ', '
                            songs = songs[:-2]
                            print('sending data back to the client')
                            connection.send(songs.encode())
                            print("Sent", songs)
                        # If it doesn't exist return 'error' which tells the client that the artist does not exist
                        else:
                            print('sending data back to the client')
                            connection.send('error'.encode())
                    else:
                        # Exit the while loop
                        break
                # Write how long the client was connected for
                write_disconnection(start_time)
            except socket.error:
                # Catch any errors and safely close the connection with the client
                print("There was an error with the connection, and it was forcibly closed.")
                write_disconnection(start_time)
                connection.close()
                data = ''
            finally:
                if data == 'close':
                    print('Closing the connection and the server')
                    # Close the connection
                    connection.close()
                    # Exit the main While loop, so the server does not listen for a new client
                    break
                else:
                    print('Closing the connection')
                    # Close the connection
                    connection.close()
                    # The server continues to listen for a new client due to the While loop
                    

read = ReadingFile()
dictionary = read.read_file("songs.txt")
running_server = Server(dictionary)
running_server.running()


