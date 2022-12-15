import time

def do_every(period,f,*args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

def hello(s):
    print('hello {} ({:.4f})'.format(s,time.time()))
    #time.sleep(.3)

do_every(0.250,hello,'foo')