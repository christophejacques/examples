import base64
import quopri


s = "=3W/iYC/JAYMxipttjBh9rk5WhrQXvHfIyTpirzDn0TI="
print(len(s))

d = base64.b64decode(s)
print(d)

q = quopri.decodestring(s[1:-1])
print(q)
