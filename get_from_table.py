import sqlite3
#Using sqlite3 as Database


class AuthenticateUser:
	def __init__(self,uname,upass):
		#Initializing the class attributes
		self.uname = uname 
		self.upass = upass
	def validate_user(self):		
		conn = sqlite3.connect('test1.db')  #Establish the connection with specified Database
		conn.row_factory = sqlite3.Row  #Means want return result in form of rows instead of tuples which is default return type
		c = conn.cursor() #Initializing cursor		
		rr = c.execute('SELECT * FROM users where uname = ? and upass = ? LIMIT 1',(self.uname,self.upass)) #Execute desired query
		data_retruned = False
		for row in rr:	
			data_retruned = True
			print(row[0])

		return data_retruned  #If user exists then True else False

		 

