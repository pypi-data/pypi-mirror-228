class transmit:
    global_data = {}

    class To:
        def __setattr__(self, name, value):
            transmit.global_data[name] = value if not isinstance(value, tuple) else list(value)

    class Me:
        def __getattr__(self, name):
            return transmit.global_data.get(name)

    def __init__(self):
        self.to = transmit.To()
        self.me = transmit.Me()
