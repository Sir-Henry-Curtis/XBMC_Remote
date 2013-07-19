import sys, os
import xbmc, xbmcaddon

# Script constants
__addon__ = xbmcaddon.Addon()
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
__cwd__ = __addon__.getAddonInfo('path')


def log(txt):
    xbmc.log(msg=txt, level=xbmc.LOGDEBUG)

log("[SCRIPT] '%s: version %s' initialized!" % (__addon__, __version__, ))

if (__name__ == "__main__"):
    import resources.lib.remoteEditor as remoteEditor
    ui = remoteEditor.RemoteClass("script-IR_Remote-remoteEditor.xml", __cwd__, "default")
    del ui

sys.modules.clear()
