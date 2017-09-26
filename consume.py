from tag_consumer.consumer import get_next_tag

if __name__ == '__main__':
    for i in range(10000):
        processed = get_next_tag()

        if processed is None:
            break
