import time
import sys, os
import urllib2,urllib
import shutil
import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
import downloader
from xml.dom.minidom import parse
import xml.etree.ElementTree
import extract
import zipfile
import ntpath

## Writen By Guy Almog From The-VIBE.CO.IL TEAM ##

addonID = "skin.eminence.zeev"
Addon = xbmcaddon.Addon(addonID)
AddonName = Addon.getAddonInfo("version")
xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
ver=xbmc_version.split(' ')

print "######### MY KODI IS " + ver[0] + " ######### "
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def renameandext(czipfile,newname):
    source = zipfile.ZipFile(czipfile, 'r')
    target = zipfile.ZipFile(newname, 'w', compression=zipfile.ZIP_DEFLATED)
    for file in source.filelist:
        if not file.filename.startswith('skin.eminence.zeev-master'):
            target.writestr(file.filename, source.read(file.filename))
        elif file.filename.startswith('skin.eminence.zeev-master'):
            target.writestr(file.filename.replace("skin.eminence.zeev-master", "skin.eminence.zeev"), source.read(file.filename))
    target.close()
    source.close()
    return True

if __name__ == '__main__':
    monitor = xbmc.Monitor()
 
while not monitor.abortRequested():
    AT = OPEN_URL('http://www.the-vibe.co.il/Packages').replace('\n','').replace('\r','')
    print "############   Checking For EM Update - The Current Ver Is " + AddonName + "  #################"
    path=xbmc.translatePath(os.path.join('special://home','addons','packages'));
    if (ver[0]=="15.2"):
        url="http://www.the-vibe.co.il/skin/CheckForUpdate";
        print "########## KODI 15.2 FOR VIBE 2 ################"
    elif (ver[0]!="15.2"):
        url="https://raw.githubusercontent.com/teamThevibe/skin.eminence.zeev/master/addon.xml";
        print "########## KODI 16 FOR VIBE 2 ################"
    lib=os.path.join(path,'EMaddon.xml')
    try: os.remove(lib)
    except: pass
    downloader.download2(url,lib)
    skinshortcutspath = xbmc.translatePath(lib).decode("utf-8")
    if xbmcvfs.exists( skinshortcutspath ):
        e = xml.etree.ElementTree.parse(skinshortcutspath).getroot()
        print "############   Checking For EM Update - The UPDATE Ver Is " + e.attrib['version'] + "  #################"
        if (e.attrib['version']!=AddonName):
            print "####### NEED SKIN UPDATE !! #############"
            xbmc.sleep(5000)
            dialog = xbmcgui.Dialog()
            confirm = dialog.yesno('Skin Have Update ' + e.attrib['version'] + '', 'Do you wish to install it ? ')
            if confirm:
                print "####### Starting update !! #############"
                url="https://github.com/teamThevibe/skin.eminence.zeev/archive/master.zip"
                lib=os.path.join(path,'EMUPDATE.zip')
                libnew=os.path.join(path,'EMUPDATEnew.zip')
                try:
                    os.remove(lib)
                    os.remove(libnew)
                except: pass            
                downloader.download(url,lib)
                renameandext(lib,libnew)
                try: os.remove(lib)
                except: pass
                addonfolder=xbmc.translatePath(os.path.join('special://','home','addons'))
                try: extract.all(libnew,addonfolder)
                except:
                    print "####### ERROR UPDATE !! #############"
                    pass
                print "####### Finished update TO " + e.attrib['version'] + "!! #############"
                try: os.remove(libnew)
                except: pass            
                dialog.ok('Finished Update To ' + e.attrib['version'] + '','Please Restart Your Kodi','')
    if monitor.waitForAbort(14400):
      # Abort was requested while waiting. We should exit
      break
