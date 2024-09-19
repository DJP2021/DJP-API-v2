### Importing necessary libraries for local functions
import mysql.connector
print("Started Loading Key Functions")
import smtp_functions as mail
import balance_functions as balance
import random
import string

### Connecting to Keys MySQL
print("Estabilishing a MySQL Connection (Keys)") # Debug Message
keys = mysql.connector.connect(
  host="djp-industries-djpapi.d.aivencloud.com", # Connecting to the following Address
  port=20164,				   # Connecting to the following Port
  user="avnadmin",	   # Connecting with the following Username
  password="AVNS_m2Nj-w9VIhMYMoQmeJu", # Connecting with the following Password
  database="defaultdb"			   # Connecting to the following Database
)
print("Successfully estabilished MySQL Connection (Keys)") # Debug Message


### Functions

## Status Functions
def get_key_plan(api_key): # Function for getting the current plan of an api key
    mycursor3 = keys.cursor(buffered=True) # Defining the Cursor the execute MySQL commands
    sql = f"SELECT * FROM key_specifications WHERE api_key ='{api_key}'" # Selecting all attributes of the entries with the specified api_key
    mycursor3.execute(sql) # Executing the stated command
    record_exists = mycursor3.rowcount # Checking if search parameter has got a result
    
    if record_exists == 1: # Validating result
        myresult = mycursor3.fetchall() # Picking the first entry and creating a dictionary with the name myresult
        plan = myresult[0][3] # Getting the current Plan of an api_key
        return plan  # Returning myresult to FastAPI main file
    return None # Returning that the search parameter did not return a valid entry to the balance_functions file

def get_key_balance(api_key): # Function for getting the current balance of an api key
    mycursor2 = keys.cursor(buffered=True) # Defining the Cursor the execute MySQL commands
    sql = f"SELECT * FROM key_specifications WHERE api_key ='{api_key}'" # Selecting all attributes of the entries with the specified api_key
    mycursor2.execute(sql) # Executing the stated command
    record_exists = mycursor2.rowcount # Checking if search parameter has got a result
    
    if record_exists == 1: # Validating result
        myresult = mycursor2.fetchall() # Picking the first entry and creating a dictionary with the name myresult
        balance = int(myresult[0][4]) # Getting the current Balance of an api_key
        return balance  # Returning myresult to FastAPI main file
        mycursor2.close() # Closing the Cursor
    mycursor2.close() # Closing the Cursor
    return None # Returning that the search parameter did not return a valid entry to the balance_functions file

def validate_api_key(api_key): # Function for checking if an API-Key is valid or not
    mycursor = keys.cursor(buffered=True) # Defining the Cursor the execute MySQL commands
    sql = f"SELECT * FROM key_specifications WHERE api_key ='{api_key}'" # Selecting all attributes of the entries with the specified api_key
    mycursor.execute(sql) # Executing the stated command
    record_exists = mycursor.rowcount # Checking if search parameter has got a result
    
    if record_exists == 1: # Validating result
        return 1  # Returning myresult to FastAPI main file
    
    return 0 # Returning that the search parameter did not return a valid entry to the main file

## Maintenance Functions
def create_key(userid, plan="Free", balance=3): # Function for generating a random key for a new user
    letters = string.ascii_letters + string.digits # Defining the allowed characters for random key creation
    key = str('djp-'+''.join(random.choice(letters) for i in range(24))) # Key generation process
    sql = "INSERT INTO key_specifications (api_key, userid, plan, balance, status) VALUES (%s, %s, %s, %s, %s)" # Command for inserting the freshly made key into the database
    
    if plan == None: # Checking if plan was defined
        plan = "Free" # Defaulting plan to Free
        
    if balance == None: # Checking if balance was defined
        balance = 3 # Defaulting balance to 3
        
    val = (key, userid, plan, balance, "Active") # Specifying the values for the insertion
    mycursor.execute(sql, val) # Execution of the Insertion Process
    keys.commit() # Saving the freshly made key into the MySQL
    return str(key) # Returning the made api key to the balance_functions file

async def reset_user_key(usermail, userid, name): # Function for regenerating a customers key while disabling the old one
    letters = string.ascii_letters + string.digits # Defining the allowed characters for random key creation
    api_key = str('djp-'+''.join(random.choice(letters) for i in range(24))) # Key generation process
    sql = f"UPDATE key_specifications SET api_key = '{api_key}' WHERE userid ='{userid}'" # Selecting all attributes of the entries with the specified parameter
    mycursor.execute(sql) # Executing the Command above
    keys.commit() # Saving the changes to the MySQL Database
    balance.update_api_key(userid, api_key)
    await mail.send_key_mail(name, usermail, api_key)