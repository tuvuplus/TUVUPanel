from Components.config import config, ConfigSubsection, ConfigText, \
	getConfigListEntry
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Tools.Directories import fileExists, copyfile
from Components.Sources.List import List
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer
from Plugins.Plugin import PluginDescriptor
from Components.MenuList import MenuList
from Components.FileList import FileList
from Screens.InputBox import InputBox 
from Screens.ChoiceBox import ChoiceBox
from Components.Pixmap import Pixmap
from os import listdir
from xml.dom import Node
from xml.dom import minidom
from time import sleep
import os
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, eListboxPythonMultiContent, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, getDesktop, loadPNG, loadPic
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from enigma import *
from Screens.Console import Console
from twisted.web.client import downloadPage
from twisted.web.client import getPage
import urllib
from enigma import *
from os import listdir


SCREEN_SOFTCAM = """
    <screen position="center,center" size="1280,720" title="TUVUPanel">
		<ePixmap position="0,0" zPosition="-1" size="1279,719" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/fondo.png"/>
		<eLabel position="center,center" size="1280,720" transparent="0" zPosition="-15" />
		<widget source="session.CurrentService" render="RunningText" options="movetype=running,startpoint=0,direction=left,steptime=25,repeat=150,startdelay=1500,always=0" position="101,450" size="215,45" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#2EFEF7" foregroundColor="#FFFFFF" noWrap="1" halign="center">
			<convert type="ServiceName">Name</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="850,42" size="300,55" backgroundColor="un140b1" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#FFFFFF" shadowOffset="-2,-2">
		  <convert type="ClockToText">Date</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="899,20" size="251,55" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#FFFFFF" shadowOffset="-2,-2">
		  <convert type="ClockToText">Format:%-H:%M</convert>
		</widget>
		<eLabel position="60,637" size="229,50" transparent="1" foregroundColor="#FFFFFF" backgroundColor="#2E64FE" text="Tuvuplus.com" font="Regular;30" zPosition="1" halign="center" valign="bottom" />
		<eLabel position="611,181" size="629,431" transparent="0" foregroundColor="white" backgroundColor="#6e6e6e" zPosition="-10" />
		<widget name="menu" position="641,140" size="629,431" scrollbarMode="showOnDemand" transparent="1" itemHeight="60" />
		<widget source="session.VideoPicture" render="Pig" position="44,136" size="498,208" backgroundColor="transparent" zPosition="-1" transparent="0" />
		
		<eLabel backgroundColor="red" position="650,640" size="120,5" zPosition="0" />
		<eLabel backgroundColor="green" position="800,640" size="120,5" zPosition="0" />
		<eLabel backgroundColor="yellow" position="950,640" size="120,5" zPosition="0" />
		eLabel backgroundColor="#6492D4" position="1100,640" size="120,5" zPosition="0" />
		<widget font="Regular;16" halign="center" name="key_red" position="650,650" size="120,35" transparent="1" valign="center" zPosition="2" />
		<widget font="Regular;16" halign="center" name="key_green" position="800,650" size="120,35" transparent="1" valign="center" zPosition="2" />
		<widget font="Regular;16" halign="center" name="key_yellow" position="950,650" size="120,35" transparent="1" valign="center" zPosition="2" />
		<widget font="Regular;16" halign="center" name="key_blue" position="1100,650" size="120,35" transparent="1" valign="center" zPosition="2" />
	</screen>"""
		
class SoftcamPanel(ConfigListScreen, Screen):
	def __init__(self, session):
		global emuDir
		emuDir = "/usr/tuvuscripts"
		self.service = None
		Screen.__init__(self, session)

		self.skin = SCREEN_SOFTCAM
		self.partyfeed = None
		#self.YellowAction = REFRESH

		camsList = []
		self["key_green"] = Label(_("Restart"))
		self["key_red"] = Label(_("Stop"))
		self["key_yellow"] = Label(_("Actualizar"))
		self["key_blue"] = Label(_("Instalar CAM"))
		self.partyfeed = os.path.exists("/etc/opkg/3rdparty-feed.conf") or os.path.exists("/etc/opkg/3rd-party-feed.conf")
		for script in os.listdir(emuDir):
			if script.endswith(".tuvuscript"):
				camsList.append(script)
				
		self['menu'] = MenuList(camsList)
		#// get the remote buttons
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"cancel": self.Exit,
			"ok": self.ok,
			"blue": self.Blue,
			"red": self.Red,
			"green": self.Green,
			"yellow": self.Yellow,
		}, -1)
		
	def Exit(self):
		self.close()
		
	def ok(self):
		pass
		
	def Blue(self):
		self.session.open(installCam)
		
	def Red(self):
		self.close()
		
	def Green(self):
		pass
		
	def Yellow(self):
		pass
	


	
	
	
	
	
