import pigpio

pi = pigpio.pi()

gpio_pin = 17
pi.set_mode(gpio_pin, pigpio.OUTPUT)

while True:
    answer = input('What do you want to do: ')

    if answer == 'on':
        pi.write(gpio_pin, 1)
    elif answer == 'off':
        pi.write(gpio_pin, 0)
    elif answer == 'exit':
        break
