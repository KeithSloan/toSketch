import FreeCADGui as Gui

class toSketchWorkbench(Gui.Workbench):
    MenuText = "toSketch"
    ToolTip = "Tools for cleaning and converting sketch geometry from section cuts"
    Icon = """
        /* XPM */
        static char * icon[] = {
        "16 16 2 1",
        "  c None",
        ". c #000000",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................"};
    """

    def Initialize(self):
        from .toline import CmdToLine
        from .tocurve_guided import CmdToCurveGuided
        from .tocurve_auto import CmdToCurveAuto

        self.cmdList = [
            "toSketch_ToLine",
            "toSketch_ToCurveGuided",
            "toSketch_ToCurveAuto"
        ]

        for c in self.cmdList:
            Gui.addCommand(c, eval(c.replace("toSketch_", "Cmd")))

        self.appendToolbar("toSketch Tools", self.cmdList)
        self.appendMenu("toSketch", self.cmdList)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(toSketchWorkbench())

