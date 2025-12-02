import sys
import FreeCAD

class _Redirect:
    def write(self, msg):
        FreeCAD.Console.PrintMessage(str(msg))
    def flush(self):
        pass

sys.stdout = _Redirect()
sys.stderr = _Redirect()
