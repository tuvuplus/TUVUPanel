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
import cams
from Plugins.Extensions.TUVUPanel.softcam import *
currversion = '0.9'
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/'


### DECLARAMOS LOS SCREEN ###
SCREEN_INI = """
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
	</screen>"""
	
SCREEN_IPTV = """
    <screen position="center,center" size="1280,720" title="TUVUPanel - iptv">
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
	</screen>"""

SCREEN_SWAP = """
    <screen position="center,center" size="1280,720" title="TUVUPanel - swap">
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
	</screen>"""

SCREEN_CLEAN_MEMORY = """
    <screen position="center,center" size="1280,720" title="TUVUPanel - Liberador memoria">
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
	</screen>"""

SCREEN_DOWNLOADS =  """
          <screen position="center,center" size="1280,720" title="TUVUPanel - Descargas">
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
	</screen>"""

#skin emus

SCREEN_SoftcamPanel =  """
          <screen position="center,center" size="1280,720" title="TUVUPanel - Emus">
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
	</screen>"""
            



Cmenu_list = [_('Cams'),
 _('Actualizar Iptv'),
 _('Swap'),
 _('Liberar memoria'),
 _('Descargas')]
 
 
class CmenuList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setItemHeight(20)
        self.l.setFont(0, gFont('Regular', 32)) 
        
        
def CmenuListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/guia.png'
    elif idx == 1:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/guia.png'
    if idx == 2:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/guia.png'    
    elif idx == 3:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/guia.png'
    if idx == 4:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/guia.png'
    elif idx == 5:
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/guia.png'        
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 7), size=(100, 120), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(80, 10), size=(500, 120), font=0, text=name))
    return res        

class Panel(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = SCREEN_INI
		self['actions'] = NumberActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
                 'cancel': self.close, 'green': self.upgrade, 'yellow': self.news, 'blue': self.info}, -1)
                self.onLayoutFinish.append(self.updateMenuList) 
		self["status"] = ScrollLabel()
		self.selection = 'all'
		self['menu'] = CmenuList([])
		self.working = False
		self["list"] = List([])
		self.CreateInfo()
		self.Timer = eTimer()
		self.Timer.callback.append(self.listecminfo)
		self.Timer.start(1000*4, False)
	
        def CreateInfo(self):
		self.listecminfo()

	def listecminfo(self):
		listecm = ""
		try:
		    ecmfiles = open("/tmp/ecm.info", "r")
		    for line in ecmfiles:
			if line[32:]:
			    linebreak = line[23:].find(' ') + 23
			    listecm += line[0:linebreak]
			    listecm += "\n" + line[linebreak + 1:]
		        else:
			   listecm += line
		    self["status"].setText(listecm)
		    ecmfiles.close()
		except:
		    self["status"].setText("")       
           		
     	def updateMenuList(self):
            self.menu_list = []
            for x in self.menu_list:
                del self.menu_list[0]

            list = []
            idx = 0
            for x in Cmenu_list:
                list.append(CmenuListEntry(x, idx))       
                self.menu_list.append(x)
                idx += 1

            self['menu'].setList(list)	
		
	def okClicked(self):
            self.keyNumberGlobal(self['menu'].getSelectedIndex())
        
        def keyNumberGlobal(self, idx):
            sel = self.menu_list[idx]
            if sel == _('Actualizar Iptv'):
                self.session.open(iptv)
            elif sel == _('Swap'):
                self.session.open(swap)
            elif sel == _('Liberar memoria'):
                self.session.open(clear_memory)
            elif sel == _('Descargas'):
                self.session.open(Download)
            elif sel == _('Cams'):
                self.session.open(SoftcamPanel)
				
        def upgrade(self):
		self.session.open(Upgrade)
                
        def news(self):
		self.session.open(News) 
                
        def info(self):
		self.session.open(Info)                         	

	                   		
class iptv(Screen):
    def __init__(self, session):
        self.skin = SCREEN_INI
        Screen.__init__(self, session)
        self.list = []
        self['key_red'] = Button(_('Exit'))
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self['info'].setText('Pulse Exit para Salir..')
        self.timer = eTimer()
        self.timer.callback.append(self.iptv)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -2)

    def iptv(self):
        self.session.open(Console,title = _("iptv"), cmdlist = ["sh /usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/scripts/iptv"])      
    
    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['list'].getCurrent())
                self.session.open(SelectIpk, self.xmlparse, selection)
            except:
                return

        else:
            self.close
           

class swap(Screen):
    def __init__(self, session):
        self.skin = SCREEN_INI
        Screen.__init__(self, session)
        self.list = []
        self['key_red'] = Button(_('Exit'))
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self['info'].setText('Pulse Exit para Salir')
        self.timer = eTimer()
        self.timer.callback.append(self.swap)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -2)

    def swap(self):
        self.session.open(Console,title = _("swap"), cmdlist = ["sh /usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/scripts/swap"])      
    
    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['list'].getCurrent())
                self.session.open(SelectIpk, self.xmlparse, selection)
            except:
                return

        else:
            self.close

class clear_memory(Screen):
    def __init__(self, session):
        self.skin = SCREEN_INI
        Screen.__init__(self, session)
        self.list = []
        self['key_red'] = Button(_('Exit'))
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self['info'].setText('Pulse Exit para Salir')
        self.timer = eTimer()
        self.timer.callback.append(self.memory)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -2)

    def memory(self):
        self.session.open(Console,title = _("memoria"), cmdlist = ["sh /usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/scripts/mem"])      
    
    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['list'].getCurrent())
                self.session.open(SelectIpk, self.xmlparse, selection)
            except:
                return

        else:
            self.close

class Download(Screen):
  
    def __init__(self, session):
        self.skin = SCREEN_DOWNLOADS
        Screen.__init__(self, session)
        self.list = []
        self['key_red'] = Button(_('Exit'))
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self['info'].setText('Pulse Exit para Salir')
        self.timer = eTimer()
        self.timer.callback.append(self.descargas)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -2)

    def descargas(self):
        self.session.open(cams.installextra)      
    
    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['list'].getCurrent())
                self.session.open(SelectIpk, self.xmlparse, selection)
            except:
                return

        else:
            self.close


class Cams(Screen):
  
    def __init__(self, session):
        self.skin = SCREEN_DOWNLOADS
        Screen.__init__(self, session)
        self.list = []
        self['key_red'] = Button(_('Exit'))
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self['info'].setText('Pulse Exit para Salir')
        self.timer = eTimer()
        self.timer.callback.append(self.emus)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close}, -2)

    def emus(self):
        self.session.open(softcam.installextra)      
    
    def okClicked(self):
        if self.downloading == True:
            try:
                selection = str(self['list'].getCurrent())
                self.session.open(SelectIpk, self.xmlparse, selection)
            except:
                return

        else:
            self.close
        
        
def main(session, **kwargs):
	session.open(Panel)
	
def Plugins(**kwargs):
	return [
	PluginDescriptor(name = _("TUVUPanel"),
		description = _("Tuvuplus.com"),
		where = [ PluginDescriptor.WHERE_PLUGINMENU,
		PluginDescriptor.WHERE_EXTENSIONSMENU ],
		icon = "images/icono.png", fnc = main)]	
