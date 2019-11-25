

class Command:

    def __init__(self, action, every_day_at=None, with_period=None, once_relative=None, once_absolute=None,
                 follow_up_command=None):

        self.action = action

        self.every_day_at = every_day_at
        self.with_period = with_period
        self.once_relative = once_relative
        self.once_absolute = once_absolute
        if all([x is None for x in [every_day_at, with_period, once_relative, once_absolute]]):
            raise AttributeError('one scheduling parameter must be supplied')

        self.follow_up_command = follow_up_command

