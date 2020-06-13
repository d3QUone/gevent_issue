import time
import threading

import requests


class BackgroundWorker(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            try:
                r = requests.get('http://127.0.0.1:8001/status')
                print(r.text)
            except Exception as e:
                print(e)


def main():
    print('Begin')
    for _ in range(25):
        BackgroundWorker().start()

    time.sleep(60)
    print('Stop')


if __name__ == '__main__':
    main()
