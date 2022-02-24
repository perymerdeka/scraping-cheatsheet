import re
import requests
from requests.utils import get_auth_from_url
from requests.auth import HTTPDigestAuth
from requests.utils import parse_dict_header
from urllib3.util import parse_url

def get_proxy_autorization_header(proxy, method):
    username, password = get_auth_from_url(proxy)
    auth = HTTPProxyDigestAuth(username, password)
    proxy_url = parse_url(proxy)
    proxy_response = requests.request(method, proxy_url, auth=auth)
    return proxy_response.request.headers['Proxy-Authorization']


class HTTPSAdapterWithProxyDigestAuth(requests.adapters.HTTPAdapter):
    def proxy_headers(self, proxy):
        headers = {}
        proxy_auth_header = get_proxy_autorization_header(proxy, 'CONNECT')
        headers['Proxy-Authorization'] = proxy_auth_header
        return headers


class HTTPAdapterWithProxyDigestAuth(requests.adapters.HTTPAdapter):
    def proxy_headers(self, proxy):
        return {}

    def add_headers(self, request, **kwargs):
        proxy = kwargs['proxies'].get('http', '')
        if proxy:
            proxy_auth_header = get_proxy_autorization_header(proxy, request.method)
            request.headers['Proxy-Authorization'] = proxy_auth_header



class HTTPProxyDigestAuth(requests.auth.HTTPDigestAuth):

    def init_per_thread_state(self):
        # Ensure state is initialized just once per-thread
        if not hasattr(self._thread_local, 'init'):
            self._thread_local.init = True
            self._thread_local.last_nonce = ''
            self._thread_local.nonce_count = 0
            self._thread_local.chal = {}
            self._thread_local.pos = None
            self._thread_local.num_407_calls = None

    def handle_407(self, r, **kwargs):
        """
        Takes the given response and tries digest-auth, if needed.
        :rtype: requests.Response
        """

        # If response is not 407, do not auth
        if r.status_code != 407:
            self._thread_local.num_407_calls = 1
            return r

        s_auth = r.headers.get('proxy-authenticate', '')

        if 'digest' in s_auth.lower() and self._thread_local.num_407_calls < 2:
            self._thread_local.num_407_calls += 1
            pat = re.compile(r'digest ', flags=re.IGNORECASE)
            self._thread_local.chal = requests.utils.parse_dict_header(
                    pat.sub('', s_auth, count=1))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.close()
            prep = r.request.copy()
            requests.cookies.extract_cookies_to_jar(prep._cookies, r.request, r.raw)
            prep.prepare_cookies(prep._cookies)

            prep.headers['Proxy-Authorization'] = self.build_digest_header(prep.method, prep.url)
            _r = r.connection.send(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep

            return _r

        self._thread_local.num_407_calls = 1
        return r

    def __call__(self, r):
        # Initialize per-thread state, if needed
        self.init_per_thread_state()
        # If we have a saved nonce, skip the 407
        if self._thread_local.last_nonce:
            r.headers['Proxy-Authorization'] = self.build_digest_header(r.method, r.url)

        r.register_hook('response', self.handle_407)
        self._thread_local.num_407_calls = 1

        return r


session = requests.Session()
session.proxies = {
    'http': 'http://username:password@proxyhost:proxyport',
    'https':  'http://username:password@proxyhost:proxyport'
}
session.trust_env = False

session.mount('http://', HTTPAdapterWithProxyDigestAuth())
session.mount('https://', HTTPSAdapterWithProxyDigestAuth())

response_http = session.get("http://ww3.safestyle-windows.co.uk/the-secret-door/")
print(response_http.status_code)

response_https = session.get("https://stackoverflow.com/questions/13506455/how-to-pass-proxy-authentication-requires-digest-auth-by-using-python-requests")
print(response_https.status_code)
