import dht
import machine
import time

class DHT11():

  def __init__(self, pin=14):
    self.d = dht.DHT11(machine.Pin(pin))

  def measure(self):
  	self.d.measure()
  	time.sleep(2)

  @property
  def temperature(self):
    return self.d.temperature()

  @property
  def humidity(self):
    return self.d.humidity()
