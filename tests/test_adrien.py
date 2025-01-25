from requests import Session
import datetime
import time


debut = datetime.datetime.now()
print(debut)


with Session() as s:
    for idx in range(10):
        print(f"{idx:>3}", datetime.datetime.now(), "-", end="", flush=True)
        r = s.post(
            url="https://demo.linuxtricks.fr/?text_content=Bonjour+tout+le+monde.&expiration_days=7&max_views=10",)
        print(r.ok, r.status_code, flush=True)
        time.sleep(0.1)
        if not r.ok:
            break

fin = datetime.datetime.now()
print(fin, flush=True)
print("\nDurée =", fin-debut)
