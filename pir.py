#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import smtplib
import os

sensor = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
previous_state = False
current_state = False
username = 'fancyusername'
password = 'fancypassword'
smtp = "fancy.smtp.server"
smtpport = 587
mfrom = 'fancy@email.ofyours'
mto = 'ancy@email.ofyours'
msubj = "Motion detected"
mbody = "Check photo"
try:
	while 1:
	    time.sleep(0.1)
	    previous_state = current_state
	    current_state = GPIO.input(sensor)
	    if current_state != previous_state:
	        new_state = "HIGH" if current_state else "LOW"
		server = smtplib.SMTP(smtp,smtpport)
		server.starttls()
		server.login(username,password)
		from subprocess import call
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEText import MIMEText
		from email.MIMEImage import MIMEImage
		msg = MIMEMultipart()
		msg['Subject'] = msubj
		msg['From'] = mfrom
		msg['To'] = mto
		text = MIMEText(mbody)
		msg.attach(text)
		os.system("wget http://127.0.0.1:8080/?action=snapshot -O /usr/local/bin/image.jpg")
		img = open("/usr/local/bin/image.jpg",'rb').read()
		imag = MIMEImage(img,name=os.path.basename("image.jpg"))
		msg.attach(imag)
		server.sendmail(msg['From'],msg['To'], msg.as_string())
		server.quit()
		command = "rm " + "/usr/local/bin/image.jpg"
		os.system(command)
except KeyboardInterrupt:
               print "Bye bye!"
               GPIO.cleanup()
