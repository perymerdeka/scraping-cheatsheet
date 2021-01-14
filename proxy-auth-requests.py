import requests
from base64 import b64encode

proxy = {
	'http': 'http://173.208.208.74:60099'
}

class HTTPProxyAuth(requests.auth.HTTPBasicAuth):
	"""Like requests.auth.HTTPBasicAuth, but adds a Proxy-Authorization header"""
	def __call__(self, r):
		auth_s = b64encode('%s:%s' % (self.username, self.password))
		r.headers['Proxy-Authorization'] = ('Basic %s' % auth_s)
		return r


auth = HTTPProxyAuth('user', 'password')
r = requests.get('http://httpbin.org/', proxies=proxy, return_response=False)
r = auth(r)
r.send()

print r.response
r = requests.get('http://httpbin.org/', proxies=proxy, return_response=False)
r = auth(r)
r.send()

print r.response 