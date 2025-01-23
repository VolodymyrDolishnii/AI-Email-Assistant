from helpers.IMAPServersList import imap_servers

def checkIMAPServer(server):
    for item in imap_servers:
        if server == item["server"]:
            return True
        
    return False