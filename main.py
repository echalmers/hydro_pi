from receivers import GrowLight, FloodPump
from schedule import Scheduler
from command import Command
from datetime import datetime, timedelta, time

# instantiate receivers
light = GrowLight()
pump = FloodPump()

# instantiate scheduler
s = Scheduler()

# turn the light on each morning
s.add(Command(action=light.turn_on, every_day_at=time(8, 0)))

# turn light off each night
s.add(Command(action=light.turn_off, every_day_at=time(20, 0)))

# run flood pump for 7 minutes every 3 hours
s.add(Command(action=pump.turn_on, with_period=timedelta(hours=3),
              follow_up_command=Command(action=pump.turn_off, once_relative=timedelta(minutes=7))))

s.run()
