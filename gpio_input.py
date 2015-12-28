import pigpio

pi = pigpio.pi()
gpio_pin = 4
pi.set_mode(gpio_pin, pigpio.INPUT)
pi.set_pull_up_down(gpio_pin, pigpio.PUD_DOWN)


def rising_callback(gpio, level, tick):
    print('Rising: ', gpio, level, tick)


def failing_callback(gpio, level, tick):
    print('Failing: ', gpio, level, tick)


pi.callback(gpio_pin, pigpio.RISING_EDGE, rising_callback)
pi.callback(gpio_pin, pigpio.FALLING_EDGE, failing_callback)

while True:
    continue
