from helpers.IMAPServersList import imap_servers

def getIMAPServerPort(server):
    for item in imap_servers:
        if server == item["server"]:
            return item["port"]
        