import requests.utils as requti
import datetime
import time

from datetime import datetime as dt, UTC


date_utc = dt.now(UTC)
heure = date_utc.hour

heure_actuelle = time.localtime().tm_hour
delta_hour = heure_actuelle - heure
# print("delta=", delta_hour)

tz = datetime.timezone(datetime.timedelta(hours=delta_hour))
maintenant = dt.isoformat(dt.now(tz))
print("date/heure =", maintenant)

une_date = dt.today()
une_date = dt.now(tz)
print()
print(une_date)
print()
print(une_date.strftime("%a - %A"))
print(une_date.strftime("%b - %B"))
print(une_date.strftime("%c - %C"))
print(une_date.strftime("%d - %D - %e"))
print(une_date.strftime("%f - %F"))
print(une_date.strftime("%G - %y - %Y"))
print(une_date.strftime("%h - %H"))
print(une_date.strftime("%I"))
print(une_date.strftime("%j"))
print(une_date.strftime("%m - %M"))
print(une_date.strftime("%n"))
print(une_date.strftime("%p"))
print(une_date.strftime("%r - %R"))
print(une_date.strftime("%S"))
print(une_date.strftime("%t - %T"))
print(une_date.strftime("%u - %U"))
print(une_date.strftime("%V"))
print(une_date.strftime("%w - %W"))
print(une_date.strftime("%x - %X"))
print(une_date.strftime("%y - %Y"))
print(une_date.strftime("%z - %Z"))