###OBTENER CAMS DEL SERVIDOR + DESCARGA E INSTALACION##
SCREEN_INSTALLCAM = """
    <screen position="center,center" size="1280,720" title="TUVUPanel">
		<ePixmap position="0,0" zPosition="-1" size="1279,719" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/fondo.png"/>
		<eLabel position="center,center" size="1280,720" transparent="0" zPosition="-15" />
		<widget source="session.CurrentService" render="RunningText" options="movetype=running,startpoint=0,direction=left,steptime=25,repeat=150,startdelay=1500,always=0" position="101,450" size="215,45" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#2EFEF7" foregroundColor="#FFFFFF" noWrap="1" halign="center">
			<convert type="ServiceName">Name</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="850,42" size="300,55" backgroundColor="un140b1" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#FFFFFF" shadowOffset="-2,-2">
		  <convert type="ClockToText">Date</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="899,20" size="251,55" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#FFFFFF" shadowOffset="-2,-2">
		  <convert type="ClockToText">Format:%-H:%M</convert>
		</widget>
		<eLabel position="60,637" size="229,50" transparent="1" foregroundColor="#FFFFFF" backgroundColor="#2E64FE" text="Tuvuplus.com" font="Regular;30" zPosition="1" halign="center" valign="bottom" />
		<eLabel position="611,181" size="629,431" transparent="0" foregroundColor="white" backgroundColor="#6e6e6e" zPosition="-10" />
		<widget name="menu" position="641,140" size="629,431" scrollbarMode="showOnDemand" transparent="1" itemHeight="60" />
		<widget source="session.VideoPicture" render="Pig" position="44,136" size="498,208" backgroundColor="transparent" zPosition="-1" transparent="0" />
		<eLabel backgroundColor="red" position="650,640" size="120,5" zPosition="0" />
		<eLabel backgroundColor="green" position="800,640" size="120,5" zPosition="0" />
		<widget font="Regular;16" halign="center" name="key_red" position="650,650" size="120,35" transparent="1" valign="center" zPosition="2" />
		<widget font="Regular;16" halign="center" name="key_green" position="800,650" size="120,35" transparent="1" valign="center" zPosition="2" />
	</screen>"""
	
class installCam(ConfigListScreen, Screen):
	def __init__(self, session):
		self.service = None
		Screen.__init__(self, session)
		listCams = []
		self.skin = SCREEN_INSTALLCAM
		self["key_green"] = Label(_("Descargar"))
		self["key_red"] = Label(_("Inicio"))
		#// get the remote buttons

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"cancel": self.Red,
			"ok": self.checkXML,
			"red": self.Red,
		}, -1)
		
	def Red(self):
		self.close()
		
	def checkXML(self):
		url = "http://tuvuplus.com/app/files/servidor.xml"
		getPage(url).addCallback(self.loadCam).addErrback(self.errorPage)

	def errorPage(self, error):
		pass
	
	def loadCam(self, data):
		self.xml = data
		try:
			if self.xml:
				xmlstr = minidom.parseString(self.xml)
				listCams = []
				for plugins in xmlstr.getElementsByTagName('plugins'):
					if "CAMS" in plugins.getAttribute('cont').encode('utf8'): 
						self.listCams.append(plugins.getAttribute('name').encode('utf8'))
						
					else:
						self['info'].setText('Ha fallado, o no tienes conexion a internet o el servidor KO !')
				return
				self['menu'] = MenuList(listCams)
		except:
			self['info'].setText('Error datos servidor')
	
