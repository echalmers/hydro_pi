from datetime import datetime, timedelta, time as datetime_time
import time
from command import Command


class Scheduler:

    class _Task:

        def __init__(self, execute_at, command):
            self.execute_at = execute_at
            self.command = command

        def __call__(self):
            return self.command.action()

    def __init__(self):
        self.tasks = []

    def add(self, command):

        if command.every_day_at:
            if not isinstance(command.every_day_at, datetime_time):
                raise AttributeError('every_day_at parameter must be a time object')
            now = datetime.now()
            run_at = datetime(now.year, now.month, now.day,
                              command.every_day_at.hour,
                              command.every_day_at.minute,
                              command.every_day_at.second)
            if run_at < now:
                run_at += timedelta(days=1)

        elif command.with_period:
            if isinstance(command.with_period, timedelta):
                run_at = datetime.now() + command.with_period

            elif isinstance(command.with_period, tuple) and \
                    isinstance(command.with_period[0], datetime) and \
                    isinstance(command.with_period[1], timedelta):
                run_at = command.with_period[0] + command.with_period[1]

            else:
                raise AttributeError('with_period parameter must be a timedelta object, or a (datetime, timedelta) tuple')

            command.with_period = (run_at, command.with_period if isinstance(command.with_period, timedelta) else command.with_period[1])

        elif command.once_relative:
            if not isinstance(command.once_relative, timedelta):
                raise AttributeError('once_relative parameter must be a timedelta object')
            run_at = datetime.now() + command.once_relative

        elif command.once_absolute:
            if not isinstance(command.once_absolute, datetime):
                raise AttributeError('once_absolute parameter must be a datetime object')
            run_at = command.once_absolute

        else:
            return

        self.tasks.append(
            self._Task(execute_at=run_at,
                       command=command
                       )
        )
        self.tasks.sort(key=lambda x: x.execute_at)

    def run(self):

        while len(self.tasks) > 0:

            if self.tasks[0].execute_at <= datetime.now():

                # re-schedule the next run of this command
                if not (self.tasks[0].command.once_absolute or self.tasks[0].command.once_relative):
                    self.add(self.tasks[0].command)

                # run the command
                self.tasks[0]()

                # schedule any follow-up commands
                if self.tasks[0].command.follow_up_command:
                    self.add(self.tasks[0].command.follow_up_command)

                # pop from the list of tasks
                self.tasks.remove(self.tasks[0])

            else:
                time.sleep(1)
