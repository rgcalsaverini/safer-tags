import os
from time import sleep, time


class FileLock(object):
    @staticmethod
    def lock(path, timeout=5):
        start = time()

        while True:
            if FileLock._can_lock(path):
                FileLock._perform_lock(path)
                return True
            else:
                if time() - start > timeout:
                    return False
                sleep(0.01)

    @staticmethod
    def release(path):
        os.unlink(path)

    @staticmethod
    def _pid_running(pid):
        for _ in range(3):
            try:
                os.kill(pid, 0)
                return True
            except ProcessLookupError:
                sleep(0.01)
        return False

    @staticmethod
    def _can_lock(path):
        if os.path.exists(path) and os.path.isfile(path):
            try:
                with open(path, 'r') as fp:
                    pid = int(fp.read().strip())
            except ValueError:
                return True

            if FileLock._pid_running(pid):
                return False
            return True
        else:
            return True

    @staticmethod
    def _perform_lock(path):
        with open(path, 'w') as fp:
            fp.write(str(os.getpid()))
