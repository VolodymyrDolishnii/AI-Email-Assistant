def checkCredentials(credentials):
    for item in credentials:
        if item == "":
            return False
    
    return True