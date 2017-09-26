from tag_consumer.consumer import get_next_tag
from time import time, sleep

if __name__ == '__main__':
    start = time()
    while True:
        processed = get_next_tag()

        if time() - start >= 45:
            break

        if processed is None:
            sleep(0.5)

