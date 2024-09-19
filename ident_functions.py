### Importing necessary libraries for local functions
import mysql.connector
import random
import string
import key_functions as keys
import smtp_functions as mails
import encryption_functions as encrypt

### Connecting to Customer MySQL
customers = mysql.connector.connect(
  host="", # Connecting to the following Address
  port="",				   # Connecting to the following Port
  user="",	   # Connecting with the following Username
  password="", # Connecting with the following Password
  database="defaultdb"			   # Connecting to the following Database
)
mycursor = customers.cursor(buffered=True) # Defining the Cursor the execute MySQL commands

### Functions
async def reset_password(mail): # Function to get a Users Information
    sql = f"SELECT * FROM customers WHERE email ='{mail}'" # Selecting all attributes of the entries with the specified parameter
    mycursor.execute(sql) # Executing the stated command
    record_exists = mycursor.rowcount # Checking if search parameter has got a result

    if record_exists == 1: # Validating result
        myresult = mycursor.fetchall() # Picking the first entry and creating a dictionary with the name myresult
        name = myresult[0][1]
        letters = string.ascii_letters + string.digits # Defining the allowed characters for random password creation
        newpassword = str(''.join(random.choice(letters) for i in range(12))) # Password generation process
        encrypted_password = await encrypt.encrypt_credentials(newpassword)
        sql = f"UPDATE customers SET password ='{str(encrypted_password)}' WHERE email ='{mail}'" # Selecting all attributes of the entries with the specified parameter
        mycursor.execute(sql) # Executing the command above
        customers.commit() # Saving the changes to MySQL Database
        await mails.send_password_mail(name, mail, new_password) # Sending the Password Reset Email with the help of a smtp_functions.py function
    
async def login_user(mail, password):
    sql = f"SELECT * FROM customers WHERE password ='{password}'" # Selecting all attributes of the entries with the specified parameter
    mycursor.execute(sql) # Executing the stated command
    record_exists = mycursor.rowcount # Checking if search parameter has got a result
    if record_exists == 1:
        return 1
    else:
        return 0
