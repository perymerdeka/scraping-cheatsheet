""" 
parameters parser in urlib can be custom like requests

"""

from urllib.parse import urlparse, urlencode, parse_qsl

keywords = str(input("masukan keywords: "))

base_url = "https://www.bukalapak.com/products?"

url_params = {
    'from':'omnisearch',
    'from_keyword_history':'false',
    'search[keywords]': keywords,
    'search_source': 'omnisearch_keyword',
    'source': 'navbar'
}

def params_parser(url, params, show_result=False):
    parsed = urlparse(url)
    current_params = dict(parse_qsl(parsed.query))
    params_merger = urlencode({**current_params, **params})
    new_url = parsed._replace(query=params_merger).geturl()
    if show_result == False:
        return
    else:
        print(f"parsed URL is: {new_url}")
    return str(new_url)


print(params_parser(base_url, params=url_params))
