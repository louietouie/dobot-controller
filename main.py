from modules.gcode_parser import GCodeParser
from third_party.dobot.include import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

def send_commands(gcode):
    for command in gcode:
        lastIndex = dType.SetPTPCmd(api, 2, command.X, command.Y, command.Z, 0, 1)
    return lastIndex[0]
    
def execute_commands(gcode):
    dType.SetQueuedCmdClear(api)
    lastIndex = send_commands(gcode)
    dType.SetQueuedCmdStartExec(api)
    # dType.SetPTPCoordinateParamsEx(api,200,1000,200,1000,1)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    dType.SetQueuedCmdStopExec(api)

if __name__ == "__main__":
    api = dType.load()
    state = dType.ConnectDobot(api, "", 115200)[0]

    if (state == dType.DobotConnect.DobotConnect_NoError):
        parser = GCodeParser("data/sample.gcode")
        parser.transform()
        parser.generate_gcode()
        execute_commands(parser.gcode)
        dType.DisconnectDobot(api)