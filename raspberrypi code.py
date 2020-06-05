from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7,GPIO.OUT)

p = GPIO.PWM(7,50)
p.start(2.5)
APP_ID = '20195098'
API_KEY = 'nCRKhxecqlDT46DQysR2x7FY'
SECRET_KEY = '10BsnqqqAh0kpxFbL7qwTy2KsehVvmnF'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
IMAGE_TYPE = 'BASE64'
camera = PiCamera()
GROUP = 'Users'
def getimage():
    camera.resolution = (1024,768)
    camera.start_preview()
    time.sleep(2)
    camera.capture('faceimage.jpg')
    time.sleep(2)
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)
    if result['error_msg'] == 'SUCCESS':
        name = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        if score > 80:
            if name == '1':
                print("welcome Yuxing")
                time.sleep(3)
                return 1
        else:
            print("Sorry I don't know you")
            name = 'Unknown'
            time.sleep(3)
            return 0
    if result['error_msg'] == 'pic not has face':
        print("No face detected.")
        time.sleep(2)
        return 0
if __name__ == '__main__':
    try:
        while True:
            print('ready')
            if True:
                getimage()
                img = transimage()
                res = go_api(img)
                if(res == 1):
                    print("open")
                    p.ChangeDutyCycle(7.5)
                    time.sleep(3)
                    p.ChangeDutyCycle(2.5)
                else:
                    print("close")
                    time.sleep(3)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
