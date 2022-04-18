from urllib.parse import unquote
from html import unescape


print(unescape('&pound; 682m'))

print(unquote("un ~:%7e, espace:'%20'"))
