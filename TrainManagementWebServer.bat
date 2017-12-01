echo off
".\Build\UI\TrainManagement.html"
REM python ".\src\TrainManagementWebServer.py" ElectronicControler.DummyControler
REM python ".\src\TrainManagementWebServer.py" ElectronicControler.RSArduinoControler COMPORT:COM8
python ".\Build\TrainManagementWebServer.pyc"
pause
