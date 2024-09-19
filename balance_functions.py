### Importing necessary libraries for local functions
import mysql.connector
print("Started Loading Balance Functions")
import key_functions as keys
import encryption_functions as encrypt

### Connecting to Customer MySQL
print("Estabilishing a MySQL Connection (Customers)")
customers = mysql.connector.connect(
  host="djp-industries-djpapi.d.aivencloud.com", # Connecting to the following Address
  port=20164,				   # Connecting to the following Port
  user="avnadmin",	   # Connecting with the following Username
  password="AVNS_m2Nj-w9VIhMYMoQmeJu", # Connecting with the following Password
  database="defaultdb"			   # Connecting to the following Database
)
mycursor = customers.cursor(buffered=True) # Defining the Cursor the execute MySQL commands
print("Successfully estabilished MySQL connection (Customers)")
### Functions

## Status Functions
def get_user_info(request): # Function to get a Users Information
    search_parameter_type = str(request[0]) # Extracting the search parameter type out of a dictionary
    search_parameter_info = str(request[1]) # Extracting the search parameter info out of a dictionary
    sql = f"SELECT * FROM customers WHERE {search_parameter_type} ='{search_parameter_info}'" # Selecting all attributes of the entries with the specified parameter
    mycursor.execute(sql) # Executing the stated command
    record_exists = mycursor.rowcount # Checking if search parameter has got a result
    
    if record_exists == 1: # Validating result
        myresult = mycursor.fetchall() # Picking the first entry and creating a dictionary with the name myresult
        name = myresult[0][1] # Getting the Name of the Customer
        email = myresult[0][2] # Getting the Email of the Customer
        userid = myresult[0][4] # Getting the Userid of the Customer
        api_key = myresult[0][5] # Getting the Api_Key of the Customer
        notes = myresult[0][6] # Getting the Notes of the Customer
        plan = keys.get_key_plan(api_key) # Getting the Plan of the Customer with the help of the key_functions file
        balance = keys.get_key_balance(api_key) # Getting the Balance of the Customer with the help of the key_functions file
        status = 1 # Setting the Status as Succeeded
        result = {"status": status, "name": name, "email": email, "userid": userid, "api_key": api_key, "notes": notes, "plan": plan, "balance": balance}
        return result  # Returning myresult to FastAPI main file
    
    return 0 # Returning that the search parameter did not return a valid entry to the FastAPI main file


## Maintenance Functions
async def register_user(name, email, password, userid, plan=None, balance=None): # Function for registering new users
    api_key = keys.create_key(str(userid), plan, balance) # Accessing key_functions file to create a new key
    encrypted_password = await encrypt.encrypt_credentials(password)
    sql = "INSERT INTO customers (name, email, password, userid, api_key, notes) VALUES (%s, %s, %s, %s, %s, %s)" # Specifying the Inserted Data
    val = (name, email, encrypted_password, userid, api_key, "None") # Giving the command above the personal data
    mycursor.execute(sql, val) # Adding the user to the database
    customers.commit() # Saving changes to MySQL database
    return api_key # Returning the api_key to FastAPI main file
    
def update_api_key(userid, newkey): # Function to update the API Key in Customer Database. Often called by key_functions file
    sql = f"UPDATE customers SET api_key = '{newkey}' WHERE userid ='{userid}'" # Selecting all attributes of the entries with the specified parameter
    mycursor.execute(sql) # Executing the Command above
    customers.commit() # Saving the changes to the MySQL Database