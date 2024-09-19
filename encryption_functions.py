### Importing necessary libraries and functions from functions.py files
from cryptography.fernet import Fernet

encryption_key = b''
f = Fernet(encryption_key) # Defining the key for encryption processing

### Functions
## Security Functions
async def encrypt_credentials(data): # Function for encrypting data like passwords and sensible informations. The data parameter is required.
    encrypted_data = f.encrypt(data.encode("utf-8")) # Encrypting given data
    return encrypted_data # Returning encrypted data token to the function

## Service Functions
async def validate_credentials(db_info, user_info): # Function for validating login credentials without decrypting the users information. The encrypted Database Data and the User Data parameter is required.
    encrypted_userdata = f.encrypt(user_info) # Encrypting user_data
    if encrypted_userdata == db_info:
        return 1
    else: 
        return 0
