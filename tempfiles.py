import datetime 
import tempfile
from time import sleep
from tempfile import gettempdir, mkstemp


def fprint(f, lines):
    for line in lines:
        f.write("{} - {}\n".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), line))


print(dir(tempfile))
print(gettempdir())

if False:
    # create a temporary file and write some data to it
    fp = tempfile.TemporaryFile(mode="w", prefix="_", suffix=".txt", delete=False)
    print(dir(fp))
    print(fp.file)
    print(fp.name)
    fp.write('Hello 1 world!\n')
    fp.write('Hello 2 world!\n')

    # close the file, it will be removed
    fp.close()
    sleep(1)

if False:
    fp, name = mkstemp(prefix="_", suffix=".txt", text=True)
    print(fp, "*", name)

with open(mkstemp(prefix="_", suffix=".txt", text=True)[1], mode='w') as f:
    nom = f.name
    print(f.name, "opened")
    print(dir(f))
    print("writable:", f.writable())
    if f.writable():
        fprint(f, ["1ere ligne", "2eme ligne"])
    f.close()
print()
