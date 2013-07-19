# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcaddon
import db
import random


def log(txt):
    xbmc.log(msg=txt, level=xbmc.LOGDEBUG)


class DBQuery:

    @staticmethod
    def remotesRootPath():
        if sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/XBMC/userdata")
        elif sys.platform.startswith("win"):
            return os.path.join(os.environ['APPDATA'], "XBMC\\userdata")
        else:
            return os.path.expanduser("~/.xbmc/userdata")

    def __init__(self):

        # Check for ~/.xbmc
        if not os.path.isdir(self.remotesRootPath()):
                os.mkdir(self.remotesRootPath())

        self.db = db.Db(os.path.join(self.remotesRootPath(), "irRemotes.db"))

        self.db.beginTransaction()

        self.db.checkTable("remoteTable", [
            {"name": "remoteId", "type": "integer primary key autoincrement"},
            {"name": "name", "type": "text"},
            {"name": "comPort", "type": "text"},
            {"name": "baudRate", "type": "text"},
            {"name": "commandTable", "type": "text"}])

        self.db.checkTable("globalCommands", [
            {"name": "name", "type": "text"},
            {"name": "value", "type": "text"}])

        self.db.checkTable("prefs", [
            {"name": "name", "type": "text"},
            {"name": "value", "type": "text"}])

        # Check Global Keyboard defaults
        self.checkDefaults("Select", 'return')
        self.checkDefaults("ScheduleRecordingTimers", 'b')
        self.checkDefaults("ContextMenu", 'c')
        self.checkDefaults("TVGuide", 'e')
        self.checkDefaults("Fastforward", 'f')
        self.checkDefaults("TVChannels", 'h')
        self.checkDefaults("Info", 'i')
        self.checkDefaults("RadioChannels", 'j')
        self.checkDefaults("RecordingsWindow", 'k')
        self.checkDefaults("ActivateWindowPlayerControls", 'm')
        self.checkDefaults("CPUUsageVideoDiag", 'o')
        self.checkDefaults("Play", 'p')
        self.checkDefaults("Queue", 'q')
        self.checkDefaults("Rewind", 'r')
        self.checkDefaults("ActivateWindowShutDownMenu", 's')
        self.checkDefaults("MarkAsWatched", 'w')
        self.checkDefaults("Stop", 'x')
        self.checkDefaults("SwitchPlayer", 'y')
        self.checkDefaults("Pause", 'space')
        self.checkDefaults("Left", 'left')
        self.checkDefaults("Right", 'right')
        self.checkDefaults("Up", 'up')
        self.checkDefaults("Down", 'down')
        self.checkDefaults("LeftCTRL", 'analogseekback')
        self.checkDefaults("RightCTRL", 'analogseekforward')
        self.checkDefaults("PageUp", 'pageup')
        self.checkDefaults("PageDown", 'pagedown')
        self.checkDefaults("Back", 'backspace')
        self.checkDefaults("PreviousMenu", 'escape')
        self.checkDefaults("SkipNext", 'period')
        self.checkDefaults("SkipPrevious", 'comma')
        self.checkDefaults("FullScreen", 'tab')
        self.checkDefaults("ScreenShot", 'printscreen')
        self.checkDefaults("VolumeDown", 'minus')
        self.checkDefaults("VolumeUp", 'plus')
        self.checkDefaults("VolumeMute", 'mute')
        self.checkDefaults("ActivateWindowFavorites", 'browser_favorites')
        self.checkDefaults("ToggleFullScreen", 'backslash')
        self.checkDefaults("shutDownMenu", 'power')  # For Frodo
        self.checkDefaults("0", 'zero')
        self.checkDefaults("1", 'one')
        self.checkDefaults("2", 'two')
        self.checkDefaults("3", 'three')
        self.checkDefaults("4", 'four')
        self.checkDefaults("5", 'five')
        self.checkDefaults("6", 'six')
        self.checkDefaults("7", 'seven')
        self.checkDefaults("8", 'eight')
        self.checkDefaults("9", 'nine')

        # Check Preferences
        self.checkPrefs("FirstRun", 'True')

        self.db.commitTransaction()

        self.checkFirstRun()

    def checkDefaults(self, name, value):
        cursor = self.db.select("globalCommands", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("globalCommands", {"name": name, "value": value})
            self.db.commitTransaction()

    def checkPrefs(self, name, value):
        cursor = self.db.select("prefs", where={"name": name})
        if not cursor.fetchone():
            self.db.beginTransaction()
            self.db.insert("prefs", {"name": name, "value": value})
            self.db.commitTransaction()

    def checkFirstRun(self):
        cursor = self.db.select("prefs", where={"name": "FirstRun"})
        checkCursor = cursor.fetchone()
        if checkCursor['value'] == 'True':
            self.setRemote('Add New Remote', '0', '0', checkCursor['value'])
            self.db.beginTransaction()
            self.db.insertOrUpdate("prefs", {"name": "FirstRun", "value": "False"}, {"name": "FirstRun"})
            self.db.commitTransaction()

    def getCurrentRemotes(self):
        remotesList = []
        remotes = self.db.select("remoteTable")
        for remote in remotes.fetchall():
            row = remote["name"]
            remotesList.append(row)

        return remotesList

    def setRemote(self, name, comPort, baudRate, firstRun):
        remotesList = []
        remotes = self.db.select("remoteTable")

        for remote in remotes.fetchall():
            row = [remote["remoteId"], remote["name"], remote["comPort"], remote["baudRate"]]
            remotesList.append(row)

        remoteId = len(remotesList)
        commandTable = ''.join((str(remoteId) + name))
        self.db.beginTransaction()
        self.db.insertOrUpdate("remoteTable", {"remoteId": remoteId, "name": name, "comPort": comPort, "baudRate": baudRate, "commandTable": commandTable}, {"remoteId": remoteId})

        if firstRun is False:
            self.db.checkTable(commandTable, [
                {"name": "hexValue", "type": "text"},
                {"name": "command", "type": "text"}])

        self.db.commitTransaction()
        return commandTable

    def updateRemote(self, remoteId, name, comPort, baudRate):
        data = {
                "remoteId": remoteId,
                "name": name,
                "comPort": comPort,
                "baudRate": baudRate}
        self.db.beginTransaction()
        self.db.insertOrUpdate("remoteTable", data, {"remoteId": remoteId})
        self.db.commitTransaction()

    def delRemote(self, remoteId):
        self.db.delete("remoteTable", where={"remoteId": remoteId})
        remoteId += 1

        remotes = self.db.select("remotetable")
        remotesList = []
        for remote in remotes.fetchall():
            row2 = [remote["remoteId"], remote["name"], remote["comPort"], remote["baudRate"]]
            remotesList.append(row2)

        row = remoteId
        oldRemoteLen = len(remotesList)

        while row < oldRemoteLen:
            update = self.db.select("remoteTable", where={"billId": remoteId})
            data = update.fetchone()
            oldRemoteId = data["remoteId"]
            remoteId = oldRemoteId - 1
            name = data["name"]
            comPort = data["comPort"]
            baudRate = data["baudRate"]
            remoteData = {
                "remoteId": remoteId,
                "name": name,
                "comPort": comPort,
                "baudRate": baudRate}
            self.db.beginTransaction()
            self.db.insertOrUpdate("remoteTable", remoteData, {"remoteId": oldRemoteId})
            self.db.commitTransaction()
            row += 1

    def getGlobalCommands(self, commandTable):
        labelsList = []
        commandsList = []
        commands = self.db.select("globalCommands")
        for command in commands.fetchall():
            labelsList.append(command["name"])
            commandsList.append(command["value"])
        return labelsList, commandsList

    def setRemoteCommands(self, commandTable, name, value):
        self.db.beginTransaction()
        self.db.insert(commandTable, {"name": name, "value": value})
        self.db.commitTransaction()

    def queryCommands(self, commandTable, hexValue):
        commands = self.db.select(commandTable)
        hexCommands = commands.fetchall()
        keys = []
        for command in hexCommands:
            keys.append(command['name'])
        if hexValue in keys:
            commands = self.db.select(commandTable, where={"name": hexValue})
            hexCommands = commands.fetchone()
            return hexCommands['value']
        return None

