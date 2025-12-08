import FreeCADGui as Gui
from PySide import QtGui, QtCore

class toSketchPreferences(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.form = self

        layout = QtGui.QFormLayout()

        self.tolCoincident = QtGui.QDoubleSpinBox()
        self.tolCoincident.setValue(Gui.ParamGet("User parameter:BaseApp/Preferences/toSketch").GetFloat("TolCoincident", 0.001))
        self.tolCoincident.setDecimals(6)
        layout.addRow("Coincident Tolerance (mm):", self.tolCoincident)

        self.angleLimit = QtGui.QDoubleSpinBox()
        self.angleLimit.setRange(0.1, 30.0)
        self.angleLimit.setValue(Gui.ParamGet("User parameter:BaseApp/Preferences/toSketch").GetFloat("AngleLimitDeg", 2.0))
        layout.addRow("Angle Break (degrees):", self.angleLimit)

        self.debug = QtGui.QCheckBox()
        self.debug.setChecked(Gui.ParamGet("User parameter:BaseApp/Preferences/toSketch").GetBool("Debug", False))
        layout.addRow("Enable Debug Logging:", self.debug)

        self.logFile = QtGui.QLineEdit()
        self.logFile.setText(Gui.ParamGet("User parameter:BaseApp/Preferences/toSketch").GetString("LogFile", "/tmp/toSketch.log"))
        layout.addRow("Log File Path:", self.logFile)

        self.setLayout(layout)

    def saveSettings(self):
        p = Gui.ParamGet("User parameter:BaseApp/Preferences/toSketch")
        p.SetFloat("TolCoincident", self.tolCoincident.value())
        p.SetFloat("AngleLimitDeg", self.angleLimit.value())
        p.SetBool("Debug", self.debug.isChecked())
        p.SetString("LogFile", self.logFile.text())


class toSketchPreferencesPage:
    def __init__(self):
        self.page = toSketchPreferences()

    def getForm(self):
        return self.page.form

    def accept(self):
        self.page.saveSettings()

