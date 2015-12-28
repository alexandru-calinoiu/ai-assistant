import pigpio

pi = pigpio.pi()
gpio_pin = 4
pi.set_mode(gpio_pin, pigpio.INPUT)
pi.set_pull_up_down(gpio_pin, pigpio.PUD_DOWN)

last_value = -1
while True:
    value = pi.read(gpio_pin)

    if value != last_value:
        last_value = value
        print(value)
