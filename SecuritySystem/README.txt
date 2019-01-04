Author: Otto Holthe
Date: 1/3/2019
Written with Python version 2.7.13

Summary:
This project is a simple security system that is designed to be setup at a single
doorway in which anyone who passes through the door will trigger a webcam to take a picture
and email the picture to the owners email address.

Requirements:
  Main Hardware Components:
    - raspberry PI 3
    - Webcam with USB plugin
    - Ultrasonic Sonar Distance Sensor
  Optional Hardware:
    - Raspi compatible LED lights (for visual indications)
    - Raspi compatible active/passive buzzer (for sounding an alarm)

  Packages:
    - RPi
    - open-csv
    - numpy
  Optional:
    - Flask (for web app control of the security system)

How it works:
  The ultrasonic distance sensor constantly measures the distance in front of it which is
  able to detect when a door has been open or closed based on the change in distance. This
  distance must be configured to correctly meet the users needs as distances vary.

  Once a change in distance has been detected the alarm is triggered sounding off the buzzers and
  triggering the webcam to snap a picture and immediately send the picture as an attachment in an email
  that the user specified upon startup.

  There is an optional web app included that can be run with flask which will allow the user to access
  the security system and disable it for a single passthrough without triggering the alarm. Once the system
  has detected the passthrough the alarm will be reset and trigger on the next passthrough.

Usage:
  // boot up the security system
  python alarm.py   
  
  // (optional) bootup the webserver to control system through web app
  python manage.py 
