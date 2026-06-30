import secrets




def generate_code_for_signup () : 
    return secrets.randbelow(900000) + 100000