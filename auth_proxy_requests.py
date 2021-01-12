""" 
BASIC AUTH
"""
proxies = { 'https' : 'https://user:password@proxyip:port' } 
r = requests.get('https://url', proxies=proxies)
print(r.status_code)

# option 1 Using HTTPProxyAuth
from requests.auth import HTTPProxyAuth
proxyDict = {
'http' : 'http://138.197.222.35:80',
'https' : 'http://1138.197.222.35:8080'
}
#auth = HTTPProxyAuth('username', 'mypassword')
r = requests.get('http://httpbin.org/ip', proxies=proxyDict)
print (r)


# option 2 Using HTTPDigestProxyAuth

# installing module
# pip install requests-toolbelt  

import requests
from requests_digest_proxy import HTTPProxyDigestAuth

s = requests.Session()
s.proxies = {
        'http': 'http://1.2.3.4:8080/',
        'https': 'http://1.2.3.4:8080/'
}
s.auth = HTTPProxyDigestAuth(('user1', 'password1'))

print(s.get('https://httpbin.org/ip').text)

'''Should the website requires some kind of HTTP authentication, this can be specified to HTTPProxyDigestAuth constructor this way:'''


# HTTP Basic authentication for website
s.auth = HTTPProxyDigestAuth(('user1', 'password1'),
        auth=requests.auth.HTTPBasicAuth('user1', 'password0'))
print(s.get('https://httpbin.org/basic-auth/user1/password0').text))

# HTTP Digest authentication for website
s.auth = HTTPProxyDigestAuth(('user1', 'password1'),,
        auth=requests.auth.HTTPDigestAuth('user1', 'password0'))
print(s.get('https://httpbin.org/digest-auth/auth/user1/password0').text)

