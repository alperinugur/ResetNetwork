import time
import sys
import RPi.GPIO as GPIO
import urllib3
import socket
import os
import datetime


GPIO.setwarnings(False)


REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False


def is_internal():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname("bat.vrmplus.com")
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def zaman():
  return (datetime.datetime.now().strftime ( "%Y-%m-%d %H:%M:%S " ))
  


a_on = '1000101010000010111111001'
a_off ='1000101010000010110000111'
b_on = '1000101010000010001111111'
b_off = '1000101010000010110011111'
c_on = '000000000000000000000000'
c_off = '000000000000000000000000'
d_on = '000000000000000000000000'
d_off = '000000000000000000000000'
short_delay = 0.00064
long_delay = 0.00170
extended_delay = 0.016

NUM_ATTEMPTS = 10
TRANSMIT_PIN = 17




def transmit_code(code, attemp):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(attemp):
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()
    
def logekle(yazi):
    falper = open('netdlog.txt', 'a')
    falper.write( zaman () + yazi + "\r" )
    falper.close



print (zaman())


logekle ("PROGRAM STARTED!")

time.sleep(10)

count = 0
while (count < 20):
    print ('60 saniye bekliyoruz')
    time.sleep(60)
    print ('NETWORK & WIFI KONTROL EDILIYOR')

    if is_internal() == True:
        print ('LAN is up and working')
        count = 0
        print ('Checking Internet connection')
        if is_connected() == False:
            print ('INTERNET CONNECTION NOT AVAILABLE AT FIRST ATTEMPT. WAITING 120 SECS! \r')
            logekle ("INTERNET CONNECTION NOT AVAILABLE AT FIRST ATTEMPT. WAITING 120 SECS!")
            time.sleep (120)

            if is_connected() == False:
              print ('INTERNET CONNECTION NOT AVAILABLE. RESETTING MODEM!')
              logekle("INTERNET CONNECTION NOT AVAILABLE. RESETTING MODEM!")

              time.sleep(2)
            
              transmit_code (a_on,20)
              transmit_code (b_off,20)
              print ('RESTART SIGNAL SENT!')
              
              logekle ("RESET SIGNAL SENT OVER RF! WAITING 5 Minutes.")

              print ('5 dakika bekliyorum')
              time.sleep(60)
              print ('4 dakika kaldi')
              time.sleep(60)
              print ('3 dakika kaldi')
              time.sleep(60)
              print ('2 dakika kaldi')
              time.sleep(60)
              print ('1 dakika kaldi')
              time.sleep(60)
              print ('Umarim baglandik')

              logekle ("Restarting Program!")


            else:
              print ('internet connection successfull at second attempt. not resetting.')
              logekle ("internet connection successfull at second attempt. not resetting" )
              continue
        else:
            print ('INTERNET VAR')
            continue
    else:
        count = count+1
        print ('NETWORKE ERISEMEDIM')
        print ('TEKRAR DENEYECEGIM')
        print (count)

        logekle ("LAN NOT REACHABLE FOR " + str(count) + " MINUTES.")
        
        continue

print ('RESTART OLMA ZAMANI')
print ('RESTART ENGELLEMEK ICIN 5 dakika sureniz var!')
time.sleep(60)
print ('RESTART ENGELLEMEK ICIN 4 dakika sureniz var!')
time.sleep(60)
print ('RESTART ENGELLEMEK ICIN 3 dakika sureniz var!')
time.sleep(60)
print ('RESTART ENGELLEMEK ICIN 2 dakika sureniz var!')
time.sleep(60)
print ('RESTART ENGELLEMEK ICIN 1 dakika sureniz var!')
time.sleep(60)

print ('RESTART OLUYOR!!!')

logekle ("INTERNAL NETWORK NOT REACHABLE FOR 20 MINUTES. RESTARTING!!" )

time.sleep(2)
os.system('sudo shutdown -r now')


        

