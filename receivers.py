from datetime import datetime

try:
    from gpiozero import LED
    LED(1)
except:
    class LED:
        def __init__(self, pin_no):
            self.pin_no = pin_no

        def on(self):
            print('pin {pin} high at {time}'.format(pin=self.pin_no, time=datetime.now()))

        def off(self):
            print('pin {pin} low at {time}'.format(pin=self.pin_no, time=datetime.now()))


class Actuator:

    def __init__(self, pin_no, active_low=False):
        self.pin = LED(pin_no)
        self.active_low = active_low

        self.turn_off()

    def turn_on(self):
        if self.active_low:
            self.pin.off()
        else:
            self.pin.on()

    def turn_off(self):
        if self.active_low:
            self.pin.on()
        else:
            self.pin.off()


class GrowLight(Actuator):

    def __init__(self):
        super().__init__(pin_no=4, active_low=True)


class FloodPump(Actuator):

    def __init__(self):
        super().__init__(pin_no=14, active_low=True)
