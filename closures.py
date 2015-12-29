def generate_power(n):
    print 'id(n): %X' % id(n)

    def nth_power(x):
        return n ** x

    print "id(nth_power): %X" % id(nth_power)
    return nth_power

print generate_power(4)(2)
