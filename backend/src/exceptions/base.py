class BaseExceptions(Exception):
    msg: str

    def message(self):
        ...
