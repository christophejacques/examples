import http.client
import urllib
from datetime import datetime as dt


msg = f"{dt.now():%d/%m/%Y %H:%M:%S}"

print("pushing message", end=" ")
conn = http.client.HTTPSConnection("api.pushover.net:443")
req = conn.request(
    "POST", "/1/messages.json", urllib.parse.urlencode({
        "token": "ahugb6ka8fwbt2dx7iwidso6jqhp9h",
        "user": "u51qwgdxsvmn8bm32pdhbi2o2c69zr",
        "message": msg,
    }), {
        "Content-type": "application/x-www-form-urlencoded"
    })
rep = conn.getresponse()
if rep.status == 200:
    print("done")
else:
    print("Error", rep.code)
