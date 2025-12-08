import FreeCAD
import FreeCADGui as Gui
import datetime

def log(msg):
    p = Gui.ParamGet("User parameter:BaseApp/Preferences/toSketch")
    debug = p.GetBool("Debug", False)
    logfile = p.GetString("LogFile", "/tmp/toSketch.log")

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[toSketch {timestamp}] {msg}"

    if debug:
        try:
            with open(logfile, "a") as f:
                f.write(line + "\n")
        except Exception as e:
            FreeCAD.Console.PrintError(f"Logging error: {e}\n")

        FreeCAD.Console.PrintMessage(line + "\n")

