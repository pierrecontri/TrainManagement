#!/bin/bash

function Compile-PyModule {
  param(
    [String]$ModuleFolder,
    [String[]]$ModulesName
  )

  Write-Output "Compile folder${ModuleFolder}"

  $ModulesName | % {
    $tmpmodule = $_;
    Write-Output "  Compile module: ${tmpmodule}";
    & python -c $("import py_compile; py_compile.compile('./src/" + $ModuleFolder + "/" + ${tmpmodule} + ".py', './Build/" + $ModuleFolder + "/" + ${tmpmodule} + ".pyc')").ToString()
  }
}

# compile all models
$models = @("ControlPanel", "DirectionCommand", "LightCommand", "SwitchCommand")
Compile-PyModule -ModuleFolder "Model" -ModulesName $models

# compile electronics components (if needed)
$elecComponents = @("InitGPIO", "SevenDigitsGPIO", "SN74HC595", "StopButton", "EightDigitsGPIO")
Compile-PyModule -ModuleFolder "ElectronicComponents" -ModulesName $elecComponents

# compile all independants libraries
$electControlers = @("DummyControler", "I2CArduinoControler", "PiControler", "RSArduinoControler")
Compile-PyModule -ModuleFolder "ElectronicControler" -ModulesName $electControlers

# compile the Controler abstract base class
$controlers = @("TrainManagementControler")
Compile-PyModule -ModuleFolder "Controler" -ModulesName $controlers

# compile the TrainIO
$trainIO = @("SwitchsCommand", "TrainDirection")
Compile-PyModule -ModuleFolder "TrainIO" -ModulesName $trainIO
