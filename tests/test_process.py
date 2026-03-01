import multiprocessing
import os
import signal
import psutil
import time
from platform import platform


def fprint(*args, **kwargs):
    print(*args, flush=True, **kwargs)


class GestionProcess:
    def __init__(self, tache):
        self.isWindows = platform()[:3].upper() == "WIN"

        if not callable(tache):
            raise TypeError(f"la tache {tache!r} n'est pas de type callable")

        self.process = multiprocessing.Process(target=tache)
        fprint(f"{tache.__name__=}")


    def start(self):
        self.process.start()
        self.pid = self.process.pid
        self.ps = psutil.Process(self.pid)
        fprint(f"{self.ps=}")
        fprint("--- STARTED  ---")

    def end(self):
        if self.pid:
            self.process.join()
        fprint("\n--- ENDED  ---")

    def pause(self):
        fprint("\n--- PAUSE (SIGSTOP) ---")
        if self.isWindows:
            self.ps.suspend()
        else:
            self.os.kill(self.pid, signal.SIGSTOP)

    def reprise(self):
        fprint("--- REPRISE (SIGCONT) ---")
        if self.isWindows:
            self.ps.resume()
        else:
            self.os.kill(self.pid, signal.SIGCONT)

    def kill(self):
        if self.isWindows:
            if self.ps.is_running():
                self.ps.kill()
        elif self.pid:
            self.os.kill(self.pid, signal.SIGTERM) 

        fprint("\n--- KILL (SIGKILL) ---", end="")
        self.pid = None
        self.end()


class Processus:
    def tache_infinie(self):
        count = 0
        while count < 70:
            count += 1
            fprint(f"{count}", end=".")
            time.sleep(0.08)


if __name__ == "__main__":
    pr = Processus()
    gp = GestionProcess(pr.tache_infinie)

    gp.start()

    time.sleep(2)
    gp.pause()

    time.sleep(3)
    gp.reprise()

    time.sleep(2)
    gp.kill()
    # gp.end()
    