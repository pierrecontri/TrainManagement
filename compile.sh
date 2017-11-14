#!/bin/bash

# compile all independants libraries
python3 -c "import py_compile; py_compile.compile('./src/ElectronicControler/DummyControler.py', './Build/ElectronicControler/DummyControler.pyc')"
python3 -c "import py_compile; py_compile.compile('./src/ElectronicControler/I2CArduinoControler.py', './Build/ElectronicControler/I2CArduinoControler.pyc')"
python3 -c "import py_compile; py_compile.compile('./src/ElectronicControler/PiControler.py', './Build/ElectronicControler/PiControler.pyc')"
python3 -c "import py_compile; py_compile.compile('./src/ElectronicControler/RSArduinoControler.py', './Build/ElectronicControler/RSArduinoControler.pyc')"

# compile and zip modules
echo "Zip internal modules"
python3 "./src/zipModules.py"
echo "Move libraries on Build folder"
mv "./src/TrainLibraries.zip" "./Build/"

# compile web server and main controler
echo "Compile web server and main controler"
python3 -c "import py_compile; py_compile.compile('./src/TrainManagementWebServer.py', './Build/TrainManagementWebServer.pyc')"

# copy GUI
echo "Copy GUI folder to Build"
cp -R "./src/UI" "./Build/"
