class Transmit:
    global_data = {}

    class To:
        def __setattr__(self, name, value):
            Transmit.global_data[name] = value if not isinstance(value, tuple) else list(value)

    class Me:
        def __getattr__(self, name):
            return Transmit.global_data.get(name)

    def __init__(self):
        self.to = Transmit.To()
        self.me = Transmit.Me()
