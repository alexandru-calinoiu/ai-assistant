import pigpio

pi = pigpio.pi()
gpio_input_pin = 4
pi.set_mode(gpio_input_pin, pigpio.INPUT)
pi.set_pull_up_down(gpio_input_pin, pigpio.PUD_DOWN)

gpio_output_pin = 17
pi.set_mode(gpio_output_pin, pigpio.OUTPUT)


def rising_callback(gpio, level, tick):
    print('Rising: ', gpio, level, tick)
    pi.write(gpio_output_pin, 1)


def failing_callback(gpio, level, tick):
    print('Failing: ', gpio, level, tick)
    pi.write(gpio_output_pin, 0)


pi.callback(gpio_input_pin, pigpio.RISING_EDGE, rising_callback)
pi.callback(gpio_input_pin, pigpio.FALLING_EDGE, failing_callback)

while True:
    continue
