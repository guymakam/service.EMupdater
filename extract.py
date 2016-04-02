import zipfile
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys

def all(_in, _out, dp=None):
    if dp:
        return allWithProgress(_in, _out, dp)

    return allNoProgress(_in, _out)
        

def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True


def allWithProgress(_in, _out, dp):

    zin = zipfile.ZipFile(_in,  'r')

    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            try:
                count += 1
                update = count / nFiles * 100
                dp.update(int(update))
                zin.extract(item, _out)
            except:
                continue
    except Exception, e:
        print str(e)
        #dialog = xbmcgui.Dialog()
        #dialog.ok("[COLOR=red][B]ERROR[/COLOR][/B]", str(e),'')
        #return False

    return True
