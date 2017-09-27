from tag_consumer.consumer import get_next_tag
from tag_consumer.filelock import FileLock

from time import time, sleep

if __name__ == '__main__':
    print("* Waiting for lock")

    if FileLock.lock('/tmp/consume.lock', timeout=60):
        print("* Running for 60 seconds")
        start = time()
        while True:
            try:
                processed = get_next_tag()
            except:
                pass

            if int(time()) - start > 60:
                break

            if processed is None:
                sleep(0.01)
        print("* Terminating...")
        FileLock.release('/tmp/consume.lock')
    print("* Stopped")
