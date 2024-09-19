### Importing necessary libraries for local functions
import mysql.connector
import random
import string

### Connecting to Keys MySQL
print("Connecting to the MySQL Database (Access)") # Debug Message
access = mysql.connector.connect(
  host="", # Connecting to the following Address
  port=,				   # Connecting to the following Port
  user="",	   # Connecting with the following Username
  password="", # Connecting with the following Password
  database=""			   # Connecting to the following Database
)
mycursor = access.cursor(buffered=True) # Defining the Cursor the execute MySQL commands
print("Successfully estabilished MySQL Connection (Access)") # Debug Message
### Functions

## Status Functions

def validate_access_key(access_key, req_permission_integer): # Function for validating an access key and its permission level. Required parameters are access key and the required permission integer.
    sql = f"SELECT * FROM access_keys WHERE access_key ='{access_key}'" # Command for selecting the row of the access key
    mycursor.execute(sql) # Command Execution of the Selection Process
    myresult = mycursor.fetchall() # Fetching the results of the executed command
    record_exists = mycursor.rowcount # Checking if search parameter has got a result
    
    if record_exists == 0: # Validating result
        return -1 # Returning to another functions file that the access key was invalid
    
    permission_level = myresult[0][2] # Fetching the permission integer out of the results
    
    if req_permission_integer <= permission_level: # Checking if the required permission level is under the permission level of the access key
        return 1 # Returning to another functions file that the access key was valid and sufficient enough for the command execution
    
    else: # Executed if permission level of the access key was too low
        return 0 # Returning to another functions filt that the access key was valid but insufficient to execute the command

## Maintenance Functions

def add_access_key(perm_integer, notes=None): # Function for adding access keys to the system. Required parameter is permission level. Optional parameter is notes.
    letters = string.ascii_letters + string.digits # Defining the allowed characters for random access key creation
    access_key = str('access-'+''.join(random.choice(letters) for i in range(16))) # Key generation process
    sql = "INSERT INTO access_keys (access_key, permission_integer, notes) VALUES (%s, %s, %s)" # Command for inserting the given data
    val = (access_key, perm_integer, notes) # Values for the insertion process
    mycursor.execute(sql, val) # Executing the insertion process
    access.commit() # Saving the changes to the MySQL database
    return access_key # Returning the access key to the main file
