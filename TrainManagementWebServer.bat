echo off
REM python "%myDocs%\Info\TrainManagement\TrainManagementWebServer.py" ElectronicControler.DummyControler
python "%myDocs%\Info\TrainManagement\TrainManagementWebServer.py" ElectronicControler.RSArduinoControler COMPORT:COM8
pause
