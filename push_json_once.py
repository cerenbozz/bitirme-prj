import json

import requests
import requests
from urllib.parse import urljoin

api_token = "1d52d143451da56520e8e5f982237d7dbfc3c230"
username = "isikkusgoz"
pythonanywhere_host = "www.pythonanywhere.com"
domain = "isikkusgoz.pythonanywhere.com"

api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
    pythonanywhere_host=pythonanywhere_host,
    username=username,
)
"""resp = requests.post(
    urljoin(api_base, "webapps/{domain}/reload/".format(domain=domain)),
    headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
)
if resp.status_code == 200:
  print('All OK')
else:
  print('Got unexpected status code {}: {!r}'.format(resp.status_code, resp.content))
"""
with open('emotion_results.json', 'r') as file:
    data = file.read()
files = {"content": data}
resp = requests.post(
    urljoin(api_base, "files/path/home/{username}/mysite/emotion_results.json".format(username=username)),
    files=files,
    headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
)
print(resp.status_code)
print(resp.content)
