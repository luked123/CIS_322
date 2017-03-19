import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# Revoke user API call. 

def main():
    if len(sys.argv) < 3: 
        print("Usage: python3 %s <host_url> <username>"%sys.argv[0])
        return

    url = sys.argv[1] + 'revoke_user'              

    args = dict()                                      # Gets arguments from command line.
    args['username'] = sys.argv[2]

    print("Revoking user: %s"%args['username'])        

    sargs = dict()                                     # Prepares arguments to send to webserver.
    sargs['arguments'] = json.dumps(args)
    data = urlencode(sargs)

    req = Request(url, data.encode('ascii'), method='POST')     # Makes the request. 
    res = urlopen(req)

    resp = json.loads(res.read().decode('ascii'))               # Returns the response from the server. 

    print("Call to LOST returned: %s"%resp['result'])

if __name__=='__main__':
    main()
