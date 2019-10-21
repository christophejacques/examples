import subprocess as sp

if __name__ != "__main__":
    print("loading subprocess", end=" ... ")


res = sp.run(["dir", "/b"], capture_output=True, shell=True, text=True, encoding="UTF-8")
if res.returncode:
    print(f"Erreur de commande :\n({res.returncode}) {res.stderr}")
else:
    print(res.stdout)

if __name__ != "__main__":
    print("ok")

input("")