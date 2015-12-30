import pigpio
import cv2


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
    def __init__(self, pi, gpio_pin = 4):
        super(buttoncontrol, self).__init__(pi, gpio_pin)

    def setup(self, rising_callback):
        self.pi.set_mode(self.gpio_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.gpio_pin, pigpio.PUD_DOWN)
        return self.pi.callback(self.gpio_pin, pigpio.RISING_EDGE, rising_callback)

class ledcontrol(gpiocontrol):
    def __init__(self, pi, gpio_pin = 17):
        super(ledcontrol, self).__init__(pi, gpio_pin)

    def setup(self):
        self.pi.set_mode(self.gpio_pin, pigpio.OUTPUT)

    def on(self):
        self.setup()
        self.pi.write(self.gpio_pin, 1)

    def off(self):
        self.setup()
        self.pi.write(self.gpio_pin, 0)

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
    cv2.imwrite('test.png', img)

    cap.release()
    led_control.off()

run()
