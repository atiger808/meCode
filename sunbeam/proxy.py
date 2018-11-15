

import requests


proxy = '127.0.0.1:8888'

proxies = {
    'https': 'https://' + proxy,
    'http': 'http://' + proxy,
}

requests.get(url, proxies=proxies)

