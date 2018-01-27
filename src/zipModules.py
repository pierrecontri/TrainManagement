import Model
import os.path as pth
import zipfile

#Get abs path about this file
absFilePath = pth.abspath(__file__)
#Get abs directory about this file
absFileDirectoryPath = pth.dirname(absFilePath)
#Join into this directory sub module directory
modulesZipPyc = pth.join(absFileDirectoryPath, 'TrainLibraries.zip')
#Create the basename for writepy method
lstModules = ('Model', 'ElectronicModel', 'Controller', 'ElectronicComponents', 'TrainIO')
with zipfile.PyZipFile(modulesZipPyc, 'w', zipfile.ZIP_DEFLATED) as zfile:
  for tmpModuleName in lstModules:
    pathNameWritePy = pth.join(absFileDirectoryPath, tmpModuleName)
    zfile.writepy(pathNameWritePy)
  zfile.close()
