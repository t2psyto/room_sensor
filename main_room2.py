import wifimgr
import LED
import mydht
import zabbixsender
import time
import machine

led = LED.LED()
led.pin.on()

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)


wlan = wifimgr.get_connection(failover=False)
for count in range(60):
    led.Blink(10,0.1)
    if wlan and wlan.isconnected() == True:
        led.pin.off()
    	break

if wlan and wlan.isconnected() == True:
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
dht = mydht.AM2320()

while True:
    # set RTC.ALARM0 to fire after 60 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, 60000)

    IsDone = False
    for count in range(4):
        try:
            led.pin.on()
            
            temperature = 0
            humidity = 0
            for n in range(4):
                led.Blink(1,0.1)
                dht.measure()
                temperature = temperature + dht.temperature
                humidity = humidity + dht.humidity

            temperature = temperature / 4
            humidity = humidity / 4

            sender.data.clear()
            sender.add_noclock("testost","room2_temperature",temperature)
            sender.send()
            
            sender.data.clear()
            sender.add_noclock("testost","room2_humidity",humidity)
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
    rtc.alarm(rtc.ALARM0, 60000)

    # put the device to sleep
    machine.deepsleep()
    time.sleep(1)
    