class Robot:
    pass

class IA:
    def __init__(self, robotLinked):
        self.robotControled = robotLinked

class Cat(IA):
    def __init__(self, robotLinked, ext):
        super().__init__(robotLinked)
        self.catExtraVar = ext

class Mouse(IA):
    def __init__(self, robotLinked, ext2):
        super().__init__(robotLinked)
        self.mouseExtraVar = ext2

