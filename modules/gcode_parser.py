import vpype_gcode as v
import subprocess

from modules.gcode_object import GCodeCommand
# from gcode_object import GCodeCommand

class GCodeParser:

    DOBOT_LIMITS = {
        "TOP_X": 280,
        "BOT_X": 190,
        "BOT_Y": -150,
        "TOP_Y": 150,
        "DRAW_Z": -25.69,
        "LIFT_Z": 0
    }

    def __init__(self, filename):
        self._load(filename)
        return
    
    def _load(self, filename):
        index = filename.rfind(".")
        extension = filename[index:]
        match extension:
            case 'svg':
                self._load_svg(filename)
            case 'gcode':
                self._load_gcode(filename)
            case _:
                raise Exception("Unknown file type")

    def _load_gcode(self, filename):
        self.gcode = [] # array of GCodeCommand objects
        with open(filename, 'r') as file:
            for line in file:
                command = GCodeCommand(line)
                self.gcode.append(command)

    def _load_svg(self, filename):
        command = f"vpype read {filename} gwrite --profile gcode data/output.gcode".split()
        subprocess.run(command, capture_output=False)
        self._load_gcode("data/output.gcode")

    def transform(self):
        self._find_bounds()
        self._shift()
        self._scale()

    def _find_bounds(self):
        self.max_x = max(command.X for command in self.gcode)
        self.max_y = max(command.Y for command in self.gcode)
        self.min_x = min(command.X for command in self.gcode)
        self.min_y = min(command.Y for command in self.gcode)

    def _shift(self):
        x_shift = self.DOBOT_LIMITS["BOT_X"] - self.min_x
        y_shift = self.DOBOT_LIMITS["BOT_Y"] - self.min_y
        for command in self.gcode:
            command.X  += x_shift
            command.Y += y_shift
            command.Z = self.DOBOT_LIMITS["DRAW_Z"]

    def _scale(self):
        x_scale = (self.DOBOT_LIMITS["TOP_X"] - self.DOBOT_LIMITS["BOT_X"])/(self.max_x - self.min_x)
        y_scale = (self.DOBOT_LIMITS["TOP_Y"] - self.DOBOT_LIMITS["BOT_Y"])/(self.max_y - self.min_y)
        min_scale = min(x_scale, y_scale)
        for command in self.gcode:
            command.X  = ((command.X - self.DOBOT_LIMITS["BOT_X"]) * min_scale) + self.DOBOT_LIMITS["BOT_X"]
            command.Y = ((command.Y - self.DOBOT_LIMITS["BOT_Y"]) * min_scale) + self.DOBOT_LIMITS["BOT_Y"]

    def display(self):
        for command in self.gcode:
            print(f"{command.X}, {command.Y}, {command.Z}")

    def generate_gcode(self):
        for command in self.gcode:
            print(f"G{command.G} F{command.F} X{command.X} Y{command.Y} Z{command.Z} E{command.E}")
    
if __name__ == "__main__":
    parser = GCodeParser("data/sample.gcode")
    parser.transform()
    parser.generate_gcode()
    print("done")