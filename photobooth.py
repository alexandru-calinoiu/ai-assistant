import pigpio
import cv2
import requests
import datetime
import json


class pressstate:
    pressed = False

    def press(self):
        self.pressed = True

    def not_pressed(self):
        return self.pressed == False


class gpiocontrol(object):
    pi = None
    gpio_pin = None

    def __init__(self, pi, gpio_pin):
        self.pi = pi
        self.gpio_pin = gpio_pin


class buttoncontrol(gpiocontrol):
    def __init__(self, pi, gpio_pin=4):
        super(buttoncontrol, self).__init__(pi, gpio_pin)

    def setup(self, rising_callback):
        self.pi.set_mode(self.gpio_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.gpio_pin, pigpio.PUD_DOWN)
        return self.pi.callback(self.gpio_pin, pigpio.RISING_EDGE, rising_callback)


class ledcontrol(gpiocontrol):
    def __init__(self, pi, gpio_pin=17):
        super(ledcontrol, self).__init__(pi, gpio_pin)

    def setup(self):
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)

    def on(self):
        self.setup()
        self.pi.write(self.gpio_pin, 1)

    def off(self):
        self.setup()
        self.pi.write(self.gpio_pin, 0)


class facedetector:
    HAAR_CASCADE_PATH = ''

    detect_image_path = ''
    haar_cascade_path = ''

    def __init__(self, detect_image_path='detect.png', haar_cascade_path='trainer/haarcascade_frontalface_alt.xml'):
        self.detect_image_path = detect_image_path
        self.haar_cascade_path = haar_cascade_path

    def detect(self, img):
        cascade = cv2.CascadeClassifier(self.haar_cascade_path)
        rects = cascade.detectMultiScale(img, 1.1, 4, 0, (30, 30))
        rects = [] if len(rects) == 0 else rects
        self.box(img, rects)

    def box(self, img, rects):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 125, 0), 2)
        cv2.imwrite(self.detect_image_path, img)


class agilebot:
    base_url = ''

    def __init__(self, base_url='http://109.103.226.38:8080/hubot'):
        self.base_url = base_url

    def photo_taken(self, room='5489460edb8155e6700ddfdc'):
        url = self.base_url + '/aidoorkeeper/photo/' + room
        data = {"date": datetime.datetime.utcnow().isoformat()}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=json.dumps(data), headers=headers)


def run():
    pi = pigpio.pi()

    press_state = pressstate()
    led_control = ledcontrol(pi)
    button_control = buttoncontrol(pi)

    def rising_callback(gpio, level, tick):
        print('Say cheese!', gpio, level, tick)
        callback.cancel()
        press_state.press()

    callback = button_control.setup(rising_callback)

    print 'Pres the red button!'

    while press_state.not_pressed():
        continue

    led_control.on()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ret, img = cap.read()
    cv2.imwrite('picture.png', img)

    bot = agilebot()
    bot.photo_taken()

    cap.release()
    led_control.off()


run()
