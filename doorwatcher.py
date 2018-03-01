import requests
from time import time, sleep
import datetime
import wiringpi
from json import dumps
import random

class DoorWatcher(object):
    def __init__(self, domain, room, rate):
        self.url = "http://{}/spsbot/{}".format(domain, room)
        self.state = True
        self.last_update = time()
        self.room = room
        self.rate = rate
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(16,0) # pin 16 is input for sensor
#        wiringpi.pinMode(15,1) # i maybe fried pin 15 so no more probe

    def checkroom(self):
        # switch is open when door is open
        self.state = not wiringpi.digitalRead(16)
        self.last_update = time()

    def run(self):
        while True:
            self.rate = random.randint(30,120)
            print(datetime.datetime.now(), {self.room: self.state})
            self.checkroom()
            wiringpi.digitalWrite(16,self.state)
            r = requests.post(self.url, data=dumps({self.room: self.state,
                                              "Last updated": self.last_update}))
            if not 200 == r.status_code:
                print(r.status_code)
                raise ValueError("STATUS CODE OF NOT 200 RETURNED")

            print("Status Sent ;)")
            sleep(self.rate)


#if __name__ == "__main__":
print("the program ran")
loungebot = DoorWatcher("nglotz.ddns.net", "lounge", 5)
loungebot.run()
