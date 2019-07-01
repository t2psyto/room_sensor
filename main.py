import wifimgr
import LED
import mydht
import zabbixsender
import time
import machine

led = LED.LED()
led.pin.on()

wlan = wifimgr.get_connection(failover=False)
for count in range(60):
    led.Blink(10,0.1)
    if wlan and wlan_sta.isconnected():
        led.pin.off()
    	break

if wlan and wlan_sta.isconnected():
	pass
else:
    #reboot: retry initialize the network connection
    machine.reset()

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")
led.Blink(2,0.2)
time.sleep(0.2)
led.Blink(2,0.2)


IP_ZBXSERVER = "192.168.16.101"

sender = zabbixsender.ZabbixSender(IP_ZBXSERVER, recv_buffer_size = 2048)
dht11 = mydht.DHT11()

while True:
    IsDone = False
    for count in range(4):
        try:
            led.pin.on()
            
            temperature = 0
            humidity = 0
            for n in range(4):
                led.Blink(1,0.1)
                dht11.measure()
                temperature = temperature + dht11.temperature
                humidity = humidity + dht11.humidity

            temperature = temperature >> 2
            humidity = humidity >> 2

            sender.data.clear()
            sender.add_noclock("testost","room_temperature",temperature)
            sender.send()
            
            sender.data.clear()
            sender.add_noclock("testost","room_humidity",humidity)
            sender.send()

            IsDone = True
            led.Notice()
        except Exception as e:
            print(e)
            time.sleep_ms(1000)
            
        finally:
            led.pin.off()
        
        if (IsDone == True):
            break

    #time.sleep(60)
    machine.deepsleep(60000)
