class BooleanField:
    def __new__(cls, arg: str):
        return arg.lower() in ("yes", "true", "t", "1")
