echo off
REM python ".\src\TrainManagementWebServer.py" ElectronicControler.DummyControler
python ".\src\TrainManagementWebServer.py" ElectronicControler.RSArduinoControler COMPORT:COM8
pause
