import sys
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

def main():
    if len(sys.argv) < 3: 
        print("Usage: python3 %s <host_url> <username>"%sys.argv[0])
        return

    url = sys.argv[1] + 'revoke_user'

    args = dict()
    args['username'] = sys.argv[2]

    print("Revoking user: %s"%args['username'])

    sargs = dict()
    sargs['arguments'] = json.dumps(args)
    data = urlencode(sargs)

    req = Request(url, data.encode('ascii'), method='POST')
    res = urlopen(req)

    resp = json.loads(res.read().decode('ascii'))

    print("Call to LOST returned: %s"%resp['result'])

if __name__=='__main__':
    main()
