class CustomError:

    def __init__(self, name, default_message="An error occured"):
        self.name = f"{name}"
        self.default_msg = default_message
        self.exception = type(self.name, (Exception,), {"__init__": self.__patch_init})

    def throw(self, msg=None):
        if msg is None:
            msg = self.default_msg

        def __throw(msg):
            raise self.exception(msg)

        __throw(msg=msg)

    def __patch_init(self, msg):
        __class__ = type(self)

        def __init_method(self, msg):
            print(self, msg)
            print(type(self))
            super().__init__()

        __class__.__init__ = __init_method

    def __str__(self):
        return f"{self.name} Exception"
