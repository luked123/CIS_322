import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# Activate user api call. 

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 %s <host_url> <username> <password> <role>"%sys.argv[0])
        return
    
    url = sys.argv[1] + 'activate_user'

    args = dict()                                      # Imports args from command line. Checks if role is correct.
    args['username'] = sys.argv[2]
    args['password'] = sys.argv[3]
    if sys.argv[4] == "facofc":
        args['role'] = "Facilities Officer"
    elif sys.argv[4] == "logofc":
        args['role'] = "Logistics Officer"
    else:
        print("Roles supported are either 'facofc' (Facilities Officer) or 'logofc' (Logistics Officer)")
        return

    print("Activating user: %s"%args['username'])      # Lets user know trying to acticate user.

    sargs = dict()                                     # Creates arguments to send.
    sargs['arguments'] = json.dumps(args)
    data = urlencode(sargs)

    req = Request(url, data.encode('ascii'),method='POST')    # Makes requests.
    res = urlopen(req)

    resp = json.loads(res.read().decode('ascii'))             # Reads the response.

    print("Call to LOST returned: %s"%resp['result'])         # Returns the response.

if __name__=='__main__':
    main()
