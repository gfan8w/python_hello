import datetime
import json
import logging

import requests

# DEBUG = False
DEBUG = True

# helloworld
# Sample Code for Two-Way (Mutual) SSL

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPSConnection.debuglevel = 0

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

print("START Sample Code for Two-Way (Mutual) SSL")

print(datetime.datetime.now())
date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

url = 'https://sandbox.api.visa.com/vdp/helloworld'
headers = {}
body = {}

payload = json.loads('''{}
''')

# THIS IS EXAMPLE ONLY how will user_id and password look like
# user_id = '1WM2TT4IHPXC8DQ5I3CH21n1rEBGK-Eyv_oLdzE2VZpDqRn_U'
# password = '19JRVdej9'

user_id = '<YOUR USER ID>'
password = '<YOUR PASSWORD>'

# THIS IS EXAMPLE ONLY how will cert and key look like
# cert = 'cert.pem'
# key = 'key_83d11ea6-a22d-4e52-b310-e0558816727d.pem'

cert = '<YOUR CLIENT CERTIFICATE PATH>'
key = '<YOUR PRIVATE KEY PATH>'

timeout = 10

try:
    response = requests.get(url,
                            # verify = ('put the CA certificate pem file path here'),
                            cert=(cert, key),
                            # headers = headers,
                            auth=(user_id, password),
                            # data = body,
                            # json = payload,
                            timeout=timeout
                            # if DEBUG: print (response.text)
                            )
except Exception as e:
    print(e)

if DEBUG: print(response.headers)
if DEBUG: print(response.content)

var1 = str(response.status_code)
var2 = '200'
msg = " Two-Way (Mutual) SSL test failed"
assert var1 == var2, msg