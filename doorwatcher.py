import requests
from time import time, sleep
import datetime
import wiringpi
from json import dumps
import random

class DoorWatcher(object):
    def __init__(self, domain, room, rate,logfile="/home/pi/doorlog.txt"):
        self.url = "http://{}/spsbot/{}".format(domain, room)
        print("url",self.url)
        self.logfile = logfile
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
            self.checkroom()
            wiringpi.digitalWrite(16,self.state)
            print('about to send request')
            r = requests.post(self.url, data=dumps({self.room: self.state,
                                              "Last updated": self.last_update}))
            with open(self.logfile,"a+") as fh:
                print(r.status_code)

                if not 200 == r.status_code:
                    fh.write("{},{},{}".format(datetime.datetime.now(), {self.room: self.state},"Status Failed ;("))
                else:
                    fh.write("{},{},{}".format(datetime.datetime.now(), {self.room: self.state},"Status Sent ;)"))
                fh.write("\n")

                sleep(self.rate)


#if __name__ == "__main__":
print("the program ran")
loungebot = DoorWatcher("nglotz.ddns.net", "lounge", 5)
loungebot.run()
