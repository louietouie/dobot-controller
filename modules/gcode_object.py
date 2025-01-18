class GCodeCommand:

    def __init__(self, command):
        self.parsers(command)

    def parsers(self, command):
        phrases = command.split(" ")
        for phrase in phrases:
            id = phrase[0]
            data = float(phrase[1:])
            setattr(self, id, data) # TODO: better way to set attributes?

    # def transform(self, scale, shift):
    #     self._x = (self.x - shift)/scale
    #     self._y =
    #     self._z = 

    # def isvalid(self):
    #     return True