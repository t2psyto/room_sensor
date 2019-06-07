import machine
import time

class LED(object):
    def __init__(self,pinNum=13):
        self.pin = machine.Pin( pinNum, machine.Pin.OUT)

    def Blink(self, repeatTime, sleepTime):
        self.pin.off()
        for i in range(repeatTime):
            self.pin.on()
            time.sleep(sleepTime)
            self.pin.off()
            time.sleep(sleepTime)

    def Notice(self):
        self.Blink(4, 0.15)
            
    def Alert(self):
        self.Blink(3, 0.06)
