from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from xml.dom import Node
from xml.dom import minidom
import os
from Components.Button import Button
from Components.ScrollLabel import ScrollLabel
from enigma import *
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from twisted.web.client import downloadPage
from twisted.web.client import getPage
import urllib
from Components.Label import Label
currversion = '1.01'

 

class installextra(Screen):

    skin = """
    <screen name="installCam" position="center,center" size="1280,720" title="TUVuplus">
    <ePixmap position="0,0" zPosition="-1" size="1279,719" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVUPanel/images/fondo.png"/>
            <widget source="session.VideoPicture" render="Pig" position="44,136" size="498,208" backgroundColor="transparent" zPosition="-1" transparent="0" />
 <!-- /* LOGOPLUS -->
 <eLabel halign="center" position="433,25" size="430,68" backgroundColor="#42b3" font="Regular;36" text="DESCARGAS" transparent="1" foregroundColor="#ffffff" valign="bottom" />
  <eLabel position="center,center" size="1280,720" transparent="0" zPosition="-15" backgroundColor="#d6d6d6" />
<widget source="session.CurrentService" render="RunningText" options="movetype=running,startpoint=0,direction=left,steptime=25,repeat=150,startdelay=1500,always=0" position="101,450" size="215,45" font="Regular; 22" transparent="1" valign="center" zPosition="2" backgroundColor="#2EFEF7" foregroundColor="#FFFFFF" noWrap="1" halign="center">
    <convert type="ServiceName">Name</convert>
  </widget>
<widget source="global.CurrentTime" render="Label" position="900,50" size="300,55" backgroundColor="un140b1" foregroundColor="metrixAccent2" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
  <convert type="ClockToText">Date</convert>
</widget>
<widget source="global.CurrentTime" render="Label" position="949,28" size="251,55" backgroundColor="un140b1" foregroundColor="metrixAccent2" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
  <convert type="ClockToText">Format:%-H:%M</convert>
</widget>
    <ePixmap name="red" position="620,658" zPosition="2" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVuplus/images/red.png" transparent="1" alphatest="on" />
    <ePixmap name="green" position="825,658" zPosition="2" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVuplus/images/green.png" transparent="1" alphatest="on" />
    <widget name="key_red" position="620,638" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
    \n\t\t\t<widget name="list" position="641,140" size="629,431" scrollbarMode="showOnDemand" transparent="1" />\n\t\t\t<eLabel position="70,100" zPosition="-1" />
    \n\t\t        <widget name="fspace" position="0,320" zPosition="4" size="600,80" font="Regular;24" foregroundColor="#aaaaaa" transparent="1" halign="left" valign="center" />
   </screen>"""


    def __init__(self, session):
        self.skin = installextra.skin
        Screen.__init__(self, session)
        self['key_red'] = Button(_('Exit'))
        self.list = []
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self['info'].setText('Descarga grupos de plugin, espere un momento')
        self.timer = eTimer()
        self.timer.callback.append(self.downloadxmlpage)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'cancel': self.close,
         'red': self.close}, -2)

    def updateable(self):
        try:
            selection = str(self.names[0])
            lwords = selection.split('_')
            lv = lwords[1]
            self.lastversion = lv
            if float(lv) == float(currversion):
                return False
            if float(lv) > float(currversion):
                return True
            return False
        except:
            return False

    def downloadxmlpage(self):
        url = 'http://tuvuplus.com/app/files/servidor.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)
        self['info'].setText('Ha fallado, o no tienes conexion a internet o el servidor KO !')
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = data
        try:
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
                self.data = []
                self.names = []
                icount = 0
                list = []
                xmlparse = xmlstr
                self.xmlparse = xmlstr
                for plugins in xmlstr.getElementsByTagName('plugins'):
                    self.names.append(plugins.getAttribute('cont').encode('utf8'))

                self.list = list
                self['info'].setText('')
                self['list'].setList(self.names)
                self.downloading = True
            else:
                self.downloading = False
                self['info'].setText('Ha fallado, o no tienes conexion a internet o el servidor KO !')
                return
        except:
            self.downloading = False
            self['info'].setText('Error datos servidor')

    def okClicked(self):
        if self.downloading == True:
            try:
                self.downloading = True
                selection = str(self['list'].getCurrent())
                self.session.open(SelectIpk, self.xmlparse, selection)
            except:
                return


class SelectIpk(Screen):

    skin = """
    <screen name="installCam" position="center,center" size="1280,720" title="TUVuplus">    
    <ePixmap name="red" position="62,688" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVuplus/images/red.png" transparent="1" alphatest="on" />
    <ePixmap name="green" position="225,688" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TUVuplus/images/green.png" transparent="1" alphatest="on" />
    <widget name="key_red" position="62,658" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
    \n\t\t\t<widget name="list" position="600,200" size="580,500" scrollbarMode="showOnDemand" transparent="1" />
    \n\t\t\t  <widget name="countrymenu" position="80,90" zPosition="-1" size="580,500" scrollbarMode="showOnDemand" transparent="1" />\n\t
    </screen>"""

    def __init__(self, session, xmlparse, selection):
        self.skin = SelectIpk.skin
        Screen.__init__(self, session)
        self['key_red'] = Button(_('Exit'))
        self.list = []
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self['info'].setText('')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.selClicked,
         'cancel': self.close,
         'red': self.close}, -2)

        self.xmlparse = xmlparse
        self.selection = selection
        list = []
        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
                    list.append(plugin.getAttribute('name').encode('utf8'))
                continue

        list.sort()
        self['countrymenu'] = MenuList(list)
    
    def selClicked(self):
        try:
            selection_country = self['countrymenu'].getCurrent()
        except:
            return

        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
                    if plugin.getAttribute('name').encode('utf8') == selection_country:
                        urlserver = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
                        pluginname = plugin.getAttribute('name').encode('utf8')
                        self.prombt(urlserver, pluginname)
                        continue
                    else:
                        continue

                continue

        return

    def prombt(self, com, dom):
        self.com = com
        self.dom = dom
        if self.selection == 'Skins':
            self.session.openWithCallback(self.callMyMsg, MessageBox, _('No tienes instalado skin compatible?'), MessageBox.TYPE_YESNO)
            
        else:
            self.session.open(Console, _('downloading-installing: %s') % dom, ['opkg install -force-overwrite %s' % com])
        self.close()

    def callMyMsg(self, result):
        if result:
            dom = self.dom
            com = self.com
            self.session.open(Console, _('downloading-installing: %s') % dom, ['ipkg install -force-overwrite %s' % com])
