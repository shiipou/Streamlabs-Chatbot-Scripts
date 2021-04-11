import clr
import sys
import json
import os
import ctypes
import codecs

ScriptName = "Welcome Announcer"
Website = "http://www.github.com/Bare7a/Streamlabs-Chatbot-Scripts"
Description = "Welcome Announcer for Streamlabs Bot"
Creator = "Bare7a"
Version = "1.2.8"

configFile = "config.json"
settings = {}
volume = 0.1
command = "__WelcomeAnnouncer__"
soundspath = ""
sounds = []
userList = []

def ScriptToggled(state):
	return

def Init():
	global sounds, soundspath, volume, settings, userList

	path = os.path.dirname(__file__)
	soundspath = path + "\\sounds"

	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
			"sourceName": "",
			"permission": "Everyone",
			"volume": 50.0,
			"useCooldown": True,
			"useCooldownMessages": False,
			"cooldown": 600,
			"onCooldown": "$user, $command is still on cooldown for $cd minutes!",
			"userCooldown": 1800,
			"onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
			"responseHello": "Hello, $user!"
		}

	volume = settings["volume"] / 1000.0
	sounds = os.listdir(soundspath)

	return

def Execute(data):
	if data.IsChatMessage() and (data.User not in userList) and Parent.HasPermission(data.User, settings["permission"], "") and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):
		outputMessage = ""
		userId = data.User
		username = data.UserName
		userList.append(data.User)

		if settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, command) or Parent.IsOnUserCooldown(ScriptName, command, userId)):
			if settings["useCooldownMessages"]:
				if Parent.GetCooldownDuration(ScriptName, command) > Parent.GetUserCooldownDuration(ScriptName, command, userId):
					cdi = Parent.GetCooldownDuration(ScriptName, command)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2)
					outputMessage = settings["onCooldown"]
				else:
					cdi = Parent.GetUserCooldownDuration(ScriptName, command, userId)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2)
					outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
			else:
				outputMessage = ""
		else:
			sound = sounds[Parent.GetRandom(0, len(sounds))]
			Parent.SetOBSSourceRender(settings["sourceName"], true)


			soundpath = soundspath + "\\" + sound
			if Parent.PlaySound(soundpath, volume):
				if settings["useCooldown"]:
					Parent.AddUserCooldown(ScriptName, command, userId, settings["userCooldown"])
					Parent.AddCooldown(ScriptName, command, settings["cooldown"])
			outputMessage = settings["responseHello"]

		outputMessage = outputMessage.replace("$user", username)

		Parent.SendStreamMessage(outputMessage)

		sleep(settings["eventDuration"])
		Parent.SetOBSSourceRender(settings["sourceName"], true)

	return

def ReloadSettings(jsonData):
	Init()

	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def Tick():

	result = Parent.GetViewerList()

	for userId in result:
		userList.append(userId)
		outputMessage = ""
		username = Parent.GetDisplayName(userId)

		if settings["useCooldown"] and (Parent.IsOnCooldown(ScriptName, command) or Parent.IsOnUserCooldown(ScriptName, command, userId)):
			if settings["useCooldownMessages"]:
				if Parent.GetCooldownDuration(ScriptName, command) > Parent.GetUserCooldownDuration(ScriptName, command, userId):
					cdi = Parent.GetCooldownDuration(ScriptName, command)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2)
					outputMessage = settings["onCooldown"]
				else:
					cdi = Parent.GetUserCooldownDuration(ScriptName, command, userId)
					cd = str(cdi / 60) + ":" + str(cdi % 60).zfill(2)
					outputMessage = settings["onUserCooldown"]
				outputMessage = outputMessage.replace("$cd", cd)
			else:
				outputMessage = ""
		else:
			sound = sounds[Parent.GetRandom(0, len(sounds))]
			Parent.SetOBSSourceRender(settings["sourceName"], true)

			soundpath = soundspath + "\\" + sound
			if Parent.PlaySound(soundpath, volume):
				if settings["useCooldown"]:
					Parent.AddUserCooldown(ScriptName, command, userId, settings["userCooldown"])
					Parent.AddCooldown(ScriptName, command, settings["cooldown"])
			outputMessage = settings["responseHello"]

		outputMessage = outputMessage.replace("$user", username)

		Parent.SendStreamMessage(outputMessage)

		sleep(settings["eventDuration"])
		Parent.SetOBSSourceRender(settings["sourceName"], false)
	return
