import requests
from time import time, sleep


class DoorWatcher(object):
    def __init__(self, domain, room, rate):
        self.url = "http://{}/spsbot/{}".format(domain, room)
        self.state = True
        self.last_update = time()
        self.room = room
        self.rate = rate

    def checkroom(self):
        # Code to read the GPIO sensor here
        self.state = True
        self.last_update = time()

    def run(self):
        while True:
            self.checkroom()
            r = requests.post(self.url, data={self.room: self.state,
                                              "Last updated": self.last_update})
            if not 200 == r.status_code:
                raise ValueError("STATUS CODE OF NOT 200 RETURNED")

            print("Status Sent ;)")
            sleep(self.rate)


if __name__ == "__main__":
    loungebot = DoorWatcher("nglotz.ddns.net", "lounge", 5)
    loungebot.run()
