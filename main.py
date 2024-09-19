### Importing necessary libraries and functions from functions.py files
from fastapi import FastAPI
print("Loading balance functions...")
import balance_functions as credits
print("Balance functions loaded successfully")
print("Loading access functions")
import access_functions as ac
import key_functions as keys
import smtp_functions as mails
import ident_functions as identification
import functional_functions as functional
import encryption_functions as encrypt
import json

### Defining FastAPI application
app = FastAPI()

### Functions / Endpoints

## Default Endpoint / Introduction Endpoint
@app.get("/")
async def introduction():
    return "Welcome to DJP-API! This message shows that our API is working correctly and is currently up and accessable for everyone. Please note that every request to this API except this one has to be made as a POST request. You are currently accessing our API with a GET request."

@app.post("/")
async def introduction():
    return "Welcome to DJP-API! This message shows that our API is working correctly and is currently up and accessable for everyone. Please note that every request to this API except this one has to be made as a POST request. You are currently accessing our API with a POST request."

## Service Endpoints

# Endpoint for User Registration
@app.post("/service/users/register")
async def user_registration(name=None, email=None, password=None, userid=None, plan=None, balance=None, access=None): # The parameters Name, Email, Password and Userid are necessary. The parameters Plan, Balance are optional. The Access Code is a code given by the frontend code to verify the permissions.
    
    if access != None: # Checking if an access key has been given
        validation = ac.validate_access_key(access, 3) # Validating if the access key is either invalid or has an insufficient permission level
        
        if validation == -1: # Executed if access key is invalid
            return {"status": 0, "error": "The access key that was given in the request body seems to be invalid. Check for spelling mistakes and try again."} # Returning an error message with an explanation to the frontend
        
        elif validation == 0: # Executed if access key has an insufficient permission level
            return {"status": 0, "error": "The access key that was given in the request body is valid. However it has an insufficient permission level to process this request. Please try again with a higher permission level."} # Returning an error message with an explanation to the frontend
        
        elif validation == 1: # Executed if access key is valid and has a sufficient permission level for executing the command
        
            if name == None or email == None or password == None or userid == None: # Checking if one of the required parameters is missing
                return {"status": 0, "error": "The request could not be processed as the request body is missing one or more necessary parameters for registration. Please try again after checking if all information are given."} # Returning an error message with an explanation to the frontend
            api_key = await credits.register_user(name, email, password, userid, plan, balance) # Generating the api_key of the new user
            status = 1 # Determining the Status of the registration process as successful
            return {"status": status, "api_key": api_key} # Returning the status and the api_key to the frontend
        
    else:
        return {"status": 0, "error": "The request body you have sent is missing an access key. Please try again after including it to process your request."}

# Endpoint for Admin User Info Management
@app.post("/service/users/userinfo")
async def user_info(name=None, email=None, userid=None, access=None): # One of the three search_parameters and a valid access code is required
    processable = 0 # Setting the state of the process as failed unless one of the parameters is given
    
    if access != None: # Checking if an access key has been given
        validation = ac.validate_access_key(access, 3) # Validating if the access key is either invalid or has an insufficient permission level
        
        if validation == -1: # Executed if access key is invalid
            return {"status": 0, "error": "The access key that was given in the request body seems to be invalid. Check for spelling mistakes and try again."} # Returning an error message with an explanation to the frontend
        
        elif validation == 0: # Executed if access key has an insufficient permission level
            return {"status": 0, "error": "The access key that was given in the request body is valid. However it has an insufficient permission level to process this request. Please try again with a higher permission level."} # Returning an error message with an explanation to the frontend
        
        elif validation == 1: # Executed if access key is valid and has a sufficient permission level for executing the command
   
            if name != None: # Checking for Name parameter
                request = ["name", name] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
        
            elif email != None: # Checking for Email parameter
                request = ["email", email] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
        
            elif userid != None: # Checking for Userid parameter
                request = ["userid", str(userid)] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
       
            if processable == 0: # Checking if there was a parameter given to the request
                return {"status": 0, "error": "Missing parameter to search for. Please give at least one of the following arguments to identify the customer: 'Name', 'Email' or 'Customer-ID'."} # Returning an error message with an explanation to the frontend
    
            else: # Executed if one parameter has been given
                userinfo = credits.get_user_info(request) # Getting information about the customer with the help of a key_functions function
        
                if userinfo == 0: # Checking if the customer parameter was invalid
                    return {"status": 0, "error": "The parameter you wanted to search for did not resolve in fetching a user. Please validate the given parameter and try it again."} # Returning an error message with an explanation to the frontend
        
                else: # Executed if previous task went successfully
                    return userinfo # Returning the User Information to the frontend
                     
       
    else:
        return {"status": 0, "error": "The request body you have sent is missing an access key. Please try again after including it to process your request."} # Returning an error message with an explanation to the frontend
    
    
# Endpoint for Admin Access Key Creation
@app.post("/service/maintenance/createaccess")
async def add_access_key(permission_level, notes=None): # A permission level is required. The notes parameter is optional
    key = ac.add_access_key(permission_level, notes) # Generating the access key with the specified permission integer and the specified notes
    return {"status": 1, "key": key} # Returning the generated access key to the frontend

