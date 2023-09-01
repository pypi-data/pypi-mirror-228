class InvalidURLException(Exception):
    def __init__(self, message:str = "This is invalid URL"):
        self.message = message
        super().__init__(self.message)