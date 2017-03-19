import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 %s <host_url> <username> <password> <role> \n"%sys.argv[0])
        return
    
    url = sys.argv[1] + 'activate_user'

    args = dict()
    args['username'] = sys.argv[2]
    args['password'] = sys.argv[3]
    if sys.argv[4] == "facofc":
        args['role'] = "Facilities Officer"
    elif sys.argv[4] == "logofc":
        args['role'] = "Logistics Officer"
    else:
        return "Roles supported are either 'facofc' (Facilities Officer) or 'logofc' (Logistics Officer)\n"

    print("Activating user: %s"%args['username'])

    sargs = dict()
    sargs['arguments'] = json.dumps(args)
    data = urlencode(sargs)

    req = Request(url, data.encode('ascii'),method='POST')
    res = urlopen(req)

    resp = json.loads(res.read().decode('ascii'))

    print("Call to LOST returned: %s"%resp['result'])

if __name__=='__main__':
    main()
