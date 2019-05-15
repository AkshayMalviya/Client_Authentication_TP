---------- Running on Windows/Linux via command line: ----------

This system is compatible with Python version 3.5 and above.

********** Initialising and starting the system **********
Step one: create Users table first
- open a command line
- navigate to the folder where the system is stored
- edit create_table.py and change the database name whatever you like at line 
	conn = sqlite3.connect('test1.db') To conn = sqlite3.connect('yourDatabaseName.db')
- now edit the entries in table at line "c.execute("INSERT INTO users(uname,upass) VALUES ('username1','password1'),('username2','password2'),('username3','password3')")" enter your username and passwords in place of username1/2/3 and password1/2/3
- run "python create_table.py"

Step two: open get_from_table.py
- now edit get_from_table.py and set the dataBaseName at line "conn = sqlite3.connect('test1.db')" TO "conn = sqlite3.connect('yourDataBaseName.db')"
- save the file
- now follow the README.txt


********** using the system **********
- Once the server and the client programs are running, you can search for songs 
associate with specific artists via the client program.
- The client prompts you to enter the name of an artist. Enter a name from the 
songs.txt file, e.g., ABBA. The client then returns the songs for Abba

********** Shuting down the system **********
- To close client connection with the server, but leaving server running 
(e.g., allow another client to connect) enter 'quit' from the client's command line window.
- To close the connection and abort the system enter 'close' form the client's command line window

Notes:
- Log files do not get overwritten! Delete them to get fresh log files.
- If server is forcibly closed then log file will not be written.