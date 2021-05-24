#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
from datetime import date
from copy import *
from types import *

import os
import os.path as pth
import sys
from subprocess import call, Popen

import inspect

#Get abs path about this file
absFilePath = pth.abspath('__file__')
#Get abs directory about this file
absFileDirectoryPath = pth.dirname(absFilePath)
#Join into this directory sub module directory
modulesPyc = pth.join(absFileDirectoryPath, 'modules')
#Calcul HMI path
uiPath = pth.join(absFileDirectoryPath, 'TrainManagement.glade')

#Default data directory
dataDir = pth.normpath(pth.join(absFileDirectoryPath, '..', 'data'))

#import owns application's modules
sys.path.append(modulesPyc)

#import zipfile module if exist
zipmodule = pth.join(modulesPyc, 'modelizing.zip')
if pth.exists(zipmodule):
	sys.path.append(zipmodule)

class winInterface(object):

	def __init__(self, datafilename = ""):
		global uiPath
		self._datafilename = datafilename
		self.widgets = gtk.glade.XML(uiPath)
		self.autoConnect()

	def __getitem__(self, widgetName):
		return self.widgets.get_widget(widgetName)

	def autoConnect(self):
		events = {}
		for (itemName, value) in self.__class__.__dict__.items():
			if callable(value) and itemName.startswith('gtk_'):
				events[itemName[4:]] = getattr(self, itemName)
		self.widgets.signal_autoconnect(events)
		# main frame managment
		self['windowCalulVoiture'].connect('destroy', self.gtk_main_quit)
		self['windowCalulVoiture'].connect('delete-event', self.delete_event)
		self['windowEditCar'].connect('delete-event', self.delete_event)


	def gtk_openFile(self, source = None, event = None):
		global dataDir
		dialog = gtk.FileChooserDialog("Open ...", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_current_folder(dataDir)
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("XmlData")
		filter.add_mime_type("data/xml")
		filter.add_pattern("*.xml")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		dialog.add_filter(filter)

		response = dialog.run()
		dialog.hide()
		if response == gtk.RESPONSE_OK:
			self.dataLoader(dialog.get_filename())
		elif response == gtk.RESPONSE_CANCEL:
			logger.info('Closed, no files selected')
		dialog.destroy()
		return

	def gtk_saveFile(self, source = None, event = None):
		if self._datafilename == "":
			self.gtk_saveAsFile()
		else:
			XmlCarManage.ExportDataToXML(self._datafilename)
			logger.info("File '" + self._datafilename + "' saved")
		return

	def gtk_saveAsFile(self, source = None, event = None):
		global dataDir
		dialog = gtk.FileChooserDialog("Save ...", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		dialog.set_current_folder(dataDir)
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("XmlData")
		filter.add_mime_type("data/xml")
		filter.add_pattern("*.xml")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("CsvData")
		filter.add_mime_type("data/csv")
		filter.add_pattern("*.csv")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("TxtData")
		filter.add_mime_type("data/txt")
		filter.add_pattern("*.txt")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		dialog.add_filter(filter)

		saveFile = False
		response = dialog.run()
		tmpFileName = ""
		if response == gtk.RESPONSE_OK:
			tmpFileName = dialog.get_filename()

			if not pth.exists(tmpFileName):
				saveFile = True
			else:
				msgBox = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format=None)
				msgBox.set_markup("The file '" + tmpFileName + "' already exists.\nDo you want to replace it ?")
				resp2 = msgBox.run()
				msgBox.hide()
				if resp2 == gtk.RESPONSE_YES:
					saveFile = True
				msgBox.destroy()
		elif response == gtk.RESPONSE_CANCEL:
			logger.info('Closed, no files selected')
		dialog.hide()
		dialog.destroy()
		# Exports XmlData to tmpFileName
		if saveFile:
			self._datafilename = tmpFileName
			XmlCarManage.ExportDataToXML(self._datafilename)
			logger.info("File saved as '" + tmpFileName + "'")
		return


	def gtk_main_quit(self, source = None, event = None):
		gtk.main_quit()


	def delete_event(self, source = None, event=None):
		# don't destroy window -- just leave it hidden
		# for now .. fix later
		source.hide()
		return

	def gtk_showAbout(self, source = None, event = None):
		if self['aboutdialogapp'] != None:
			self['aboutdialogapp'].run()
			self['aboutdialogapp'].hide()
		else:
			logger.warning("Error creating widget about for 'def gtk_showAbout'")
		return


### main

if __name__ == '__main__':
	fileName = ""
	if len(sys.argv) > 1:
		fileName = sys.argv[1]
	mainWindow = winInterface(fileName)
	gtk.main()
