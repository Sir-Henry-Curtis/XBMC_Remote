
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html

import os
import sys
import xbmcaddon
import xbmc
import time
from resources.library.remoteClient.xbmcclient import XBMCClient
from resources.library import serial
from resources.library import dbQuery
from resources.library import db

__scriptname__ = "IRRemote Service"
__author__ = "jlbrian"
__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString
__cwd__ = __settings__.getAddonInfo('path')
__layoutDir__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'layout'))

STARTUP = True
remoteClient = XBMCClient("IR Remote")
remoteClient.connect()


def remotesRootPath():
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/XBMC/userdata")
    elif sys.platform.startswith("win"):
        return os.path.join(os.environ['APPDATA'], "XBMC\\userdata")
    else:
        return os.path.expanduser("~/.xbmc/userdata")


def log(msg):
    xbmc.log("### [%s] - %s" % (__scriptname__, msg, ), level=xbmc.LOGDEBUG)


while (not xbmc.abortRequested):
    remotesDb = db.Db(os.path.join(remotesRootPath(), "irRemotes.db"))
    remoteSerial = serial.Serial
    if STARTUP:
        remotesList = dbQuery.DBQuery().getCurrentRemotes()
        for remote in remotesList:
            aRemote = remotesDb.select("remoteTable", where={"name": remote})
            getRemote = aRemote.fetchone()
            try:
                remoteVar = getRemote['name']
                vars()[remoteVar] = remoteSerial(getRemote['comPort'], getRemote['baudRate'])
            except:
                if getRemote['comPort'] == 0 or getRemote['comPort'] == '0':
                    pass
                else:
                    print "Invalid Comm Port: " + getRemote['comPort']
        STARTUP = False
    else:
        hexVal = ''
        for remote in remotesList:
            aRemote = remotesDb.select("remoteTable", where={"name": remote})
            getRemote = aRemote.fetchone()
            try:
                remoteVar = globals()[getRemote['name']]
                hexVal = remoteVar.readline()
            except:
                pass
            if hexVal != '':
                commandTable = getRemote['commandTable']
                keys = []
                commands = remotesDb.select(commandTable)
                for command in commands.fetchall():
                    keys.append(command['hexValue'])
                if hexVal in keys:
                    commands = remotesDb.select(commandTable, where={"hexValue": hexVal})
                    hexCommands = commands.fetchone()
                    command = hexCommands['command']
                remoteClient.send_keyboard_button(command)
                time.sleep(0.1)
                remoteClient.release_button()
                remoteClient.close()


for remote in remotesList:
    aRemote = remotesDb.select("remoteTable", where={"name": remote})
    getRemote = aRemote.fetchone()
    try:
        remoteVar = globals()[getRemote['name']]
        hexVal = remoteVar.close()
    except:
        print 'Could not close ' + getRemote['name'] + ' serial connection.'