# Endpoint for User Password Resetting
@app.post("/service/users/resetpassword")
async def reset_user_password(name=None, email=None, userid=None, access=None): # One of the three search_parameters and a valid access code is required
    processable = 0 # Setting the state of the process as failed unless one of the parameters is given
    
    if access != None: # Checking if an access key has been given
        validation = ac.validate_access_key(access, 3) # Validating if the access key is either invalid or has an insufficient permission level
        
        if validation == -1: # Executed if access key is invalid
            return {"status": 0, "error": "The access key that was given in the request body seems to be invalid. Check for spelling mistakes and try again."} # Returning an error message with an explanation to the frontend
        
        elif validation == 0: # Executed if access key has an insufficient permission level
            return {"status": 0, "error": "The access key that was given in the request body is valid. However it has an insufficient permission level to process this request. Please try again with a higher permission level."} # Returning an error message with an explanation to the frontend
        
        elif validation == 1: # Executed if access key is valid and has a sufficient permission level for executing the command
   
            if name != None: # Checking for Name parameter
                request = ["name", name] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
        
            elif email != None: # Checking for Email parameter
                request = ["email", email] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
        
            elif userid != None: # Checking for Userid parameter
                request = ["userid", str(userid)] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
       
            if processable == 0: # Checking if there was a parameter given to the request
                return {"status": 0, "error": "Missing parameter to search for. Please give at least one of the following arguments to identify the customer: 'Name', 'Email' or 'Customer-ID'."} # Returning an error message with an explanation to the frontend
    
            else: # Executed if one parameter has been given
                userinfo = credits.get_user_info(request) # Getting information about the customer with the help of a key_functions function
        
                if userinfo == 0: # Checking if the customer parameter was invalid
                    return {"status": 0, "error": "The parameter you wanted to search for did not resolve in fetching a user. Please validate the given parameter and try it again."} # Returning an error message with an explanation to the frontend
        
                else: # Executed if previous task went successfully
                    usermail = userinfo["email"] # Fetching User Email for password reset
                    await identification.reset_password(usermail)
                    return {"status": 1, "error": "The User has been sent a new password via the mail associated with its account."} # Returning an error message with an explanation to the frontend
                    
       
    else:
        return {"status": 0, "error": "The request body you have sent is missing an access key. Please try again after including it to process your request."} # Returning an error message with an explanation to the frontend
    
# Endpoint for User API Key Resetting
@app.post("/service/users/resetapikey")
async def reset_user_password(name=None, email=None, userid=None, access=None): # One of the three search_parameters and a valid access code is required
    processable = 0 # Setting the state of the process as failed unless one of the parameters is given
    
    if access != None: # Checking if an access key has been given
        validation = ac.validate_access_key(access, 3) # Validating if the access key is either invalid or has an insufficient permission level
        
        if validation == -1: # Executed if access key is invalid
            return {"status": 0, "error": "The access key that was given in the request body seems to be invalid. Check for spelling mistakes and try again."} # Returning an error message with an explanation to the frontend
        
        elif validation == 0: # Executed if access key has an insufficient permission level
            return {"status": 0, "error": "The access key that was given in the request body is valid. However it has an insufficient permission level to process this request. Please try again with a higher permission level."} # Returning an error message with an explanation to the frontend
        
        elif validation == 1: # Executed if access key is valid and has a sufficient permission level for executing the command
   
            if name != None: # Checking for Name parameter
                request = ["name", name] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
        
            elif email != None: # Checking for Email parameter
                request = ["email", email] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
        
            elif userid != None: # Checking for Userid parameter
                request = ["userid", str(userid)] # Defining the request parameters for the key_functions function
                processable = 1 # Setting the state of the process as processable
       
            if processable == 0: # Checking if there was a parameter given to the request
                return {"status": 0, "error": "Missing parameter to search for. Please give at least one of the following arguments to identify the customer: 'Name', 'Email' or 'Customer-ID'."} # Returning an error message with an explanation to the frontend
    
            else: # Executed if one parameter has been given
                userinfo = credits.get_user_info(request) # Getting information about the customer with the help of a key_functions function
        
                if userinfo == 0: # Checking if the customer parameter was invalid
                    return {"status": 0, "error": "The parameter you wanted to search for did not resolve in fetching a user. Please validate the given parameter and try it again."} # Returning an error message with an explanation to the frontend
        
                else: # Executed if previous task went successfully
                    usermail = userinfo["email"] # Fetching User Email for API Key reset
                    userid = userinfo["userid"] # Fetching User ID for API Key reset
                    name = userinfo["name"]
                    await keys.reset_user_key(usermail, userid, name) 
                    return {"status": 1, "error": "The User has been sent a new password via the mail associated with its account."} # Returning an error message with an explanation to the frontend
                    
       
    else:
        return {"status": 0, "error": "The request body you have sent is missing an access key. Please try again after including it to process your request."} # Returning an error message with an explanation to the frontend
    
@app.post("/service/users/login")
async def login(mail, password):
    valid = identification.login_user(mail, password)
    return valid
    

## Functional Endpoints

# Endpoint for LLM access
@app.post("/functional/llm")
async def llm_request(prompt, api_key, system=None): # Prompt and API-Key are required parameters, System Prompt is optional
    validation = keys.validate_api_key(api_key) # Checking the given API-Key
    if validation == 0: # Triggered if API-Key is invalid or unknown 
        return {"status": 0, "error": "The given API-Key seems to be unknown or invalid. If you are a developer, pay attention to the spelling of the API-Key. If you are a user of our frontend, please try again. If this error proceeds, please contact the support team."} # Returning an error message with an explanation to the frontend
    else: # Triggered if API-Key is valid
        print(1)
        response = functional.llm_request(prompt)
        status = 1
        return {"status": status, "response": response}
    
