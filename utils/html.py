import urllib.request
from msvcrt import getch
import traceback
from definition import printdef
from urllib.parse import urlparse

try:
  url = "http://www.python.org/"
  requete = urllib.request.Request(url)
  #printdef(requete)
  
  response = urllib.request.urlopen(url)
  printdef(response)
  print(dict(response.getheaders())['Content-Type'].split("; ")[1].split("=")[1])
  print((dict(response.getheaders())['Content-Type']))
  
  o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html?arg1=12&arg2=abcd')
  #printdef(o)
  

except urllib.error.HTTPError as e:
  print("HTTP Error :")
  print(e.code)
  print(e.read()[:500])

except urllib.error.URLError as e:
  print("URL Error :")
  print("reason:", e.reason)
  
except:
  print(traceback.print_exc())
  
print("Press any key.")
getch()