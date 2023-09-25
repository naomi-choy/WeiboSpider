import requests
from urllib import request

url = 'https://weibo.com/u/5978791676'

resp = requests.get(url)

rt = request.Request(url=url, method='GET')
with request.urlopen(rt) as rp:
    txt = rp.read()

print(txt)