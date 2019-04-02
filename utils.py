from gtts import gTTS
import requests
import json
import smtplib
import uuid
import os
import glob

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


class TempImage:
    def __init__(self, basePath="./", ext=".jpg"):
        # construct the file path
        self.path = "{base_path}/{rand}{ext}".format(base_path=basePath,
                                                     rand=str(uuid.uuid4()), ext=ext)

    def cleanup(self):
        # remove the file
        os.remove(self.path)


def send_email(conf):
    fromaddr = "address@gmail.com"
    for email_address in conf['email_address']:
        toaddrs = email_address
        print("[INFO] Emailing to {}".format(email_address))
        text = 'Hey Someone in Your House!!!!'
        subject = 'Security Alert!!'
        message = 'Subject: {}\n\n{}'.format(subject, text)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddrs
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        # set attachments
        files = glob.glob("/tmp/talkingraspi*")
        print("[INFO] Number of images attached to email: {}".format(len(files)))
        for f in files:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                    f)
                msg.attach(part)

        # Credentials (if needed) : EDIT THIS
        username = "gmail_username"
        password = "password"

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()


def send_mail(conf, files=None,
              ):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


def playVidwaitButton(mov1, mov2, pin):
    import RPi.GPIO as GPIO
    from subprocess import Popen, PIPE, STDOUT
    import time
    # setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    DEVNULL = open(os.devnull, 'wb')
    # Play first video in loop via omxplayer
    omxc = Popen(['omxplayer', '-b', '--loop', mov1],
                 stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    while GPIO.input(pin) == GPIO.HIGH:
        time.sleep(0.01)
    # if the button is pressed--> Play the second one
    os.system('killall omxplayer.bin')
    omxc = Popen(['omxplayer', '-b', mov2], stdin=PIPE,
                 stdout=DEVNULL, stderr=STDOUT)
    # Wait for duration of video
    time.sleep(10)
    # And start again from the top
    # playVidwaitButton(mov1, mov2, pin)
    GPIO.cleanup()


def say_weather(speech):
    filename = 'speech.mp3'
    tts = gTTS(text=speech, lang='de').save(filename)
    play_sound(filename)


def play_sound(filename):
    """ Helper function to play audio files in Linux """
    play_cmd = "mpg123 {} {} ./{}".format('--quiet --pitch',
                                          4.00, filename)
    os.system(play_cmd)
