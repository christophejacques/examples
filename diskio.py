from psutil import disk_io_counters
from math import floor, log
from sys import argv
from time import sleep
import os


def bytes2human(n):
    symbols = (' B', ' KiB', ' MiB', ' GiB', ' TiB', ' PiB', ' EiB', ' ZiB', ' YiB')
    i = floor(log(abs(n)+1, 2) / 10)
    return '%.1f%s' % (n/2**(i*10), symbols[int(i)])


class Disk_IO:

    file_name = "DISKIO.txt"

    @classmethod
    def __init__(self):
        # disk_io_counters.cache_clear()
        pass

    @classmethod
    def save(self):
        with open(self.file_name, "w") as f:
            disks = disk_io_counters(perdisk=True, nowrap=False)
            premiere_ligne = True
            for disk in disks:
                if not premiere_ligne:
                    f.write("\n")
                else:
                    premiere_ligne = False
                ligne = "{} {} {}".format(disk, disks[disk].read_bytes, disks[disk].write_bytes)
                # print(ligne)
                f.write(ligne)
        f.close()

    @classmethod
    def load(self, disk_label):
        if os.path.isfile(self.file_name):
            with open(self.file_name, "r") as f:
                try:
                    while True:
                        ligne, *ldebut = f.readline().split()
                        if ligne == disk_label:
                            debut = list(map(int, ldebut))
                            break

                except Exception as e:
                    # print(e)
                    debut = (0, 0)
            f.close()
        else:
            debut = (0, 0)

        return debut

    @classmethod
    def get(self, disk_label):
        try:
            d = disk_io_counters(perdisk=True, nowrap=False)
            return d[disk_label].read_bytes, d[disk_label].write_bytes

        except Exception as e:
            print("No Disc", f"{disk_label!r}")
            exit(1)


def main(index, disk_label):
    diskio = Disk_IO()
    debut = diskio.load(disk_label)
    fin = diskio.get(disk_label)

    tailler = fin[0]-debut[0]
    taillew = fin[1]-debut[1]

    if tailler+taillew>0:
        print(disk_label + " : ", end="")

        if tailler>0:
            print( bytes2human(tailler), chr(9650), end=" ")
        if taillew>0:
            print( bytes2human(taillew), chr(9660), end=" ")

        print()
        diskio.save()

if __name__ == "__main__":
    if len(argv)>1:
        disk_label = argv[1]
    else:
        disk_label = "PhysicalDrive0"

    main(0, disk_label)

