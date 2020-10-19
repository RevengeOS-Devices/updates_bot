from homebot import bot_path, dispatcher, get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW
from importlib import import_module
from pkgutil import iter_modules
from telegram.ext import CommandHandler

modules_dir = bot_path / "modules"

modules_list = []
commands_list = []

def init_modules():
	global modules_list
	modules_list = [name for _, name, _ in iter_modules([modules_dir])]
	for module in modules_list:
		load_module(module)
	LOGI("Modules loaded")

def load_module(module):
	import_module('homebot.modules.' + module, package="*")
	LOGI("Loading module " + module + " finished")

def unload_module(module):
	LOGI("Unloading" + module + "is WIP")

def add_command(entry):
	global commands_list
	commands_list += entry

def remove_command(entry):
	global commands_list
	commands_list += entry

def get_modules_list():
	return modules_list

def get_commands_list():
	return commands_list

def register(commands):
	def decorator(func):
		async def wrapper(check):
			try:
				await func(check)
			except BaseException as e:
				LOGE(e)
			else:
				pass

		dispatcher.add_handler(CommandHandler(commands, func, run_async=True))

		if type(commands) is list:
			for command in commands:
				add_command(command)
		else:
			add_command(commands)

		return wrapper

	return decorator
