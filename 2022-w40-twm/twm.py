import subprocess

class BackgroundSwitcherApp:

    """
    I change to different desktop background depending on hour of day.

    I can set a background:

    >>> events = []
    >>> process = Process.create_null()
    >>> process.listen(events.append)
    >>> clock = Clock.create_null(hour_of_day=9)
    >>> app = BackgroundSwitcherApp(process=process, clock=clock)
    >>> app.run()
    >>> events == [{'type': 'RUN', 'command': ['/usr/bin/changebg', ImageSelector().get_image(hour_of_day=9)]}]
    True

    I can be instantiated:

    >>> isinstance(BackgroundSwitcherApp.create(), BackgroundSwitcherApp)
    True
    """

    @staticmethod
    def create():
        return BackgroundSwitcherApp(
            process=Process.create(),
            clock=Clock.create()
        )

    def __init__(self, process, clock):
        self.process = process
        self.clock = clock

    def run(self):
        hour_of_day = self.clock.get_hour_of_day()
        image = ImageSelector().get_image(hour_of_day)
        self.process.run(['/usr/bin/changebg', image])

class ImageSelector:

    """
    >>> ImageSelector().get_image(hour_of_day=5)
    'morning.png'

    >>> ImageSelector().get_image(hour_of_day=13)
    'afternoon.png'
    """

    def get_image(self, hour_of_day):
        if hour_of_day > 12:
            return 'afternoon.png'
        else:
            return 'morning.png'

class Observable:

    def __init__(self):
        self.event_listeners = []

    def listen(self, event_listener):
        self.event_listeners.append(event_listener)

    def notify(self, event):
        for event_listener in self.event_listeners:
            event_listener(event)

class Process(Observable):

    """
    I run commands on the system:

    >>> subprocess.check_output([
    ...     "python", "-c",
    ...     "import twm; twm.Process.create().run(['echo', 'hello'])",
    ... ])
    b'hello\\n'

    I can capture output from commands:

    >>> Process.create().run(["echo", "hello"], capture=True)
    b'hello\\n'

    The null version can simulate output from commands:

    >>> process = Process.create_null(responses=[b'first\\n', b'second\\n'])
    >>> process.run(["irrelevant-command"], capture=True)
    b'first\\n'
    >>> process.run(["irrelevant-command"], capture=True)
    b'second\\n'

    You can observe what commands I run:

    >>> events = []
    >>> process = Process.create_null()
    >>> process.listen(events.append)
    >>> process.run(['some', 'command'])
    >>> events
    [{'type': 'RUN', 'command': ['some', 'command']}]

    The null version of me does not actually run commands:

    >>> Process.create_null().run(["/usr/bin/i-do-not-exist"])
    """

    @staticmethod
    def create():
        return Process(subprocess=subprocess)

    @staticmethod
    def create_null(responses=[]):
        class NullSubprocess:
            def call(self, command):
                pass
            def check_output(self, command):
                return responses.pop(0)
        return Process(subprocess=NullSubprocess())

    def __init__(self, subprocess):
        Observable.__init__(self)
        self.subprocess = subprocess

    def run(self, command, capture=False):
        return_value = None
        if capture:
            return_value = self.subprocess.check_output(command)
        else:
            self.subprocess.call(command)
        self.notify({"type": "RUN", "command": command})
        return return_value

class Clock:

    """
    I can simulate hour of day:

    >>> Clock.create_null(hour_of_day=5).get_hour_of_day()
    5

    >>> isinstance(Clock.create().get_hour_of_day(), int)
    True

    I can be instantiated:

    >>> isinstance(Clock.create(), Clock)
    True
    """

    @staticmethod
    def create():
        return Clock(process=Process.create())

    @staticmethod
    def create_null(hour_of_day):
        return Clock(process=Process.create_null(
            responses=[f"{hour_of_day}\n".encode("ascii")]
        ))

    def __init__(self, process):
        self.process = process

    def get_hour_of_day(self):
        return int(self.process.run(["date", "+%H"], capture=True))

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        import doctest
        if doctest.testmod(
            optionflags=doctest.REPORT_NDIFF|doctest.FAIL_FAST
        ).failed == 0:
            print("OK")
    else:
        BackgroundSwitcherApp.create().run()
