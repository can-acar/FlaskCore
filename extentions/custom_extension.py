from src.lib.extension import extension


@extension(str)
def toString(self) -> str:
    return self.__name__.split(".")[-1]


@extension(str)
class CustomeExtension:
    def __init__(self):
        pass

    def __str__(self):
        return self.__name__.split(".")[-1]

    @staticmethod
    def toLowerCase2(self):
        return self.lower()


def test():
    test_string = 'test'
    print(test_string.toLowerCase2())
